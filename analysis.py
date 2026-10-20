"""Apple annual-base FCFF workbench. Standard library only; no network at run time."""
import copy
import csv
import json
import math
from pathlib import Path
import apple_proforma as model

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'outputs' / 'retrospective'
BASE = dict(shares=14773.260)  # FY2025 period-end common shares, millions; SBC cash-equivalent policy.
WACC_INPUTS = dict(risk_free=.04, beta=1.10, equity_risk_premium=.055,
                   pretax_debt_cost=.05, shield_tax=.21, debt_weight=.03)
COST_EQUITY = WACC_INPUTS['risk_free'] + WACC_INPUTS['beta'] * WACC_INPUTS['equity_risk_premium']
WACC = ((1 - WACC_INPUTS['debt_weight']) * COST_EQUITY + WACC_INPUTS['debt_weight']
        * WACC_INPUTS['pretax_debt_cost'] * (1 - WACC_INPUTS['shield_tax']))
G = .025
LIMITATION = ('Retrospective annual-base illustration at 2025-09-27; evidence through 2026-07-30, '
              'retrieved 2026-10-19 local. Not a contemporaneous October 2026 valuation or price target. '
              'No supported current market comparison; refresh before any trade.')
TRIGGERS = ('Rebuild on next filing; challenge growth if two successive quarters grow below 6% YoY; '
            'challenge margin if two successive quarters excluding identifiable refunds fall below 47%; '
            'reassess capex if trailing capex/revenue exceeds 4%; suspend conclusions on any failed check. '
            'Consider initiation only after a dated refresh, peer review and price at least 20% below refreshed base value.')


def discounted(flows, wacc, growth):
    """Signed year-end flows; continuing cash flow grows from the final year."""
    if not all(math.isfinite(x) for x in [*flows, wacc, growth]):
        raise ValueError('Nonfinite DCF input')
    if len(flows) != 5 or not 0 <= growth < wacc or wacc > 1:
        raise ValueError('Require five flows and 0 <= terminal growth < WACC <= 100%')
    if flows[-1] <= 0:
        raise ValueError('Nonpositive terminal FCFF: no supported positive perpetuity')
    pvs = [cf / (1 + wacc) ** t for t, cf in enumerate(flows, 1)]
    terminal_flow = flows[-1] * (1 + growth)
    terminal_value = terminal_flow / (wacc - growth)
    terminal_pv = terminal_value / (1 + wacc) ** 5
    return dict(present_values=pvs, explicit_pv=sum(pvs), terminal_fcff=terminal_flow,
                terminal_value=terminal_value, terminal_pv=terminal_pv,
                enterprise_value=sum(pvs) + terminal_pv,
                terminal_share=terminal_pv / (sum(pvs) + terminal_pv))


def calculate(overrides=None, wacc=WACC, growth=G):
    a = dict(BASE)
    a.update(overrides or {})
    if not math.isfinite(a['shares']) or a['shares'] <= 0:
        raise ValueError('Share count must be finite and positive')
    rows = model.project(a)
    model.assert_balanced(rows, a)
    tax = model.parameters(a)['tax_rate']
    for r in rows:
        r['nopat'] = r['operating_income'] * (1 - tax)
        r['operating_da'] = r['depreciation'] + r['other_da']
        r['fcff'] = (r['nopat'] + r['operating_da'] - r['capex']
                     - r['other_reinvestment'] - r['change_nwc'])
        # Exact reconciliation even if the model has no tax benefit on a loss.
        r['fcff_cash_route'] = r['cfo'] + r['cfi'] + r['nopat'] - r['net_income']
        if abs(r['fcff'] - r['fcff_cash_route']) > model.TOLERANCE:
            raise ValueError('FCFF routes disagree')
    value = discounted([r['fcff'] for r in rows], wacc, growth)
    surplus = model.OPENING['securities'] + max(0., model.OPENING['cash'] - model.parameters(a)['min_cash'])
    debt = model.OPENING['commercial_paper'] + model.OPENING['debt']
    equity = value['enterprise_value'] + surplus - debt
    reinvestment_rate = (rows[-1]['nopat'] - rows[-1]['fcff']) / rows[-1]['nopat']
    value.update(terminal_reinvestment_rate=reinvestment_rate,
                 terminal_implied_roic=growth/reinvestment_rate if reinvestment_rate > 0 else None,
                 surplus_assets=surplus, debt=debt, other_claims=0., equity_value=equity,
                 shares=a['shares'], per_share=equity / a['shares'], wacc=wacc, terminal_growth=growth)
    if abs(value['equity_value'] - value['enterprise_value'] - surplus + debt) > 1e-6:
        raise ValueError('Enterprise-equity bridge fails')
    return dict(assumptions=model.parameters(a), statements=rows, checks=model.check_rows(rows, a), valuation=value)


