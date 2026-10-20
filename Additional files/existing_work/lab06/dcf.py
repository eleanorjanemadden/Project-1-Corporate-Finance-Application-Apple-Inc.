# EDITABLE INPUTS: USD millions; diluted shares in millions; rates as decimals.
# Source: FY26_Q3_Consolidated_Financial_Statements.pdf (Apple Inc.).

#
# FCFF is NOT reported directly. This is an annualized CFO-minus-capex PROXY:
# page 3, nine months ended June 27, 2026; multiply by 12/9 for an annual base.
# It omits an after-tax interest add-back (interest expense is not disclosed)
# and assumes the nine-month cash flows are representative of a full year.
STARTING_FCFF = (116_996 - 6_799) * 12 / 9

# PDF p. 1: nine-month revenue growth. The forecast below is our assumption,
# NOT Apple guidance: FCFF grows with revenue, fading linearly to 3% in Year 5.
# This assumes stable cash conversion; the PDF supplies no five-year forecast.
REVENUE_GROWTH = 364_357 / 313_695 - 1
TERMINAL_GROWTH = 0.03  # Analyst long-run assumption, not Apple guidance.
YEARLY_GROWTH_RATES = [
    REVENUE_GROWTH + (TERMINAL_GROWTH - REVENUE_GROWTH) * year / 4
    for year in range(5)
]  # Replace with five hand-entered rates if desired.

# Page 2, June 27, 2026: cash + current and non-current marketable securities.
# Assumption: all these balances are non-operating and available to equity.
NON_OPERATING_CASH = 39_544 + 22_855 + 84_118
# Page 2: commercial paper + current term debt + non-current term debt.
DEBT = 1_997 + 11_007 + 71_340
# Page 1: latest quarter's weighted-average diluted shares, reported in thousands.
# Convert to millions; this is a proxy for valuation-date diluted shares.
DILUTED_SHARES = 14_714_676 / 1_000


# Additional editable inputs: rates and shifts are decimals (0.01 = 1 percentage point).
SENSITIVITY_TERMINAL_GROWTH_RATES = [0.02, 0.03, 0.04]
# Dated quote snapshot from the web finance tool; no network/packages needed at run time.
MARKET_PRICE = 326.57
PRICE_AS_OF = "2026-09-10 21:09:22 UTC (latest trade returned; not a closing-price claim)"
PRICE_SOURCE = "Web finance tool, AAPL, retrieved 2026-09-10"
TARGET_SHARE_PRICE = MARKET_PRICE  # Edit to test another target; market comparison stays separate.
# PDF p. 1: quarterly operating margin; monitor its durability next quarter.
QUARTER_OPERATING_MARGIN = 35_695 / 109_417
PRIOR_QUARTER_OPERATING_MARGIN = 28_202 / 94_036  # Prior-year comparable quarter.
APPLE_RESULTS_URL = "https://www.apple.com/newsroom/2026/07/apple-reports-third-quarter-results/"
REVERSE_SHIFT_LOWER = -0.05
REVERSE_SHIFT_UPPER = 0.20  # Editable search limit; never treated as a solution by default.


# APPLE WACC INPUTS: dated observations, editable estimates; rates are decimals.
RISK_FREE_RATE = 0.0483  # Fed H.15, 10-year Treasury, Sep 9; release Sep 10, 2026.
EQUITY_BETA = 1.09  # Yahoo AAPL, 5-year monthly beta; retrieved Sep 10 (Sep 4 snapshot).
EQUITY_RISK_PREMIUM = 0.0414  # Damodaran, Sep 1, 2026, Treasury-based implied ERP.
PRETAX_COST_OF_DEBT = 0.0504  # Apple 4.75% May 2035 bond, ISIN US037833FB15.
# BondTerminal Sep 8, 2026 yield-to-worst; proxy for marginal borrowing cost,
# NOT the coupon or the weighted historical interest rate of all Apple's debt.
MARGINAL_TAX_RATE = 0.21  # FY25 10-K PDF p. 55: U.S. statutory rate.
# Assumes interest deductions at this rate; ignores state/foreign differences.
SHARES_OUTSTANDING = 14_608_963 / 1_000  # Q3 PDF p. 2, June 27, 2026; millions.
# Use outstanding common shares for equity weight, NOT weighted-average diluted EPS shares.
MARKET_EQUITY = MARKET_PRICE * SHARES_OUTSTANDING
DEBT_WEIGHT = DEBT / (MARKET_EQUITY + DEBT)  # Book debt is a market-value proxy.
COST_OF_EQUITY = RISK_FREE_RATE + EQUITY_BETA * EQUITY_RISK_PREMIUM
AFTERTAX_COST_OF_DEBT = PRETAX_COST_OF_DEBT * (1 - MARGINAL_TAX_RATE)
WACC = (1 - DEBT_WEIGHT) * COST_OF_EQUITY + DEBT_WEIGHT * AFTERTAX_COST_OF_DEBT
SENSITIVITY_WACCS = [WACC - 0.01, WACC, WACC + 0.01]  # +/- one percentage point.
WACC_SOURCES = (
    "https://www.federalreserve.gov/releases/h15/",
    "https://finance.yahoo.com/quote/AAPL/",
    "https://pages.stern.nyu.edu/~adamodar/New_Home_Page/home.htm",
    "https://bondterminal.com/issuers/apple-inc",
)


