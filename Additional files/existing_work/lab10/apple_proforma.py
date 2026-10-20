"""FIN43900 Lab 10: Apple five-year pro-forma, USD millions.

Run: python3 apple_proforma.py
Save tables: python3 apple_proforma.py --write
Standard library only. Sources and assumption labels are in Lab_10_Apple.md.
This is an educational annual-base model, not a live investment recommendation.
"""
import argparse
import csv
import math
from pathlib import Path

YEARS = (2026, 2027, 2028, 2029, 2030)
TOLERANCE = 1e-6  # USD millions; checks use unrounded amounts.
HISTORY = {
    2023: dict(revenue=383285, gross_profit=169148, sga=24932, rd=29915,
               net_income=96995, pretax=113736, tax=16741, inventory=6331,
               ppe=43715, equity=62146, depreciation=8500, da=11519,
               capex=10959, vendor_receivables=31477),
    2024: dict(revenue=391035, gross_profit=180683, sga=26097, rd=31370,
               net_income=93736, pretax=123485, tax=29749, inventory=7286,
               ppe=45680, equity=56950, depreciation=8200, da=11445,
               capex=9447, vendor_receivables=32833),
    2025: dict(revenue=416161, gross_profit=195201, sga=27601, rd=34550,
               net_income=112010, pretax=132729, tax=20719, inventory=5718,
               ppe=49834, equity=73733, depreciation=8000, da=11698,
               capex=12715, vendor_receivables=33180),
}
OPENING = dict(revenue=416161., cash=35934., securities=96486.,
               receivables=39777., vendor_receivables=33180., inventory=5718.,
               other_current_assets=14585., ppe=49834., other_assets=83727.,
               payables=69860., deferred_revenue=9055., other_liabilities=107936.,
               commercial_paper=7979., debt=90678., revolver=0., equity=73733.)

# History: exact FY2025 ratios carried forward, following the lab convention.
# Forward stability is an assumption even where the lab calls the input history.
H = HISTORY[2025]
COGS_2025 = H['revenue'] - H['gross_profit']
DEFAULTS = dict(
    growth=(.15, .08, .06, .05, .04),             # J1 judgment
    gross_margin=.49,                           # J2 judgment
    sga_ratio=H['sga'] / H['gross_profit'],       # history
    rd_ratio=.095,                              # J3 judgment
    depreciation_ratio=8000 / 49834,             # history, PP&E only
    other_da_ratio=(11698 - 8000) / 416161,       # history, residual D&A proxy
    capex_ratio=.03,                            # J4 judgment
    tax_rate=.18,                               # J5 judgment
    inventory_days=5718 / COGS_2025 * 365,       # history, ending balances
    receivables_ratio=39777 / 416161,             # history
    vendor_ratio=33180 / COGS_2025,               # history, company-specific line
    other_current_assets_ratio=14585 / 416161,  # history
    payables_ratio=69860 / COGS_2025,             # history
    deferred_revenue_ratio=9055 / 416161,        # history
    repayments=(12393., 10078., 9300., 5235., 4972.),  # J6; filing maturities
    debt_rate=.03, cp_rate=.035,                 # J7 judgment, not quoted rates
    buyback=75000., dividend=16000.,             # J8 judgment, annual dollars
    min_cash=30000., revolver_limit=0., revolver_rate=.06,  # J9
    cost_of_equity=.10, terminal_growth=.025,    # J10, J11 judgments
    shares=14594.180,                           # history: Q3 2026 cover, millions
)
# J12: other non-current assets/liabilities and securities held flat; other D&A
# is matched by reinvestment. J13: future SBC treated as cash compensation; no
# SBC addback or share issuance. Buybacks are distributions, not FCFE expense.
# J14: zero interest income, other gains, OCI and incremental impairment.
# J15: terminal debt refinanced; repayment stops, interest continues.
# J16: securities + opening cash above floor added once to equity value.
MARKET_PRICE = 337.01
MARKET_TIMESTAMP = '2026-09-24 15:03 EDT (intraday snapshot)'
MARKET_URL = 'https://stockanalysis.com/stocks/aapl/financials/cash-flow-statement/'

ASSET_KEYS = ('cash', 'securities', 'receivables', 'vendor_receivables',
              'inventory', 'other_current_assets', 'ppe', 'other_assets')
LIABILITY_KEYS = ('payables', 'deferred_revenue', 'other_liabilities',
                  'commercial_paper', 'debt', 'revolver')
WC_ASSETS = ('receivables', 'vendor_receivables', 'inventory', 'other_current_assets')
WC_LIABILITIES = ('payables', 'deferred_revenue')


def balance_gap(row):
    return sum(row[k] for k in ASSET_KEYS) - sum(row[k] for k in LIABILITY_KEYS) - row['equity']


