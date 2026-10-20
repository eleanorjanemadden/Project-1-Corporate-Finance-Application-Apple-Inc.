"""Dated extension of the existing Apple engine; no live downloads or global mutation."""
from datetime import date
import json
import copy
from pathlib import Path
import apple_proforma as model
import analysis

ROOT = Path(__file__).resolve().parent
AS_OF = date(2026, 7, 31)
REPORT_DATE = date(2026, 6, 27)
FY26_END = date(2026, 9, 26)
ENDS = [date(2027,9,25),date(2028,9,30),date(2029,9,29),date(2030,9,28),date(2031,9,27)]
RISK_FREE = .0468  # July30 DGS10, primary FRED/H.15 CSV; July31 end-of-day cutoff.
BETA = 1.10  # Analyst risk assumption, not a newly estimated regression.
ERP = .055  # Analyst premium assumption.
COST_EQUITY = RISK_FREE + BETA * ERP
PRICE = 308.91  # July31 unadjusted close; source ledger records provider and date.
BASIC_SHARES = 14594.180  # July17 cover count, NOT July31 measurement.
DILUTION_PROXY = 14714.676 - 14656.110  # Q3 weighted-average diluted less basic.
SHARES = BASIC_SHARES + DILUTION_PROXY  # Estimated common equivalents, not reported count.
REPORTED = dict(revenue=0.,cash=39544.,securities=22855.+84118.,receivables=31398.,
    vendor_receivables=27509.,inventory=11092.,other_current_assets=17420.,ppe=51431.,
    other_assets=20342.+77557.,payables=64525.,deferred_revenue=9538.,
    other_liabilities=62259.+55080.,commercial_paper=1997.,debt=11007.+71340.,
    revolver=0.,equity=107520.)
BASE = dict(growth=(.08,.06,.05,.04,.03),gross_margin=(.48,.485,.49,.49,.49),
            shares=SHARES,repayments=(0.,)*5,buyback=75000.,dividend=16000.)


def add_fcff(rows, tax):
    for r in rows:
        r['nopat'] = r['operating_income'] * (1-tax)
        r['operating_da'] = r['depreciation'] + r['other_da']
        r['fcff'] = r['nopat'] + r['operating_da'] - r['capex'] - r['other_reinvestment'] - r['change_nwc']
        r['fcff_cash_route'] = r['cfo'] + r['cfi'] + r['nopat'] - r['net_income']
        if abs(r['fcff']-r['fcff_cash_route']) > model.TOLERANCE:
            raise ValueError('Dated FCFF routes disagree')