from math import isfinite


def dcf(wacc, terminal_growth, shift=0.0):
    """One calculation shared by the base case, sensitivity, and reverse DCF."""
    if not all(isfinite(x) for x in (wacc, terminal_growth, shift)):
        raise ValueError("Rates and shift must be finite.")
    if wacc <= -1 or terminal_growth >= wacc:
        raise ValueError("Require WACC > -100% and terminal growth < WACC.")
    fcff, flows = STARTING_FCFF, []
    for growth in YEARLY_GROWTH_RATES:
        fcff *= 1 + growth + shift
        flows.append(fcff)
    explicit_pv = sum(cf / (1 + wacc) ** year for year, cf in enumerate(flows, 1))
    terminal_value = flows[-1] * (1 + terminal_growth) / (wacc - terminal_growth)
    terminal_pv = terminal_value / (1 + wacc) ** 5
    enterprise = explicit_pv + terminal_pv
    equity = enterprise + NON_OPERATING_CASH - DEBT
    price = equity / DILUTED_SHARES
    if not isfinite(price):
        raise ValueError("Calculated share value must be finite.")
    return flows, explicit_pv, terminal_value, terminal_pv, enterprise, equity, price


def share_value(wacc, terminal_growth, shift=0.0):
    return dcf(wacc, terminal_growth, shift)[-1]


def print_sensitivity():
    print("\nSensitivity: value per diluted share (USD)")
    print("WACC / terminal g" + "".join(f"{g:>14.2%}" for g in SENSITIVITY_TERMINAL_GROWTH_RATES))
    for wacc in SENSITIVITY_WACCS:
        cells = []
        for growth in SENSITIVITY_TERMINAL_GROWTH_RATES:
            try:
                cells.append(f"{share_value(wacc, growth):>14.4f}")
            except (ValueError, OverflowError):
                cells.append(f"{'invalid':>14}")
        print(f"{wacc:<17.2%}" + "".join(cells))


def solve_growth_shift(target, lower, upper):
    """Bisect a valid bracket; never substitute a bound for an unreachable target."""
    if not all(isfinite(x) for x in [target, lower, upper]):
        raise ValueError("Target and bracket bounds must be finite.")
    if lower >= upper:
        raise ValueError("Lower shift bound must be less than upper shift bound.")
    if any(not isfinite(g) or g + lower <= -1
           for g in YEARLY_GROWTH_RATES):
        raise ValueError("Invalid bracket: an annual growth rate reaches -100% or below.")
    # These conditions make share value monotonic in the uniform growth shift.
    if STARTING_FCFF <= 0 or TERMINAL_GROWTH <= -1:
        raise ValueError("Reverse DCF requires positive starting FCFF and terminal growth > -100%.")
    low_price = share_value(WACC, TERMINAL_GROWTH, lower)
    high_price = share_value(WACC, TERMINAL_GROWTH, upper)
    if target < low_price or target > high_price:
        raise ValueError(
            f"No solution in that bracket: attainable share prices are "
            f"{low_price:.4f} to {high_price:.4f} USD."
        )
    # An endpoint is a solution only when its price actually equals the target.
    if target == low_price:
        return lower
    if target == high_price:
        return upper
    for _ in range(200):
        midpoint = (lower + upper) / 2
        price = share_value(WACC, TERMINAL_GROWTH, midpoint)
        if abs(price - target) <= 1e-8:
            return midpoint
        if midpoint == lower or midpoint == upper:
            break
        if price < target:
            lower = midpoint
        else:
            upper = midpoint
    raise ValueError("Bisection did not converge to the target price within tolerance.")