def parameters(overrides=None):
    a = DEFAULTS.copy()
    if overrides:
        a.update(overrides)
    if len(a['growth']) != 5 or len(a['repayments']) != 5:
        raise ValueError('Exactly five growth rates and repayments are required')
    if not 0 <= a['terminal_growth'] < a['cost_of_equity']:
        raise ValueError('Terminal growth must be nonnegative and below cost of equity')
    if a['shares'] <= 0 or a['revolver_limit'] < 0:
        raise ValueError('Share count must be positive and revolver limit nonnegative')
    if not 0 <= a['tax_rate'] <= 1 or not 0 < a['gross_margin'] < 1:
        raise ValueError('Tax rate or gross margin outside its valid range')
    if any(g <= -1 for g in a['growth']):
        raise ValueError('Revenue growth must exceed -100%')
    return a


def project(overrides=None):
    a = parameters(overrides)
    if abs(balance_gap(OPENING)) > TOLERANCE:
        raise ValueError(f'FY2025 opening balance gap: {balance_gap(OPENING)}')
    opening = OPENING.copy()
    results = []
    for year, growth, repayment in zip(YEARS, a['growth'], a['repayments']):
        r = dict(year=year)
        r['revenue'] = opening['revenue'] * (1 + growth)
        r['gross_profit'] = r['revenue'] * a['gross_margin']
        r['cost_of_sales'] = r['revenue'] - r['gross_profit']
        r['sga'] = r['gross_profit'] * a['sga_ratio']
        r['rd'] = r['revenue'] * a['rd_ratio']
        # D&A is already embedded in gross margin and expense ratios.
        r['operating_income'] = r['gross_profit'] - r['sga'] - r['rd']
        r['depreciation'] = opening['ppe'] * a['depreciation_ratio']
        r['other_da'] = r['revenue'] * a['other_da_ratio']
        r['interest'] = (opening['debt'] * a['debt_rate']
                         + opening['commercial_paper'] * a['cp_rate']
                         + opening['revolver'] * a['revolver_rate'])
        r['pretax'] = r['operating_income'] - r['interest']
        r['tax'] = max(0., r['pretax']) * a['tax_rate']
        r['net_income'] = r['pretax'] - r['tax']
        r['receivables'] = r['revenue'] * a['receivables_ratio']
        r['vendor_receivables'] = r['cost_of_sales'] * a['vendor_ratio']
        r['inventory'] = r['cost_of_sales'] * a['inventory_days'] / 365
        r['other_current_assets'] = r['revenue'] * a['other_current_assets_ratio']
        r['payables'] = r['cost_of_sales'] * a['payables_ratio']
        r['deferred_revenue'] = r['revenue'] * a['deferred_revenue_ratio']
        r['capex'] = r['revenue'] * a['capex_ratio']
        r['ppe'] = opening['ppe'] + r['capex'] - r['depreciation']
        r['other_reinvestment'] = r['other_da']
        r['other_assets'] = opening['other_assets'] + r['other_reinvestment'] - r['other_da']
        for key in ('securities', 'other_liabilities', 'commercial_paper'):
            r[key] = opening[key]
        if repayment < 0 or repayment > opening['debt']:
            raise ValueError(f'FY{year}: repayment exceeds debt or is negative')
        r['repayment'] = repayment
        r['debt'] = opening['debt'] - repayment
        r['buyback'], r['dividend'] = a['buyback'], a['dividend']
        r['equity'] = opening['equity'] + r['net_income'] - r['buyback'] - r['dividend']
        for key in WC_ASSETS + WC_LIABILITIES:
            r['change_' + key] = r[key] - opening[key]
        r['change_nwc'] = (sum(r['change_' + k] for k in WC_ASSETS)
                           - sum(r['change_' + k] for k in WC_LIABILITIES))
        r['cfo'] = r['net_income'] + r['depreciation'] + r['other_da'] - r['change_nwc']
        r['cfi'] = -r['capex'] - r['other_reinvestment']
        r['fcfe'] = r['cfo'] + r['cfi'] - repayment
        cash_before_revolver = opening['cash'] + r['fcfe'] - r['buyback'] - r['dividend']
        if cash_before_revolver < a['min_cash']:
            r['revolver_change'] = min(a['min_cash'] - cash_before_revolver,
                                         a['revolver_limit'] - opening['revolver'])
        else:
            r['revolver_change'] = -min(opening['revolver'], cash_before_revolver - a['min_cash'])
        r['revolver'] = opening['revolver'] + r['revolver_change']
        r['cff'] = -repayment - r['buyback'] - r['dividend'] + r['revolver_change']
        r['cash_change'] = r['cfo'] + r['cfi'] + r['cff']
        r['opening_cash'] = opening['cash']
        r['cash'] = opening['cash'] + r['cash_change']  # cash computed last, never plugged
        r['assets'] = sum(r[k] for k in ASSET_KEYS)
        r['liabilities'] = sum(r[k] for k in LIABILITY_KEYS)
        results.append(r)
        opening = r
    return results