def calculate(overrides=None, wacc=None, terminal_growth=.025, q4_growth=.10, q4_margin=.475):
    a = model.parameters(dict(BASE, **(overrides or {})))
    # FY25Q4 = FY25 annual less comparable nine months. Only information available by AS_OF.
    q4_revenue = (416161.-313695.) * (1+q4_growth)
    annual_revenue = 364357. + q4_revenue
    opening = dict(REPORTED, revenue=annual_revenue)
    stub_a = dict(a,growth=(0.,)*5,gross_margin=q4_margin)
    fraction = (FY26_END-REPORT_DATE).days / 365
    stub_rows = model.project(stub_a,opening_balance=opening,years=(2026,),
                              first_fraction=fraction,first_revenue=q4_revenue)
    model.assert_balanced(stub_rows,stub_a,opening_balance=opening,years=(2026,))
    add_fcff(stub_rows,a['tax_rate'])
    stub = stub_rows[0]
    annual_opening = dict(stub,revenue=annual_revenue)
    rows = model.project(a,opening_balance=annual_opening,years=tuple(range(2027,2032)))
    model.assert_balanced(rows,a,opening_balance=annual_opening,years=tuple(range(2027,2032)))
    add_fcff(rows,a['tax_rate'])
    elapsed = (AS_OF-REPORT_DATE).days/(FY26_END-REPORT_DATE).days
    # Explicit straight-line interpolation assumption, NOT a July31 reported balance.
    estimated = {k:REPORTED[k]+elapsed*(stub[k]-REPORTED[k]) for k in model.ASSET_KEYS+model.LIABILITY_KEYS+('equity',)}
    if abs(model.balance_gap(estimated)) > model.TOLERANCE:
        raise ValueError('Estimated valuation-date balance sheet does not balance')
    if estimated['cash'] < a['min_cash']:
        raise ValueError('Estimated valuation-date operating cash reserve not funded')
    remaining_stub = stub['fcff']*(1-elapsed)
    times = [(FY26_END-AS_OF).days/365]+[(end-AS_OF).days/365 for end in ENDS]
    flows = [remaining_stub]+[r['fcff'] for r in rows]
    equity_market = PRICE * BASIC_SHARES
    debt_weight = (REPORTED['debt']+REPORTED['commercial_paper'])/(equity_market+REPORTED['debt']+REPORTED['commercial_paper'])
    selected_wacc = ((1-debt_weight)*COST_EQUITY+debt_weight*.05*(1-.21)) if wacc is None else wacc
    if not 0 <= terminal_growth < selected_wacc or flows[-1] <= 0:
        raise ValueError('Invalid dated perpetuity')
    pvs = [cf/(1+selected_wacc)**t for cf,t in zip(flows,times)]
    terminal = flows[-1]*(1+terminal_growth)/(selected_wacc-terminal_growth)
    terminal_pv = terminal/(1+selected_wacc)**times[-1]
    ev = sum(pvs)+terminal_pv
    surplus = estimated['securities']+max(0.,estimated['cash']-a['min_cash'])
    debt = estimated['debt']+estimated['commercial_paper']
    equity = ev+surplus-debt
    val = dict(per_share=equity/a['shares'],basic_per_share=equity/BASIC_SHARES,enterprise_value=ev,
        explicit_pv=sum(pvs),terminal_pv=terminal_pv,terminal_share=terminal_pv/ev,
        equity_value=equity,surplus_assets=surplus,debt=debt,other_claims=0.,shares=a['shares'],
        wacc=selected_wacc,terminal_growth=terminal_growth,debt_weight=debt_weight,
        terminal_value=terminal,terminal_fcff=flows[-1]*(1+terminal_growth),
        terminal_reinvestment_rate=(rows[-1]['nopat']-rows[-1]['fcff'])/rows[-1]['nopat'],
        terminal_implied_roic=terminal_growth/((rows[-1]['nopat']-rows[-1]['fcff'])/rows[-1]['nopat']),
        remaining_stub_fcff=remaining_stub,elapsed_stub_fcff_excluded=stub['fcff']*elapsed,
        present_values=pvs,discount_times=times,fcff=flows)
    if abs(equity-ev-surplus+debt)>1e-6:raise ValueError('Dated bridge failure')
    return dict(assumptions=a,q4_growth=q4_growth,q4_margin=q4_margin,stub=stub,
        reported_opening=REPORTED,estimated_date_balance=estimated,elapsed_fraction=elapsed,
        statements=rows,checks=model.check_rows(rows,a,annual_opening),valuation=val)


def peers():
    # Existing peer policy predates this refresh; use June-ending trailing-year windows.
    inputs=[dict(ticker='AAPL',price=PRICE,shares=BASIC_SHARES,ebit=133050.+122432.-100623.,
        net_income=112010.+101464.-84544.,debt=84344.,cash_securities=146517.,
        period='TTM ended 2026-06-27',share_date='2026-07-17',balance_date='2026-06-27'),
        dict(ticker='MSFT',price=464.72,shares=7427.,ebit=155237.,net_income=133749.,
        debt=9227.+31067.,cash_securities=20935.+55908.,period='TTM ended 2026-06-30',
        share_date='2026-06-30',balance_date='2026-06-30')]
    rows=[analysis.comparable(dict(x,price_date=str(AS_OF),status='Latest reported balances/counts held as valuation-date proxies; not exact date balances')) for x in inputs]
    apple,msft=rows
    implied=dict(peer='MSFT',ev_ebit_price=(msft['ev_ebit']*apple['ebit']+apple['cash_securities']-apple['debt'])/SHARES,
        pe_price=msft['pe']*apple['net_income']/SHARES,
        ev_ebit_basic_price=(msft['ev_ebit']*apple['ebit']+apple['cash_securities']-apple['debt'])/BASIC_SHARES,
        pe_basic_price=msft['pe']*apple['net_income']/BASIC_SHARES,
        note='One admitted peer; two method diagnostics, not a peer range. No averaging. GAAP P/E includes investment gains.')
    return rows,implied