def print_reverse_dcf():
    print("\nReverse DCF: uniform shift added to all five explicit growth rates")
    print(f"Target share price (USD): {TARGET_SHARE_PRICE:.4f}")
    print(f"Shift bracket (percentage points): {100 * REVERSE_SHIFT_LOWER:.4f} to {100 * REVERSE_SHIFT_UPPER:.4f}")
    print(
        f"Held fixed: starting FCFF={STARTING_FCFF:.4f} USD millions; "
        f"base growth rates={[round(g, 6) for g in YEARLY_GROWTH_RATES]}; WACC={WACC:.4f}; "
        f"terminal growth={TERMINAL_GROWTH:.4f}; "
        f"non-operating cash={NON_OPERATING_CASH:.4f} USD millions; "
        f"debt={DEBT:.4f} USD millions; diluted shares={DILUTED_SHARES:.4f} million; "
        "five annual end-of-year cash flows and Year-5 terminal value."
    )
    try:
        shift = solve_growth_shift(TARGET_SHARE_PRICE, REVERSE_SHIFT_LOWER, REVERSE_SHIFT_UPPER)
    except (ValueError, OverflowError) as error:
        print(f"Reverse DCF: {error}")
        return
    print(f"Solved uniform growth shift (percentage points): {100 * shift:.8f}")
    print("Price-implied annual growth path: " + ", ".join(f"{g + shift:.4%}" for g in YEARLY_GROWTH_RATES))
    print("This is one conditional implied path, not a unique market forecast.")
    print(f"Value per diluted share at solved shift (USD): {share_value(WACC, TERMINAL_GROWTH, shift):.4f}")


def print_inputs():
    print("\nAAPL inputs and forecast basis (USD millions except per-share price)")
    print("Source: FY26_Q3_Consolidated_Financial_Statements.pdf, June 27, 2026.")
    print(f"p. 3: FCFF proxy = (116,996 CFO - 6,799 capex) * 12/9 = {STARTING_FCFF:.4f}.")
    print("Annualization assumes no seasonality; no after-tax interest add-back or normalization.")
    print(f"p. 2: cash + securities = {NON_OPERATING_CASH:.4f}; debt = {DEBT:.4f}.")
    print("All cash/securities assumed non-operating; debt includes commercial paper and term debt.")
    print(f"p. 1: diluted shares = 14,714,676 thousand / 1,000 = {DILUTED_SHARES:.4f} million.")
    print(f"p. 1: nine-month revenue growth = 364,357 / 313,695 - 1 = {REVENUE_GROWTH:.4%}.")
    print("Assumed FCFF forecast: " + ", ".join(f"{g:.4%}" for g in YEARLY_GROWTH_RATES))
    print(f"Analyst assumptions: linear growth fade; calculated WACC={WACC:.4%}; terminal growth={TERMINAL_GROWTH:.2%}.")
    print("The PDF supplies no five-year forecast; WACC is estimated below; shares stay fixed.")
    print(f"Market price: ${MARKET_PRICE:.4f}; {PRICE_AS_OF}; {PRICE_SOURCE}.")
    print("Saved snapshot, not an automatically refreshed live quote: update price and date together.")


def print_wacc():
    print("\nApple-specific WACC estimate (inputs retrieved September 10, 2026)")
    print(f"Cost of equity = Rf + beta * ERP = {RISK_FREE_RATE:.2%} + "
          f"{EQUITY_BETA:.2f} * {EQUITY_RISK_PREMIUM:.2%} = {COST_OF_EQUITY:.4%}.")
    print("Dates: Treasury Sep 9; beta Sep 4 quote snapshot; ERP Sep 1; bond yield Sep 8, 2026.")
    print(f"After-tax debt cost = {PRETAX_COST_OF_DEBT:.2%} * "
          f"(1 - {MARGINAL_TAX_RATE:.2%}) = {AFTERTAX_COST_OF_DEBT:.4%}.")
    print(f"Equity = ${MARKET_PRICE:.4f} * {SHARES_OUTSTANDING:.4f} million shares "
          f"= {MARKET_EQUITY:.4f} USD millions; gross debt = {DEBT:.4f} USD millions.")
    print(f"Weights: equity={1 - DEBT_WEIGHT:.4%}; debt={DEBT_WEIGHT:.4%}.")
    print(f"WACC = equity weight * cost of equity + debt weight * after-tax debt cost = {WACC:.4%}.")
    print("Estimates: June share count; book debt approximates market debt; one bond yield proxies "
          "borrowing cost; 21% tax shield from FY25 10-K p. 55. No netting cash against debt.")
    print("Treasury-based ERP convention; September 1 ERP held fixed through the valuation date.")
    print("WACC is held fixed during reverse DCF, including when testing a different target price.")
    print("FCFF remains the annualized CFO-minus-capex proxy; WACC does not remove that limitation.")
    for source in WACC_SOURCES:
        print(f"Source: {source}")