def compare_to_base(changed, base):
    return dict(value_change=changed['valuation']['per_share'] - base['valuation']['per_share'])


def demo_failure():
    """Corrupt only an in-memory copy; invoke the real valuation gate; recover."""
    a = dict(BASE)
    good = model.project(a)
    bad = copy.deepcopy(good)
    bad[0]['cash'] += 1000
    try:
        model.assert_balanced(bad, a)
    except ValueError as error:
        model.assert_balanced(good, a)
        return dict(label='DEMONSTRATION ONLY — separate copy, never exported as valid statements',
                    change='FY2026 cash +1,000 USD million without a cash-flow entry',
                    caught=str(error), recovered=True)
    raise AssertionError('Corruption escaped the real check')


def reverse_dcf(target=255.46, baseline=None):
    """Historical dated price diagnostic, not a current market-implied forecast."""
    lo, hi = -.02, .30
    selected = model.parameters(dict(BASE, **(baseline or {})))
    def at(shift):
        changed = dict(selected, growth=tuple(x + shift for x in selected['growth']), buyback=0.)
        return calculate(changed)['valuation']['per_share']
    if not at(lo) <= target <= at(hi):
        raise ValueError('Target outside bracket; no solution claimed')
    for _ in range(80):
        mid = (lo + hi) / 2
        if at(mid) < target: lo = mid
        else: hi = mid
    shift = (lo + hi) / 2
    return dict(target=target, quote_date='2025-09-26 close; Yahoo historical unadjusted close, secondary source',
                valuation_date='2025-09-27 annual base, retrospective', shift=shift,
                implied_growth=[x + shift for x in selected['growth']], baseline_assumptions=selected, repriced=at(shift),
                held_fixed='Selected baseline assumptions above, except uniform growth shift and buybacks=0; '
                'WACC; 2.5% g; FY25 surplus/debt/shares; year-end timing. Buybacks zero in entire solve '
                '(financing only). Evidence cutoff later than target date: not a point-in-time backtest.')


def comparable(row):
    """Historical diagnostic: GAAP income, operating leases left operating."""
    for key in ('price','shares','ebit','net_income'):
        if not math.isfinite(row[key]) or row[key] <= 0: raise ValueError('Invalid multiple denominator or market input')
    equity = row['price'] * row['shares']
    ev = equity + row['debt'] - row['cash_securities']
    return dict(row, market_equity=equity, enterprise_value=ev,
                ev_ebit=ev / row['ebit'], pe=equity / row['net_income'])


def comparables():
    # Policy written in docs/peer_policy.md before this computation.
    inputs = [dict(ticker='AAPL',price=255.46,shares=14773.260,ebit=133050.,net_income=112010.,
                   debt=98657.,cash_securities=132420.,fiscal_end='2025-09-27',share_date='2025-09-27'),
              dict(ticker='MSFT',price=511.46,shares=7434.,ebit=128528.,net_income=101832.,
                   debt=43151.,cash_securities=94565.,fiscal_end='2025-06-30',share_date='2025-06-30')]
    return [comparable(dict(r,price_date='2025-09-26',status='Historical diagnostic; period/share lags; not admitted current peer estimate')) for r in inputs]