def run_analysis(inputs=None):
    selected=dict(BASE,**(inputs or {}));base=calculate(selected)
    cases={'low':calculate(dict(selected,growth=(.02,.02,.02,.02,.02),gross_margin=.44,rd_ratio=.105,capex_ratio=.04,buyback=0.),wacc=.11,terminal_growth=.02,q4_growth=.05,q4_margin=.45),
           'base':base,
           'high':calculate(dict(selected,growth=(.10,.08,.07,.06,.05),gross_margin=.51),wacc=.09,terminal_growth=.03,q4_growth=.11,q4_margin=.48)}
    sensitivity=[];details=[];rankings=[]
    for label,width,mw in [('supplied',.02,.02),('alternative',.01,.04)]:
        for driver in ('growth','gross_margin'):
            for side in (-1,1):
                changed=dict(selected)
                if driver=='growth':changed['growth']=tuple(x+side*width for x in base['assumptions']['growth'])
                else:
                    gm=base['assumptions']['gross_margin'];gm=[gm]*5 if isinstance(gm,(float,int)) else gm
                    changed['gross_margin']=tuple(x+side*mw for x in gm)
                run=calculate(changed);end=run['statements'][-1];b=base['statements'][-1]
                sensitivity.append(dict(range=label,driver=driver,side=side,operating_profit=end['operating_income'],
                    profit_change=end['operating_income']-b['operating_income'],fcff=end['fcff'],fcff_change=end['fcff']-b['fcff'],
                    per_share=run['valuation']['per_share'],value_change=run['valuation']['per_share']-base['valuation']['per_share']))
                details += [dict(range=label,driver=driver,side=side,**row) for row in run['statements']]
        for metric in ('operating_profit','fcff','per_share'):
            spans={d:max(x[metric] for x in sensitivity if x['range']==label and x['driver']==d)-min(x[metric] for x in sensitivity if x['range']==label and x['driver']==d) for d in ('growth','gross_margin')}
            rankings.append(dict(range=label,metric=metric,spans=spans,ranking=sorted(spans,key=spans.get,reverse=True)))
    if calculate(selected)!=base:raise AssertionError('Dated restored baseline differs')
    table=[dict(wacc=w,g=g,per_share=calculate(selected,wacc=w,terminal_growth=g)['valuation']['per_share']) for w in (.09,base['valuation']['wacc'],.11) for g in (.02,.025,.03)]
    lo,hi=-.02,.35
    def reverse_at(shift):
        future=calculate(dict(selected,growth=tuple(x+shift for x in base['assumptions']['growth']),buyback=0.))
        # Freeze the base July31 bridge; changing future distributions cannot rewrite elapsed cash.
        return (future['valuation']['enterprise_value']+base['valuation']['surplus_assets']-base['valuation']['debt'])/base['valuation']['shares']
    if not reverse_at(lo)<=PRICE<=reverse_at(hi):raise ValueError('Dated reverse target not bracketed')
    for _ in range(70):
        mid=(lo+hi)/2
        if reverse_at(mid)<PRICE:lo=mid
        else:hi=mid
    shift=(lo+hi)/2
    peer_rows,implied=peers()
    return dict(as_of=str(AS_OF),evidence_cutoff='2026-07-31 end of day, 17:00 EDT; market reference is 16:00 regular-session close',
        wacc_components=dict(risk_free=RISK_FREE,risk_free_date='2026-07-30',risk_free_source='FRED DGS10 / Federal Reserve H.15',beta=BETA,erp=ERP,cost_of_equity=COST_EQUITY,pretax_debt_cost=.05,shield_tax=.21,definitions='Beta, ERP and marginal debt cost are analyst assumptions; gross book debt weight uses July31 close and latest reported basic shares/debt'),
        decision='Watch/defer; no position. Do not initiate at the dated price on these assumptions.',
        market_price=PRICE,entry_threshold=.8*base['valuation']['per_share'],units='USD millions; million shares; USD/share; annual rate decimals',
        definition='June27 reported opening → forecast FY26 Q4 → estimated July31 bridge → remaining FY26 stub plus five full fiscal years FY2027–2031; end-of-period discounting.',
        limitations='Analyst estimates between reporting dates; linear within-quarter cash-flow timing; diluted claim proxy; assumed beta/ERP/marginal debt cost, flat refinancing and noncurrent operating liabilities; one admitted platform peer. This is a July31 decision, not an October19 recommendation.',
        reversal_trigger=analysis.TRIGGERS,base=base,cases=cases,sensitivity=sensitivity,sensitivity_statements=details,
        rankings=rankings,wacc_growth=table,comparables=peer_rows,peer_implied=implied,
        reverse_dcf=dict(target=PRICE,shift=shift,implied_growth=[x+shift for x in base['assumptions']['growth']],repriced=reverse_at(shift),
            held_fixed='Q4 stub and July31 bridge estimates; selected margins/tax/reinvestment/working-capital ratios; WACC; terminal g; diluted shares. Buybacks zero throughout solve (financing only).'),
        restored_base_equal=True,failure_demo=demo_failure())