def check_rows(results, overrides=None):
    """Recompute checks from actual lines; never trust a stored gap or total."""
    a = parameters(overrides)
    opening = OPENING
    checks = []
    for r in results:
        expected_cfo = (r['net_income'] + r['depreciation'] + r['other_da']
                        - sum(r[k] - opening[k] for k in WC_ASSETS)
                        + sum(r[k] - opening[k] for k in WC_LIABILITIES))
        checks.append(dict(year=r['year'], balance=balance_gap(r),
            cash=r['cash'] - opening['cash'] - r['cfo'] - r['cfi'] - r['cff'],
            cfo=r['cfo'] - expected_cfo,
            cfi=r['cfi'] + r['capex'] + r['other_reinvestment'],
            cff=r['cff'] + r['repayment'] + r['buyback'] + r['dividend'] - r['revolver_change'],
            ppe=r['ppe'] - opening['ppe'] - r['capex'] + r['depreciation'],
            other_assets=r['other_assets'] - opening['other_assets'] - r['other_reinvestment'] + r['other_da'],
            debt=r['debt'] - opening['debt'] + r['repayment'],
            equity=r['equity'] - opening['equity'] - r['net_income'] + r['buyback'] + r['dividend'],
            revolver=r['revolver'] - opening['revolver'] - r['revolver_change'],
            fcfe=r['fcfe'] - r['cfo'] - r['cfi'] + r['repayment'],
            asset_total=r['assets'] - sum(r[k] for k in ASSET_KEYS),
            liability_total=r['liabilities'] - sum(r[k] for k in LIABILITY_KEYS),
            cash_floor_shortfall=max(0., a['min_cash'] - r['cash'])))
        opening = r
    return checks


def assert_balanced(results, overrides=None):
    a = parameters(overrides)
    if tuple(r['year'] for r in results) != YEARS:
        raise ValueError('All five forecast years must be present and ordered')
    for r in results:
        for key, value in r.items():
            if not math.isfinite(value):
                raise ValueError(f'FY{r["year"]}: {key} is not finite')
        for key in ASSET_KEYS + LIABILITY_KEYS:
            if r[key] < -TOLERANCE:
                raise ValueError(f'FY{r["year"]}: negative {key}: {r[key]:.6f}')
        if r['revolver'] > a['revolver_limit'] + TOLERANCE:
            raise ValueError(f'FY{r["year"]}: revolver limit exceeded')
    for c in check_rows(results, a):
        for name, gap in c.items():
            if name != 'year' and abs(gap) > TOLERANCE:
                raise ValueError(f'FY{c["year"]}: {name} gap = {gap:.6f} million; valuation refused')


def value_equity(results, overrides=None):
    a = parameters(overrides)
    assert_balanced(results, a)  # mandatory, before any valuation
    if any(abs(r['revolver']) > TOLERANCE for r in results):
        raise ValueError('Valuation with revolver financing requires a revised financing policy')
    # Lab convention for a negative FCFE year: retain it in statements, value only positives.
    pv_fcfe = sum(max(0., r['fcfe']) / (1 + a['cost_of_equity']) ** t
                  for t, r in enumerate(results, 1))
    last = results[-1]
    if last['fcfe'] <= 0:
        raise ValueError('Terminal-year FCFE is nonpositive; no positive perpetuity assumed')
    # At the terminal date interest resets to closing, not opening, debt.
    interest_saving = last['repayment'] * a['debt_rate'] * (1 - a['tax_rate'])
    terminal_fcfe = (last['fcfe'] + last['repayment'] + interest_saving) * (1 + a['terminal_growth'])
    pv_terminal = terminal_fcfe / (a['cost_of_equity'] - a['terminal_growth']) / (1 + a['cost_of_equity']) ** 5
    surplus_assets = OPENING['securities'] + max(0., OPENING['cash'] - a['min_cash'])
    course_equity = pv_fcfe + pv_terminal
    total_equity = course_equity + surplus_assets
    return dict(pv_fcfe=pv_fcfe, pv_terminal=pv_terminal, surplus_assets=surplus_assets,
                course_equity=course_equity, equity_value=total_equity,
                course_per_share=course_equity / a['shares'],
                per_share=total_equity / a['shares'],
                terminal_share=pv_terminal / total_equity, terminal_fcfe=terminal_fcfe)