def sensitivities(base):
    rows=[]; detail=[]
    selected = base['assumptions']
    for label, shift, margin_width in [('supplied',.02,.02),('alternative',.01,.04)]:
        for driver in ('growth','gross_margin'):
            for direction in (-1,1):
                overrides = dict(selected)
                if driver == 'growth':
                    overrides['growth'] = tuple(x + direction*shift for x in selected['growth'])
                else:
                    gm = selected['gross_margin']
                    overrides['gross_margin'] = (tuple(x + direction*margin_width for x in gm)
                        if isinstance(gm, (list, tuple)) else gm + direction*margin_width)
                changed=calculate(overrides)
                r,b=changed['statements'][-1],base['statements'][-1]
                record=dict(range=label,driver=driver,side='low' if direction<0 else 'high',
                            input=json.dumps(overrides),operating_profit=r['operating_income'],
                            profit_change=r['operating_income']-b['operating_income'],fcff=r['fcff'],
                            fcff_change=r['fcff']-b['fcff'],per_share=changed['valuation']['per_share'],
                            value_change=changed['valuation']['per_share']-base['valuation']['per_share'])
                rows.append(record)
                detail += [dict(range=label,driver=driver,side=record['side'],**s) for s in changed['statements']]
    restored=calculate(selected)
    if restored != base: raise AssertionError('Restored base differs')
    ranks=[]
    for label in ('supplied','alternative'):
        for metric in ('operating_profit','fcff','per_share'):
            spans={d:max(r[metric] for r in rows if r['range']==label and r['driver']==d)-min(r[metric] for r in rows if r['range']==label and r['driver']==d) for d in ('growth','gross_margin')}
            ranks.append(dict(range=label,metric=metric,ranking=sorted(spans,key=spans.get,reverse=True),spans=spans))
    return rows, detail, ranks


def run_analysis(inputs=None):
    base=calculate(inputs)
    selected=base['assumptions']
    cases={
        'low':calculate(dict(selected, growth=(.12,0.,.02,.02,.02),gross_margin=(.47,.44,.44,.44,.44),rd_ratio=.105,capex_ratio=.04,buyback=0.),.11,.02),
        'base':base,
        'high':calculate(dict(selected, growth=(.17,.10,.08,.07,.06),gross_margin=(.50,.51,.51,.51,.51)),.09,.03)}
    sens,details,ranks=sensitivities(cases['base'])
    table=[dict(wacc=w,g=g,per_share=calculate(selected,wacc=w,growth=g)['valuation']['per_share'])
           for w in (.09,WACC,.11) for g in (.02,.025,.03)]
    return dict(decision='Watch/defer — no current position; authorize refresh research, no trade',
                as_of='2025-09-27 annual-base illustration; prepared 2026-10-19 America/Indiana/Indianapolis',
                evidence_cutoff='2026-07-30',units='USD millions; shares millions; USD/share; rates decimals',
                recommendation='Annual-base scenario range only; current initiation assessment deferred pending refresh',
                reversal_trigger=TRIGGERS,limitations=LIMITATION,wacc_inputs=WACC_INPUTS,cost_of_equity=COST_EQUITY,
                baseline_policy='inputs define the selected base; all OAT shocks are relative to it; named causal cases override declared operating paths but inherit other selected assumptions',
                base=base,cases=cases,sensitivity=sens,sensitivity_statements=details,rankings=ranks,
                wacc_growth=table,reverse_dcf=reverse_dcf(baseline=selected),comparables=comparables(),failure_demo=demo_failure(),
                implied_q4=[dict(case=k,revenue=v['statements'][0]['revenue']-364357,
                    yoy_growth=(v['statements'][0]['revenue']-364357)/(416161-313695)-1,
                    gross_margin=(v['statements'][0]['gross_profit']-178782)/(v['statements'][0]['revenue']-364357))
                    for k,v in cases.items()],
                restored_base_equal=True,normalization=[
                    dict(year=2024,reported_tax=29749,aid_tax_adjustment=10246,normalized_tax=29749-10246,
                         reported_net_income=93736,normalized_net_income=93736+10246),
                    dict(year=2025,reported_tax=20719,aid_tax_adjustment=-486,normalized_tax=20719+486,
                         reported_net_income=112010,normalized_net_income=112010-486)])


def write_csv(name, rows):
    with (OUT/name).open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)


