# Lab 6 — Apple (AAPL) DCF

## Inputs and assumptions

All dollar amounts are USD millions unless stated otherwise.

| Item | Value | Assumption / basis |
|---|---:|---|
| Starting FCFF proxy | $146,929.33 | `(116,996 CFO − 6,799 capex) × 12/9`; annualizes nine-month cash flow, assumes no seasonality, and omits an after-tax interest add-back |
| Five-year FCFF growth | 16.1501%, 12.8626%, 9.5750%, 6.2875%, 3.0000% | FCFF grows with revenue; growth fades linearly from nine-month revenue growth to 3% |
| WACC | 9.2462% | CAPM cost of equity plus after-tax debt cost; book debt proxies for market debt |
| Terminal growth | 3.00% | Analyst long-run assumption, not Apple guidance |
| Cash and marketable securities | $146,517 | All treated as non-operating and available to equity holders |
| Debt | $84,344 | Commercial paper plus current and non-current term debt |
| Diluted shares | 14,714.676 million | Latest-quarter weighted-average diluted shares proxy for valuation-date shares |
| Forecast convention | Five annual, end-of-year cash flows | Year-5 FCFF is used to calculate terminal value |

## Base-case output

| Output | Result |
|---|---:|
| Year 1 FCFF | $170,658.54 |
| Year 2 FCFF | $192,609.60 |
| Year 3 FCFF | $211,052.05 |
| Year 4 FCFF | $224,321.99 |
| Year 5 FCFF | $231,051.65 |
| PV of explicit FCFF | $785,442.57 |
| PV of terminal value | $2,448,486.01 |
| Enterprise value | $3,233,928.57 |
| Equity value | $3,296,101.57 |
| **Implied value per diluted share** | **$224.00** |
| Terminal-value share of enterprise value | 75.71% |

## Sensitivity: value per diluted share

| WACC \ Terminal growth | 2.00% | 3.00% | 4.00% |
|---:|---:|---:|---:|
| 8.25% | $231.62 | $266.53 | $317.87 |
| 9.25% | $199.65 | **$224.00** | $257.64 |
| 10.25% | $175.44 | $193.23 | $216.71 |

## Price comparison and interpretation

Apple's regular-session closing price on September 10, 2026 was **$315.34 per share**. The model value of **$224.00** is **0.71×** the market price (29.0% lower), so it is inside the required 0.5×–2× reasonableness range. The model therefore does not require an input adjustment.

Holding starting FCFF, WACC, terminal growth, cash, debt, diluted shares, the five-year timing convention, and all other inputs fixed, matching the $315.34 market price requires adding **8.7021 percentage points** to every explicit-period growth rate. The resulting price-implied growth path is **24.8522%, 21.5647%, 18.2772%, 14.9896%, and 11.7021%**. This shift is a conditional sensitivity result, not proof that Apple is mispriced and not a unique market forecast.

Price source: [Investing.com AAPL quote](https://www.investing.com/equities/apple-computer-inc), corroborated by [Public's September 10 after-hours page](https://public.com/stocks/aapl/after-hours), which reports the same $315.34 regular-session close.

## Anonymous temperature check

- **What works:** Building the DCF in Python makes the assumptions transparent and makes sensitivity checks quick.
- **What confuses:** It is difficult to distinguish sourced company data from analyst assumptions, especially for FCFF and WACC.
- **One change:** Provide a short example that labels each input as reported, calculated, or assumed before students build the model.