def print_call():
    fair_value = share_value(WACC, TERMINAL_GROWTH)
    print("\nAAPL conditional call (model-based research conclusion)")
    print(f"DCF value: ${fair_value:.4f}/share; market: ${MARKET_PRICE:.4f}; "
          f"value/price - 1: {fair_value / MARKET_PRICE - 1:.2%}.")
    print("Status: " + ("Initiation condition met." if MARKET_PRICE < fair_value else "Watch-defer."))
    print(f"Initiate if price falls below ${fair_value:.2f} and the forecast remains supported; "
          "otherwise watch-defer unless sourced evidence supports a higher FCFF path "
          "whose recomputed value exceeds the purchase price.")
    print("The threshold is model fair value, not a guaranteed price floor or a margin of safety.")
    try:
        shift = solve_growth_shift(MARKET_PRICE, REVERSE_SHIFT_LOWER, REVERSE_SHIFT_UPPER)
        print(f"At the market price, breakeven requires a {shift * 100:+.4f}-point uniform growth shift; "
              "initiation requires a supported path above that breakeven path.")
    except (ValueError, OverflowError) as error:
        print(f"Market-implied growth: {error}")
    print(f"Monitor: next quarter's operating margin versus {QUARTER_OPERATING_MARGIN:.2%} "
          f"this quarter and {PRIOR_QUARTER_OPERATING_MARGIN:.2%} in the prior-year quarter (PDF p. 1).")
    print("Check whether profitability persists without tariff refunds: Apple's Q3 release says "
          "refunds added about 2 percentage points to gross margin; do not assume that benefit repeats.")
    print(f"Company context source: {APPLE_RESULTS_URL}")


def main():
    if TERMINAL_GROWTH >= WACC:
        raise SystemExit("Error: terminal growth must be less than WACC.")
    if len(YEARLY_GROWTH_RATES) != 5:
        raise SystemExit("Error: provide exactly five yearly growth rates.")

    if WACC <= -1:
        raise SystemExit("Error: WACC must be greater than -1.")
    if DILUTED_SHARES <= 0:
        raise SystemExit("Error: diluted shares must be greater than zero.")

    try:
        (yearly_fcff, explicit_pv, terminal_value, terminal_pv,
         enterprise_value, equity_value, value_per_share) = dcf(WACC, TERMINAL_GROWTH)
    except (ValueError, OverflowError) as error:
        raise SystemExit(f"Error: {error}")
    if enterprise_value == 0:
        raise SystemExit("Error: enterprise value is zero; terminal-value share is undefined.")
    terminal_pv_share = terminal_pv / enterprise_value

    for year, cash_flow in enumerate(yearly_fcff, start=1):
        print(f"FCFF Year {year} (USD millions): {cash_flow:.4f}")
    print(f"PV of five explicit FCFF (USD millions): {explicit_pv:.4f}")
    print(f"Terminal value at Year 5 (USD millions): {terminal_value:.4f}")
    print(f"PV of terminal value (USD millions): {terminal_pv:.4f}")
    print(f"Enterprise value (USD millions): {enterprise_value:.4f}")
    print(f"Equity value (USD millions): {equity_value:.4f}")
    print(f"Value per diluted share (USD): {value_per_share:.4f}")
    print(f"PV of terminal value / enterprise value (fraction): {terminal_pv_share:.4f}")

    print_inputs()
    print_wacc()
    print_sensitivity()
    print_reverse_dcf()
    print_call()


if __name__ == "__main__":
    main()