TABLES = [
    ('Income statement', [('Revenue', 'revenue'), ('Cost of sales', 'cost_of_sales'),
      ('Gross profit', 'gross_profit'), ('SG&A', 'sga'), ('R&D', 'rd'),
      ('Operating income', 'operating_income'), ('Interest expense', 'interest'),
      ('Pretax income', 'pretax'), ('Income tax', 'tax'), ('Net income', 'net_income')]),
    ('Balance sheet', [('Cash', 'cash'), ('Marketable securities', 'securities'),
      ('Trade receivables', 'receivables'), ('Vendor non-trade receivables', 'vendor_receivables'),
      ('Inventory', 'inventory'), ('Other current assets', 'other_current_assets'),
      ('Net PP&E', 'ppe'), ('Other non-current assets', 'other_assets'), ('Total assets', 'assets'),
      ('Accounts payable', 'payables'), ('Deferred revenue', 'deferred_revenue'),
      ('Other liabilities', 'other_liabilities'), ('Commercial paper', 'commercial_paper'),
      ('Term debt', 'debt'), ('Revolver', 'revolver'), ('Total liabilities', 'liabilities'),
      ('Shareholders equity', 'equity')]),
    ('Cash flow', [('Net income', 'net_income'), ('PP&E depreciation addback', 'depreciation'),
      ('Other D&A addback', 'other_da'), ('Increase in net working capital (use)', 'change_nwc'),
      ('Of which vendor receivables increase', 'change_vendor_receivables'),
      ('Operating cash flow', 'cfo'), ('PP&E capex (outflow)', 'capex'),
      ('Other asset reinvestment (outflow)', 'other_reinvestment'), ('Investing cash flow', 'cfi'),
      ('Debt repayment (outflow)', 'repayment'), ('FCFE before distributions', 'fcfe'),
      ('Buybacks (outflow)', 'buyback'), ('Dividends (outflow)', 'dividend'),
      ('Revolver draw / repayment', 'revolver_change'), ('Financing cash flow', 'cff'),
      ('Net change in cash', 'cash_change'), ('Opening cash', 'opening_cash'), ('Closing cash', 'cash')]),
]


def render(results):
    value = value_equity(results)
    lines = ['# Apple Lab 10 - generated model results', '',
             'USD millions except per-share values. Expense and outflow detail is shown as positive magnitudes;',
             'cash-flow subtotals carry their actual signs. Full precision is retained for checks.', '']
    for title, rows in TABLES:
        lines += [f'## {title}', '', '| Line | ' + ' | '.join(f'FY{y}E' for y in YEARS) + ' |',
                  '|---|' + '---:|' * 5]
        for label, key in rows:
            lines.append('| ' + label + ' | ' + ' | '.join(f'{r[key]:,.1f}' for r in results) + ' |')
        lines.append('')
    checks = check_rows(results)
    lines += ['## Enforced checks', '', '| Check gap | ' + ' | '.join(map(str, YEARS)) + ' |', '|---|' + '---:|' * 5]
    for name in checks[0]:
        if name != 'year':
            lines.append('| ' + name + ' | ' + ' | '.join(f'{0. if abs(c[name]) < TOLERANCE else c[name]:.1f}' for c in checks) + ' |')
    lines += ['', 'All checks PASS. Cash floor: $30,000 million. No revolver draw in the base case.', '',
              '## Valuation', '', f'- PV of FY2026-FY2030 FCFE: ${value["pv_fcfe"]:,.2f} million.',
              f'- FY2031 normalized terminal FCFE: ${value["terminal_fcfe"]:,.2f} million.',
              f'- PV of terminal value: ${value["pv_terminal"]:,.2f} million.',
              f'- Course-style FCFE value before surplus assets: ${value["course_equity"]:,.2f} million (${value["course_per_share"]:.2f}/share).',
              f'- Opening surplus cash and securities added once: ${value["surplus_assets"]:,.2f} million.',
              f'- Total estimated equity value: ${value["equity_value"]:,.2f} million.',
              f'- Share count used: {DEFAULTS["shares"]:,.3f} million (July 17, 2026 filing cover).',
              f'- **Apple model value per share: ${value["per_share"]:.2f}.**',
              f'- Terminal value / total equity value: {value["terminal_share"]:.2%}.',
              f'- Market reference: ${MARKET_PRICE:.2f}, {MARKET_TIMESTAMP}. [Source]({MARKET_URL})',
              '- FCFE status: positive in every projected year.', '',
              'Timing: five full annual periods are discounted to the FY2025 opening-model date.',
              'The September 2026 quote and July 2026 share count are dated comparison inputs,',
              'not a claim that this annual-base exercise is a rolled-forward September 2026 valuation.', '']
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='Save result Markdown and CSV beside this file')
    args = parser.parse_args()
    results = project()
    output = render(results)
    print(output)
    if args.write:
        folder = Path(__file__).resolve().parent
        (folder / 'apple_results.md').write_text(output, encoding='utf-8')
        with (folder / 'apple_forecast.csv').open('w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=list(results[0]))
            writer.writeheader()
            writer.writerows(results)


if __name__ == '__main__':
    main()

