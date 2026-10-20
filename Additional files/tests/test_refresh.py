import copy
import csv
import json
from pathlib import Path
import unittest
import analysis as old
import dated_refresh as new

ROOT=Path(__file__).resolve().parents[1]

class RefreshChecks(unittest.TestCase):
    def test_selected_retrospective_baseline(self):
        inputs=dict(gross_margin=.48,rd_ratio=.10,capex_ratio=.035,buyback=0.,shares=15000.,min_cash=35000.)
        r=old.run_analysis(inputs)
        self.assertEqual(r['base'],r['cases']['base'])
        for row in r['sensitivity']:
            selected=dict(r['base']['assumptions'])
            width=.02 if row['range']=='supplied' else .01
            mw=.02 if row['range']=='supplied' else .04
            side=-1 if row['side']=='low' else 1
            if row['driver']=='growth':selected['growth']=tuple(x+side*width for x in selected['growth'])
            else:selected['gross_margin']+=side*mw
            expected=old.calculate(selected)
            self.assertAlmostEqual(row['value_change'],expected['valuation']['per_share']-r['base']['valuation']['per_share'])
        first=r['wacc_growth'][0]
        self.assertEqual(first['per_share'],old.calculate(r['base']['assumptions'],first['wacc'],first['g'])['valuation']['per_share'])
        self.assertTrue(r['restored_base_equal'])

    def test_nonconstant_selected_margin_baseline(self):
        r=old.run_analysis(dict(gross_margin=(.47,.48,.49,.50,.51),buyback=0.,shares=16000.))
        self.assertEqual(r['base'],r['cases']['base'])
        high=next(x for x in r['sensitivity'] if x['range']=='supplied' and x['driver']=='gross_margin' and x['side']=='high')
        a=dict(r['base']['assumptions'],gross_margin=(.49,.50,.51,.52,.53))
        self.assertAlmostEqual(high['per_share'],old.calculate(a)['valuation']['per_share'])
        self.assertTrue(r['restored_base_equal'])

    def test_risk_free_observation_and_wacc(self):
        with (ROOT/'sources/dgs10_july2026.csv').open() as source:
            rates=list(csv.DictReader(source))
        observation=next(x for x in rates if x['observation_date']=='2026-07-30')
        self.assertAlmostEqual(float(observation['DGS10'])/100,new.RISK_FREE,places=12)
        base=new.calculate()['valuation'];dw=base['debt_weight']
        expected=(1-dw)*(.0468+1.10*.055)+dw*.05*(1-.21)
        self.assertAlmostEqual(base['wacc'],expected)

    def test_selected_minimum_cash_bridge(self):
        a=old.calculate({'buyback':0.});b=old.calculate({'buyback':0.,'min_cash':35000.})
        self.assertEqual(a['valuation']['surplus_assets']-b['valuation']['surplus_assets'],5000)
        self.assertAlmostEqual(a['valuation']['equity_value']-b['valuation']['equity_value'],5000)
        a=new.calculate();b=new.calculate({'min_cash':35000.})
        self.assertAlmostEqual(a['valuation']['equity_value']-b['valuation']['equity_value'],5000)
        for invalid in (-1.,float('nan')):
            with self.assertRaises(ValueError):old.calculate({'min_cash':invalid})
            with self.assertRaises(ValueError):new.calculate({'min_cash':invalid})

    def test_ledger_fact_assumption_separation(self):
        rows={r['id']:r for r in csv.DictReader((ROOT/'docs/source_ledger.csv').open())}
        self.assertIn('p29',rows['FY25_revenue']['locator'])
        self.assertNotIn('p31',rows['FY25_revenue']['locator'])
        self.assertEqual(rows['FY25_revolver']['kind'],'assumed')
        self.assertIn('not a reported',rows['FY25_revolver']['source'])
        self.assertIn('not independently reported',rows['FY25_revolver']['verification'])

    def test_reported_opening_and_stub_articulation(self):
        self.assertEqual(sum(new.REPORTED[k] for k in old.model.ASSET_KEYS),383266)
        self.assertEqual(sum(new.REPORTED[k] for k in old.model.LIABILITY_KEYS),275746)
        r=new.calculate();self.assertEqual(r['stub']['year'],2026)
        self.assertEqual([x['year'] for x in r['statements']],list(range(2027,2032)))
        self.assertAlmostEqual(old.model.balance_gap(r['estimated_date_balance']),0,places=6)
        for row in [r['stub']]+r['statements']:
            self.assertAlmostEqual(row['fcff'],row['fcff_cash_route'],places=6)
        self.assertAlmostEqual(r['valuation']['fcff'][0],r['stub']['fcff']*(1-r['elapsed_fraction']))
        self.assertAlmostEqual(r['valuation']['elapsed_stub_fcff_excluded']+r['valuation']['fcff'][0],r['stub']['fcff'])

    def test_timing_bridge_and_boundaries(self):
        r=new.calculate();v=r['valuation']
        self.assertEqual(v['discount_times'][0],57/365)
        self.assertGreater(v['discount_times'][-1],5.)
        self.assertAlmostEqual(v['explicit_pv'],sum(cf/(1+v['wacc'])**t for cf,t in zip(v['fcff'],v['discount_times'])))
        self.assertAlmostEqual(v['equity_value'],v['enterprise_value']+v['surplus_assets']-v['debt'])
        self.assertLess(new.calculate(wacc=.11)['valuation']['per_share'],v['per_share'])
        self.assertGreater(new.calculate(terminal_growth=.03)['valuation']['per_share'],v['per_share'])
        with self.assertRaises(ValueError):new.calculate(wacc=.025,terminal_growth=.025)
        self.assertTrue(new.demo_failure()['recovered'])

    def test_dated_peers_match_windows_and_definitions(self):
        rows,implied=new.peers()
        self.assertEqual({x['price_date'] for x in rows},{'2026-07-31'})
        self.assertEqual(rows[0]['ebit'],154859)
        self.assertEqual(rows[0]['net_income'],128930)
        self.assertEqual(rows[1]['ebit'],155237)
        self.assertEqual(rows[1]['debt'],40294)
        for r in rows:
            self.assertAlmostEqual(r['ev_ebit'],(r['price']*r['shares']+r['debt']-r['cash_securities'])/r['ebit'])
            self.assertAlmostEqual(r['pe'],r['price']*r['shares']/r['net_income'])
        self.assertGreater(implied['pe_price'],0)

    def test_dated_contract_and_restoration(self):
        r=new.run_analysis()
        for f in ('outputs/visible_output.json','outputs/dated/visible_output.json'):
            self.assertEqual(json.loads((ROOT/f).read_text()),json.loads(json.dumps(r)))
        self.assertAlmostEqual(r['reverse_dcf']['repriced'],new.PRICE,places=6)
        self.assertTrue(r['restored_base_equal'])
