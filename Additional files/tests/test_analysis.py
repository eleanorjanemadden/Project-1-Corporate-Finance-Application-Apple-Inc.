import copy
import hashlib
import json
import math
import subprocess
import sys
import os
from pathlib import Path
import unittest
import analysis as a

ROOT=Path(__file__).resolve().parents[1]

class FinanceChecks(unittest.TestCase):
    def test_published_course_abg_known_answer(self):
        # Professor tutorial slides 34–36: rounded FCFE, not Apple evidence.
        source=(ROOT/'sources/course_abg_slides.html').read_text()
        self.assertIn('$291.75',source)
        flows=[211.4,255.1,299.7,320.9,342.3]
        pv=a.discounted(flows,.10,.025)['explicit_pv']
        terminal=(342.3+150)*1.025/(.10-.025)/1.10**5
        self.assertAlmostEqual((pv+terminal)/17.95,291.75,delta=.05)
        self.assertAlmostEqual(terminal/(pv+terminal),.7976,delta=.001)

    def test_published_fcff_definition_and_reverse_known_answer(self):
        # Damodaran published Boeing example, slide 47: implied growth 6.11%.
        g=(40789*.0917-1176)/(40789+1176)
        self.assertAlmostEqual(g,.0611,delta=.00005)
        self.assertAlmostEqual(1176*(1+g)/(.0917-g),40789,places=6)

    def test_base_year_filing_reconciliation(self):
        # Independently transcribed from printed FY25 statement pages 29,31,33.
        expected=dict(revenue=416161,cash=35934,securities=18763+77723,
            receivables=39777,vendor_receivables=33180,inventory=5718,
            other_current_assets=14585,ppe=49834,other_assets=83727,
            payables=69860,deferred_revenue=9055,other_liabilities=66387+41549,
            commercial_paper=7979,debt=12350+78328,revolver=0,equity=73733)
        self.assertEqual(expected,a.model.OPENING)
        self.assertEqual(sum(expected[k] for k in a.model.ASSET_KEYS),359241)
        self.assertEqual(sum(expected[k] for k in a.model.LIABILITY_KEYS),285508)
        self.assertEqual(195201-27601-34550,133050)
        self.assertEqual(133050-321-20719,112010)
        cfo=112010+11698+12863-89-6682-347+1400-9197+902-11076
        self.assertEqual(cfo,111482)
        text=(ROOT/'sources/aapl-20250927.txt').read_text()
        for token in ('416,161','359,241','111,482','14,773,260'):self.assertIn(token,text)
        self.assertEqual(a.BASE['shares'],14773.260)

    def test_all_cases_articulate_and_fcff_routes(self):
        result=a.run_analysis()
        for case in result['cases'].values():
            a.model.assert_balanced(case['statements'],case['assumptions'])
            for r in case['statements']:
                self.assertAlmostEqual(r['fcff'],r['fcff_cash_route'],places=6)
                self.assertAlmostEqual(r['fcff'],r['fcfe']+r['repayment']+r['interest']*(1-case['assumptions']['tax_rate']),delta=1e-6)
            v=case['valuation']
            self.assertAlmostEqual(v['equity_value'],v['enterprise_value']+v['surplus_assets']-v['debt'],places=6)

    def test_financing_and_forecast_cash_do_not_create_fcff_value(self):
        base=a.calculate()
        other=a.calculate({'buyback':0.,'repayments':(0.,)*5})
        self.assertAlmostEqual(base['valuation']['per_share'],other['valuation']['per_share'])
        self.assertNotEqual(base['statements'][-1]['cash'],other['statements'][-1]['cash'])

    def test_signed_flows_and_boundaries(self):
        got=a.discounted([-100,50,60,70,80],.1,.02)
        expect=sum(x/1.1**i for i,x in enumerate([-100,50,60,70,80],1))
        self.assertAlmostEqual(got['explicit_pv'],expect)
        self.assertLess(got['explicit_pv'],a.discounted([0,50,60,70,80],.1,.02)['explicit_pv'])
        for w,g in ((.02,.02),(.01,.02),(float('nan'),.02)):
            with self.assertRaises(ValueError):a.discounted([100]*5,w,g)
        with self.assertRaises(ValueError):a.discounted([100,100,100,100,-1],.1,.02)

    def test_monotonicity_changed_input_and_restoration(self):
        # AI-assisted expectation written before executing this test: higher margin/growth increases value; higher WACC lowers it.
        base=a.calculate()
        self.assertGreater(a.calculate({'gross_margin':.51})['valuation']['per_share'],base['valuation']['per_share'])
        self.assertGreater(a.calculate({'growth':(.17,.10,.08,.07,.06)})['valuation']['per_share'],base['valuation']['per_share'])
        self.assertLess(a.calculate(wacc=.11)['valuation']['per_share'],base['valuation']['per_share'])
        self.assertGreater(a.calculate(growth=.03)['valuation']['per_share'],base['valuation']['per_share'])
        self.assertEqual(a.calculate(),base)

    def test_highest_risk_omitted_vendor_wc_detected(self):
        rows=a.model.project(a.BASE)
        amount=rows[0]['change_vendor_receivables']
        for key in ('cfo','fcfe','cash','assets','equity'):rows[0][key]+=amount
        with self.assertRaisesRegex(ValueError,'cfo gap'):a.model.assert_balanced(rows,a.BASE)
        self.assertTrue(a.demo_failure()['recovered'])

    def test_peer_definitions(self):
        for r in a.comparables():
            self.assertEqual(r['price_date'],'2025-09-26')
            self.assertAlmostEqual(r['pe'],r['price']*r['shares']/r['net_income'])
            self.assertAlmostEqual(r['ev_ebit'],(r['market_equity']+r['debt']-r['cash_securities'])/r['ebit'])
        with self.assertRaises(ValueError):a.comparable(dict(price=10,shares=1,ebit=0,net_income=1))

    def test_frozen_contract_matches_engine(self):
        saved=json.loads((ROOT/'outputs/retrospective/visible_output.json').read_text())
        self.assertEqual(saved,json.loads(json.dumps(a.run_analysis())))

    def test_reverse_reprices_and_preservation(self):
        reverse=a.reverse_dcf()
        self.assertAlmostEqual(reverse['repriced'],reverse['target'],places=6)
        if os.environ.get('APPLE_COLD_STAGING') == 'runtime_only':
            self.skipTest('Protected originals not staged in runtime cold run; separate original-content check remains incomplete')
        # OneDrive placeholders can block indefinitely. An unavailable read is a skip, never PASS.
        code = '''import csv, hashlib
from pathlib import Path
root=Path.cwd()
print('READ FILE-INVENTORY.csv (original supplied expected hashes)',flush=True)
rows=[r for r in csv.DictReader((root/'FILE-INVENTORY.csv').open()) if r['path'].startswith('existing_work/')]
assert len(rows)==19
for r in rows:
 print('READ '+r['path'],flush=True)
 assert hashlib.sha256((root/r['path']).read_bytes()).hexdigest()==r['sha256'], r['path']
print('PRESERVATION PASS: all19 protected files match original supplied inventory')
'''
        try:
            checked=subprocess.run([sys.executable,'-B','-S','-c',code],cwd=ROOT,capture_output=True,text=True,timeout=15)
        except subprocess.TimeoutExpired as error:
            output=error.stdout.decode() if isinstance(error.stdout,bytes) else (error.stdout or '')
            self.skipTest('OneDrive read unavailable; preservation NOT reverified: '+output.splitlines()[-1])
        self.assertEqual(checked.returncode,0,checked.stdout+checked.stderr)
        print(checked.stdout)

if __name__=='__main__':unittest.main()