def main():
    result=run_analysis();OUT.mkdir(parents=True,exist_ok=True)
    # Export only after all calculation gates and restoration have succeeded.
    (OUT/'visible_output.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    write_csv('forecast.csv',result['base']['statements'])
    write_csv('history_normalization.csv',result['normalization'])
    write_csv('checks.csv',result['base']['checks'])
    write_csv('scenario_implied_q4.csv',result['implied_q4'])
    write_csv('scenarios.csv',[dict(case=k,**v['valuation']) for k,v in result['cases'].items()])
    write_csv('scenario_statements.csv',[dict(case=k,**r) for k,v in result['cases'].items() for r in v['statements']])
    write_csv('sensitivity.csv',result['sensitivity']);write_csv('sensitivity_statements.csv',result['sensitivity_statements'])
    write_csv('sensitivity_deltas.csv',[dict(range=r['range'],driver=r['driver'],side=r['side'],year=r['year'],
        **{k:r[k]-result['cases']['base']['statements'][r['year']-2026][k] for k in result['cases']['base']['statements'][0] if k!='year'}) for r in result['sensitivity_statements']])
    write_csv('wacc_growth.csv',result['wacc_growth']);write_csv('comparables.csv',result['comparables'])
    (OUT/'failure_demo.json').write_text(json.dumps(result['failure_demo'],indent=2))
    v=result['base']['valuation']; low=result['cases']['low']['valuation']['per_share']; high=result['cases']['high']['valuation']['per_share']
    text=f'''# Apple valuation summary — executed annual-base FCFF

{result['decision']}. {LIMITATION}

Annual-base low/base/high: **${low:.2f} / ${v['per_share']:.2f} / ${high:.2f} per share**. Scenario range is not a probability interval or current price target.

Base WACC {WACC:.4%}; terminal growth {G:.2%}; enterprise value {v['enterprise_value']:,.2f}; explicit PV {v['explicit_pv']:,.2f}; terminal PV {v['terminal_pv']:,.2f}; terminal share of EV {v['terminal_share']:.2%}. All dollar totals USD millions.

Bridge: EV + {v['surplus_assets']:,.0f} opening surplus assets - {v['debt']:,.0f} debt - 0 additional claims = {v['equity_value']:,.2f} equity / {v['shares']:,.3f} period-end common shares (millions). Terminal reinvestment/NOPAT is {v['terminal_reinvestment_rate']:.2%}; growth divided by that rate implies incremental ROIC {v['terminal_implied_roic']:.2%}, a demanding unverified continuing-efficiency assumption. No future cash balance is added. Operating cash retained: 30,000; other liabilities treated as operating with rent/taxes embedded in forecast. This aggregation limits claim completeness; review before trading.

FCFF = EBIT × (1 − 18%) + PP&E depreciation + other D&A − PP&E capex − other reinvestment − increase in operating NWC. Other reinvestment equals other D&A. Cash route = CFO + CFI + NOPAT − net income (equals after-tax interest addback with positive taxable income). Dividends, buybacks and debt repayment are excluded. Annual cash flows arrive at ends of FY2026–2030, discounted 1–5 periods to FY2025 end. Terminal FCFF = FY2030 FCFF × 1.025; continuing reinvestment/cash-conversion ratios assumed stable, not separately forecast FY2031.

SBC remains an operating expense, without addback or future issuance; shares held fixed. Repurchases are treasury distributions, not a forecast of per-share accretion. Per-share values use period-end basic common shares under this cash-equivalent compensation assumption, not EPS diluted weighted-average shares. Outstanding awards need a refreshed fully diluted claim assessment before trading.

{TRIGGERS}

See docs/source_ledger.csv, docs/assumption_challenges.csv, outputs/sensitivity.csv, outputs/visible_output.json and docs/validation-and-ai-use.md. The earlier $127.62 FCFE and $224 proxy results are separate methods, not endpoints. Comparables are historical diagnostics with fiscal/share lags; no current peer target is inferred or averaged with DCF.
'''
    (OUT/'valuation_summary.md').write_text(text)
    print(text)

if __name__=='__main__':main()