def demo_failure():
    base=calculate();bad=copy.deepcopy(base['statements'])
    bad[0]['cash']+=1000.
    opening=dict(base['stub'],revenue=364357.+(416161.-313695.)*(1+base['q4_growth']))
    try:
        model.assert_balanced(bad,base['assumptions'],opening_balance=opening,years=tuple(range(2027,2032)))
    except ValueError as error:
        model.assert_balanced(base['statements'],base['assumptions'],opening_balance=opening,years=tuple(range(2027,2032)))
        return dict(label='DEMONSTRATION ONLY — separate in-memory copy',caught=str(error),recovered=True)
    raise AssertionError('Dated corruption not caught')


def main():
    result=run_analysis();out=ROOT/'outputs/dated';out.mkdir(parents=True,exist_ok=True)
    contract=json.dumps(result,indent=2,allow_nan=False)+'\n'
    (out/'visible_output.json').write_text(contract)
    (ROOT/'outputs/visible_output.json').write_text(contract)
    old=analysis.OUT;analysis.OUT=out
    try:
        analysis.write_csv('forecast.csv',result['base']['statements'])
        analysis.write_csv('checks.csv',result['base']['checks'])
        analysis.write_csv('bridge_reported_vs_estimated.csv',[dict(field=k,reported_june27=v,estimated_july31=result['base']['estimated_date_balance'].get(k,v)) for k,v in REPORTED.items() if k!='revenue'])
        analysis.write_csv('scenarios.csv',[dict(case=k,**v['valuation']) for k,v in result['cases'].items()])
        analysis.write_csv('scenario_statements.csv',[dict(case=k,**row) for k,c in result['cases'].items() for row in c['statements']])
        analysis.write_csv('sensitivity.csv',result['sensitivity']);analysis.write_csv('sensitivity_statements.csv',result['sensitivity_statements'])
        analysis.write_csv('sensitivity_deltas.csv',[dict(range=x['range'],driver=x['driver'],side=x['side'],year=x['year'],**{k:x[k]-result['base']['statements'][x['year']-2027][k] for k in result['base']['statements'][0] if k!='year'}) for x in result['sensitivity_statements']])
        analysis.write_csv('stub_forecast.csv',[dict(case=k,**c['stub']) for k,c in result['cases'].items()])
        analysis.write_csv('scenario_implied_q4.csv',[dict(case=k,q4_revenue=c['stub']['revenue'],q4_yoy_growth=c['q4_growth'],q4_margin=c['q4_margin'],annual_revenue=364357.+c['stub']['revenue']) for k,c in result['cases'].items()])
        analysis.write_csv('timing_cashflows.csv',[dict(period='remaining FY26 stub' if i==0 else str(2026+i),time=t,fcff=cf,pv=pv) for i,(t,cf,pv) in enumerate(zip(result['base']['valuation']['discount_times'],result['base']['valuation']['fcff'],result['base']['valuation']['present_values']))])
        analysis.write_csv('wacc_growth.csv',result['wacc_growth']);analysis.write_csv('comparables.csv',result['comparables'])
        analysis.write_csv('peer_implied.csv',[result['peer_implied']])
    finally:analysis.OUT=old
    for f in out.glob('*.csv'):
        target=ROOT/'outputs'/f.name;temp=target.with_suffix('.csv.new')
        temp.write_bytes(f.read_bytes());temp.replace(target)
    for folder in (out,ROOT/'outputs'):
        target=folder/'failure_demo.json';temp=target.with_suffix('.json.new')
        temp.write_text(json.dumps(result['failure_demo'],indent=2));temp.replace(target)
    print({k:round(v['valuation']['per_share'],2) for k,v in result['cases'].items()})

if __name__=='__main__':main()
