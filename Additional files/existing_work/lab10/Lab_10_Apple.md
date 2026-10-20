## D - Define

What are five years of Apple's statements worth, built from assumptions that can be defended?

Company: **Apple Inc.** Ticker: **AAPL**. Historical years: FY2023, FY2024 and FY2025. Opening balance sheet: September 27, 2025. Forecast years: FY2026-FY2030.

The existing ABG `proforma.py` was run first: $291.75 per share, 79.76% of value after 2030, and zero annual balance gaps. The Apple adaptation is saved separately as [apple_proforma.py](apple_proforma.py).

### Apple-specific implementation

The selected working-capital line is **vendor non-trade receivables**. Apple's component purchases and manufacturing-vendor arrangements create this asset; it is neither a dealer inventory loan nor additional sales revenue. The model links its ending balance to cost of sales and subtracts the increase in operating cash flow. This is a cost-of-sales proxy, not a claim that Apple's contracts specify a fixed ratio. Apple reports $33,180 of this asset at FY2025 year-end. [S1, balance sheet p. 31 and Note 4 p. 39](https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm)

The model also includes R&D separately, removes ABG floor-plan financing, includes dividends and commercial paper, and distinguishes PP&E depreciation from total D&A. It does not deduct depreciation a second time from gross profit less SG&A and R&D: Apple's reported expense categories already incorporate depreciation.

Apple is a unique company because its a leader in its group. They are very consistent and have 2 strong lines of revenue, one from their products (iPhone, iPad, etc.) and the other from their services which they continue to expand. 


## R - Historical evidence

### Sources

Page numbers below are the **printed filing pages**, not PDF-viewer page numbers. The local FY2025 PDF has a different viewer-page offset.

| ID | Source | Sections used |
|---|---|---|
| S1 | [Apple FY2025 10-K](https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm), filed October 31, 2025 | MD&A pp. 21-26; statements pp. 29-33; Note 4 vendor receivables and Note 5 PP&E p. 39; Note 9 debt p. 44 |
| S2 | [Apple FY2024 10-K](https://www.sec.gov/Archives/edgar/data/320193/000032019324000123/aapl-20240928.htm), filed November 1, 2024 | Statements of operations p. 29; balance sheet p. 31; cash flows p. 33; MD&A and Notes 5 and 7 |
| S3 | [Apple FY2023 10-K](https://www.sec.gov/Archives/edgar/data/320193/000032019323000106/aapl-20230930.htm), filed November 3, 2023 | Statements of operations p. 28; balance sheet p. 30; cash flows p. 32; MD&A and Note 5 |
| S4 | [Apple Q3 FY2026 10-Q](https://www.sec.gov/Archives/edgar/data/320193/000032019326000020/aapl-20260627.htm) | Cover: 14,594,180,000 shares outstanding July 17, 2026; p. 1: nine-month income statement |
| S5 | [Stock Analysis / S&P Global cash-flow data](https://stockanalysis.com/stocks/aapl/financials/cash-flow-statement/), retrieved September 24, 2026 | Annual capex comparison; dated AAPL price snapshot |
| C1 | [Lab 10 instructions](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-05/lab-10-proforma-your-company.md) | Assignment and grading criteria |
| C2 | [Lab 9 engine requirements](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-05/lab-09-proforma-build.md) and [Part 1 tutorial](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-05/pro-forma-abg-tutorial.md) | Benchmark, cash-last method, refusal checks and FCFE valuation |

### Required three-year history grid

Every cell gives its filing and printed page. Gross profit is the dollar line Apple calls gross margin; it is not the gross-margin percentage.

| Item | FY2023 | FY2024 | FY2025 |
|---|---:|---:|---:|
| Revenue | 383,285 (S3 p. 28) | 391,035 (S2 p. 29) | 416,161 (S1 p. 29) |
| Gross profit | 169,148 (S3 p. 28) | 180,683 (S2 p. 29) | 195,201 (S1 p. 29) |
| SG&A | 24,932 (S3 p. 28) | 26,097 (S2 p. 29) | 27,601 (S1 p. 29) |
| Net income | 96,995 (S3 p. 28) | 93,736 (S2 p. 29) | 112,010 (S1 p. 29) |
| Inventory | 6,331 (S3 p. 30) | 7,286 (S2 p. 31) | 5,718 (S1 p. 31) |
| Net PP&E | 43,715 (S3 p. 30) | 45,680 (S2 p. 31) | 49,834 (S1 p. 31) |
| Shareholders' equity | 62,146 (S3 p. 30) | 56,950 (S2 p. 31) | 73,733 (S1 p. 31) |

AI source review: the required 21 figures above were located in the filings; none is marked unresolved. This does **not** count as the student's two manual checks.

### Supporting historical inputs

| Item | FY2023 | FY2024 | FY2025 | Source |
|---|---:|---:|---:|---|
| Cost of sales | 214,137 | 210,352 | 220,960 | S1 p. 29, also S3 p. 28 and S2 p. 29 |
| R&D | 29,915 | 31,370 | 34,550 | Same income statements |
| Pretax income | 113,736 | 123,485 | 132,729 | Same income statements |
| Income-tax provision | 16,741 | 29,749 | 20,719 | Same income statements |
| PP&E depreciation, rounded disclosure | 8,500 | 8,200 | 8,000 | S1 Note 5 p. 39, corroborated by each earlier filing's Note 5 |
| Total depreciation and amortization | 11,519 | 11,445 | 11,698 | S1 cash flows p. 33 |
| Vendor non-trade receivables | 31,477 | 32,833 | 33,180 | S3 p. 30; S2 p. 31; S1 p. 31 |
| PP&E capital spending | 10,959 | 9,447 | 12,715 | S3 p. 32; S2 p. 33; S1 p. 33 |

Depreciation is disclosed in tenths of a billion; converting it to millions does not create additional precision. Total D&A is **not** interchangeable with PP&E depreciation in the PP&E roll-forward.

### Required ratios and capital-spending comparison

| Ratio or comparison | FY2023 | FY2024 | FY2025 |
|---|---:|---:|---:|
| Gross profit / revenue | 44.13% | 46.21% | 46.91% |
| SG&A / gross profit | 14.74% | 14.44% | 14.14% |
| Inventory / cost of sales x 365 | 10.79 days | 12.64 days | 9.45 days |
| PP&E depreciation / ending net PP&E | 19.44% | 17.95% | 16.05% |
| Total D&A / ending net PP&E, context only | 26.35% | 25.05% | 23.47% |
| Tax provision / pretax income | 14.72% | 24.09% | 15.61% |
| Reported revenue growth | -2.80% | 2.02% | 6.43% |
| Separately disclosed consolidated organic/same-store growth | Not identified | Not identified | Not identified |
| R&D / revenue, Apple context | 7.80% | 8.02% | 8.30% |
| Filing PP&E capital spending, positive spending amount | 10,959 | 9,447 | 12,715 |
| Provider capital expenditures, signed cash-flow field (S5) | -10,959 | -9,447 | -12,715 |
| Difference after normalizing outflow sign | 0 | 0 | 0 |

Ratios are computed from the sourced amounts above. FY2023 growth uses FY2022 revenue of 394,328 from S3 p. 28. Inventory days use ending inventory and 365 days, matching the tutorial convention; FY2023 actually had 53 weeks, so this is a standardized metric rather than exact fiscal-period days. Depreciation uses ending PP&E in the history ratio and that ratio is applied to opening PP&E in each forecast year, as in the lab.

The capex provider agrees with the filings after sign normalization. Its other standardized fields should not automatically be treated as identical to Apple's reported lines; only the requested capex field was reconciled here.

The MD&A discusses product/service and geographical sales changes; no consolidated organic or same-store series was identified in the three filings. Reported sales growth is therefore shown as reported, not relabeled organic. FY2024's 24.09% effective tax rate also should not be mechanically extrapolated: the State Aid Decision affected that year's tax expense. [S1 MD&A pp. 23-25](https://www.sec.gov/Archives/edgar/data/320193/000032019325000079/aapl-20250927.htm)




### Opening balance sheet - FY2025

All inputs are history from S1 p. 31. The grouped rows explicitly show their construction; no balancing plug is used.

| Asset | Amount | Liability or equity | Amount |
|---|---:|---|---:|
| Cash and cash equivalents | 35,934 | Accounts payable | 69,860 |
| Marketable securities: 18,763 current + 77,723 non-current | 96,486 | Deferred revenue | 9,055 |
| Trade receivables | 39,777 | Other liabilities: 66,387 current + 41,549 non-current | 107,936 |
| Vendor non-trade receivables | 33,180 | Commercial paper | 7,979 |
| Inventory | 5,718 | Term debt: 12,350 current + 78,328 non-current | 90,678 |
| Other current assets | 14,585 | Modeled revolver | 0 |
| Net PP&E | 49,834 | Total liabilities | 285,508 |
| Other non-current assets | 83,727 | Shareholders' equity | 73,733 |
| **Total assets** | **359,241** | **Total liabilities + equity** | **359,241** |

### Labelled assumptions

No quantitative assumption is labeled guidance: the model does not claim that management supplied these five-year forecasts. Historical ratios are labeled history in the lab's sense of carrying forward a computed ratio; assuming that they remain stable is still a modeling choice.

| Value / assumption | Label | Evidence, model rationale and required student reason |
|---|---|---|
| **J1 - Revenue growth:** 15%, 8%, 6%, 5%, 4% for FY2026-FY2030 | Judgment | S4 nine-month revenue grew 16.15%. The first-year proposal is slightly below that pace, then tapers as growth normalizes. It is not management guidance and does not assume acquisitions. 
| **J2 - Gross margin:** 49% each year | Judgment | S4 nine-month gross margin was 49.07%, versus FY2025's 46.91%. The proposal holds near the recent level without indefinite margin expansion; tariffs and product/service mix could invalidate it. 
| **SG&A / gross profit:** 27,601 / 195,201 = 14.1398% | History | Exact FY2025 ratio, S1 p. 29; carried forward with no assumed efficiency gain. |
| **J3 - R&D / revenue:** 9.5% | Judgment | S4 nine-month R&D/revenue was 9.34%, above FY2025's 8.30%. The proposal allows a slightly higher investment burden.  |
| **PP&E depreciation / opening net PP&E:** 8,000 / 49,834 = 16.0533% | History | S1 Note 5; distinct from total D&A. Depreciation remains embedded in the expense ratios and is added back only in cash flow. |
| **Residual D&A / revenue:** (11,698 - 8,000) / 416,161 = 0.8886% | History | Arithmetic difference between S1 p. 33 D&A and Note 5 PP&E depreciation; approximate because the latter is rounded. The other-asset mapping is J12 below. |
| **J4 - PP&E capex / revenue:** 3% | Judgment | Near FY2025's 12,715 / 416,161 = 3.06%; a conservative reinvestment allowance rather than treating the newest interim pace as permanent.  
| **J5 - Effective tax rate:** 18% | Judgment | Above FY2025's 15.61%, close to S4 nine-month 17.58%, and avoids perpetuating FY2024's unusual tax charge.
| **Inventory days:** 5,718 / 220,960 x 365 = 9.4455 | History | FY2025 ending-inventory convention; S1 pp. 29 and 31. |
| **Trade receivables / revenue:** 39,777 / 416,161 = 9.5581% | History | S1 pp. 29 and 31. Increases use operating cash. |
| **Vendor non-trade receivables / cost of sales:** 33,180 / 220,960 = 15.0163% | History | Apple's selected company-specific working-capital line. It is an asset; increases consume cash. This does not create revenue or floor-plan debt. |
| **Other current assets / revenue:** 14,585 / 416,161 = 3.5047% | History | FY2025 ratio; S1 pp. 29 and 31. |
| **Accounts payable / cost of sales:** 69,860 / 220,960 = 31.6166% | History | FY2025 ratio; increases supply operating cash. |
| **Deferred revenue / revenue:** 9,055 / 416,161 = 2.1758% | History | FY2025 ratio; increases supply operating cash. |
| **J6 - Term-debt cash repayments:** 12,393; 10,078; 9,300; 5,235; 4,972. Commercial paper stays at 7,979 | Judgment, based on filed contractual schedule | S1 Note 9 p. 44 provides the maturity amounts; paying them without new net term borrowing and rolling commercial paper is the policy judgment. The model starts at carrying debt, 90,678, rather than principal 91,281; it holds the 603 net carrying adjustment constant instead of modeling accretion/hedges. 
| **J7 - Interest rates:** 3% term debt; 3.5% commercial paper | Judgment | Simplified blended costs, not claimed as Apple's reported effective borrowing rates or current quotes. Interest uses opening balances. 
| **J8 - Annual distributions:** 75,000 buybacks; 16,000 dividends | Judgment | FY2025 cash-flow amounts were 90,711 repurchases and 15,421 dividends. The proposal moderates repurchases while retaining dividends and debt repayment; distributions reduce cash and equity, not FCFE. **YOUR RESPONSE J8:** [Your reason for both amounts.] |
| **J9 - Minimum cash:** 30,000; additional revolver limit 0; unused scenario rate 6% | Judgment | Opening cash is 35,934. No unverified credit facility is assumed. The base case needs no revolver; an unfunded cash shortfall stops valuation. The 6% rate is only a scenario input if a facility is later justified. 
| **J10 - Cost of equity:** 10% | Judgment | A transparent classroom hurdle rate, not an estimated current CAPM result. It is provisional and a material driver of value. FCFE must be discounted at cost of equity, not WACC.
| **J11 - Terminal growth:** 2.5% | Judgment | A mature perpetual-growth assumption below 10% cost of equity; it is not the five-year revenue forecast.
| **Shares for valuation:** 14,594.180 million | History | S4 cover: 14,594,180,000 issued and outstanding on July 17, 2026. This is a point-in-time share count, not weighted-average diluted EPS shares. |
| **J12 - Other balances:** other non-current assets 83,727; other liabilities 107,936; securities 96,486 held flat; other-asset reinvestment equals residual D&A | Judgment | Simplifies non-core schedules while explicitly offsetting non-PP&E asset consumption with reinvestment. Allocating residual D&A to this aggregate is a proxy, not a disclosed amortization schedule.
| **J13 - Future share compensation:** cash-equivalent expense; no SBC addback or forecast share issuance | Judgment | Prevents treating compensation as free cash while ignoring dilution. Expenses retain the compensation burden; future payments are modeled as cash, unlike Apple's actual equity-award mechanics. Fixed valuation shares describe today's claim on aggregate equity; modeled buybacks are distributions, not an automatic extra per-share uplift. 
| **J14 - Interest income, other gains, OCI, acquisitions and incremental impairment:** zero | Judgment | No speculative gains, investment income, acquisitions or separate write-downs are forecast. Marketable securities are valued separately, so their income is excluded to avoid double-counting. 
| **J15 - After FY2030:** refinance remaining debt; no net principal repayment; continuing interest | Judgment | Terminal FCFE adds back FY2030 repayment and the after-tax interest saving from that final repayment, then grows at 2.5%. Debt does not disappear: refinancing is required. 
| **J16 - Surplus-assets valuation adjustment:** 96,486 securities + (35,934 - 30,000) excess cash = 102,420 | Judgment | Assumes these opening assets are distributable at carrying value with no haircut; their income is excluded from the forecast. They are added once, and no terminal cash balance is added again. 

### YOUR RESPONSE - partner attack and two-sentence answer

This belongs directly under the assumption table, as instructed. Use an actual classmate's challenge; the AI's tests and research notes do not count as partner review.

- Partner name/date: Drew
- His specific attack on one judgment: He pushed back on the assumption that revenue growth will significantly slow from aroun 15% to 4% because he thinks that Apple revenue will grow as the market trends upward. 
- My answer: I explained that I think grow will gradually slow because Apple has been slow in AI adoption, and the market will become more competitive. 
- My specific attack on their company and judgment: I wanted to know why he made the assumption that Nvidia's R&D percentage costs would increase. 
## I - Implementation

Run from this Lab 10 folder:

```sh
python3 proforma.py
python3 apple_proforma.py
python3 apple_proforma.py --write
python3 -m unittest -v test_apple_proforma.py
```

The first command reruns ABG. The second prints Apple. The third refreshes [apple_results.md](apple_results.md) and the machine-readable [apple_forecast.csv](apple_forecast.csv). The fourth runs accounting/refusal tests. Python 3 and its standard library are sufficient; there are no packages to install. The CSV is an export, not an input.

Annual logic:

1. Forecast sales, gross profit, SG&A, R&D, interest, taxes and net income.
2. Forecast operating assets and liabilities; roll PP&E, other assets, debt and equity.
3. Build CFO from net income, non-cash D&A and the separately computed working-capital changes. Build investing and financing cash flows.
4. Calculate cash from opening cash plus net cash flow, after distributions and any permitted financing.
5. Recompute all accounting checks from the statement lines before allowing valuation.

The model uses **FCFE = CFO - PP&E capex - other-asset reinvestment - term-debt repayment**. The cash-flow statement then subtracts buybacks and dividends below FCFE. Equity rolls by net income less the same distributions. No debt amount is subtracted again from FCFE equity value.

## V - Results and checks

Full three-statement output and all check rows are in [apple_results.md](apple_results.md).

| Result | FY2026E | FY2027E | FY2028E | FY2029E | FY2030E |
|---|---:|---:|---:|---:|---:|
| Revenue | 478,585.1 | 516,872.0 | 547,884.3 | 575,278.5 | 598,289.6 |
| Net income | 125,363.9 | 135,894.6 | 144,425.5 | 151,970.9 | 158,245.7 |
| FCFE before distributions | 103,056.7 | 117,898.9 | 127,590.7 | 139,538.0 | 146,540.4 |
| Closing cash | 47,990.7 | 74,889.7 | 111,480.4 | 160,018.4 | 215,558.8 |
| Assets - liabilities - equity | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Cash-floor shortfall | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| Revolver balance | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

No revolver is drawn because internal cash generation covers modeled capital investment, repayments, buybacks and dividends while retaining the $30,000 minimum. All projected FCFE are positive, so the lab's negative-FCFE branch does not apply to this base case.

The model checks balance-sheet equality, cash-flow linkage, CFO/CFI/CFF reconciliation, PP&E and other-asset roll-forwards, debt, equity, revolver, FCFE, statement totals and the cash floor. It rejects nonfinite amounts and invalid terminal growth. Checks use full precision with a $1 tolerance (0.000001 million), not rounded display values.

**Validation completed:** 10 tests passed. They include deliberately typing cash, omitting vendor receivables from CFO, hiding a PP&E error with an offsetting asset, exhausting the cash floor, using invalid terminal growth, inserting NaN, and dropping a forecast year. Additional economic tests confirm that higher R&D reduces value and that changing distributions does not create pre-distribution FCFE value. [Test code](test_apple_proforma.py)

### Valuation bridge

| Component | USD millions |
|---|---:|
| PV of five annual FCFE at 10% | 473,282.24 |
| FY2031 normalized terminal FCFE | 155,425.53 |
| PV of terminal value | 1,286,760.37 |
| FCFE equity value before surplus assets | 1,760,042.61 |
| Opening surplus cash and marketable securities | 102,420.00 |
| **Total estimated equity value** | **1,862,462.61** |
| Shares, millions | 14,594.180 |
| **Estimated value per share** | **$127.62** |

For transparency, the FCFE-only course-style result before the Apple surplus-assets adjustment is $120.60 per share. The headline $127.62 includes the separately labeled adjustment. Terminal value is 69.09% of total equity value, making terminal growth and cost of equity material judgments.

The terminal calculation is:

```text
Normalized FY2031 FCFE =
    [FY2030 FCFE + FY2030 repayment
     + FY2030 repayment x term interest rate x (1 - tax rate)] x (1 + g)
Terminal value at FY2030 = normalized FY2031 FCFE / (cost of equity - g)
```

The interest adjustment reflects the difference between FY2030 opening debt and the debt left after that year's repayment. Repayment stops because remaining debt is assumed refinanced, not forgiven. Unlike enterprise-value DCF, this calculation does not subtract debt again: borrowing costs and modeled principal repayments already affect FCFE.

### Dated market comparison

The retrieved S5 page showed **AAPL $337.01 at 3:03 p.m. EDT on September 24, 2026**, during the trading session. This is an intraday snapshot, not a closing price. At the same 14,594.180 million shares, the reference market equity value is $4,918,384.60 million. It is calculated directly from that quote and count rather than borrowing a provider's differently dated market cap.

**Comparison sentence:** The Apple annual-base model says $127.62 per share and the market snapshot says $337.01 on September 24, 2026, using 14,594.180 million shares for both equity-value comparisons; what different expectations for growth, margins and required return would explain the gap?

**Timing limitation:** The lab engine discounts FY2026-FY2030 by one through five full years from its FY2025 opening-model date. The quote and share count are later dated comparison inputs, and the first-year assumptions incorporate the Q3 update. This is therefore a classroom annual-base model, not a point-in-time backtest or a fully rolled-forward valuation as of September 24, 2026. Using the same share count removes a denominator mismatch; it does not remove this timing difference.

### Interpretation limits

Balancing verifies accounting links, not the truth of the forecast. The main simplifications are blended interest rates, flat other liabilities (including tax/lease aggregates), a cost-of-sales proxy for vendor receivables, cash-equivalent treatment of future stock compensation, fixed valuation shares, and the surplus-assets/terminal-refinancing judgments. The model is useful for the lab's auditable base case; these judgments must be defended rather than presented as company guidance.


## Reflect - YOUR RESPONSE

1. Which assumption label would you defend the longest, and why? I would defend labeling the 49% gross-margin assumption as a judgment. Although Apple’s first nine months of FY2026 support a margin near that level, keeping it constant for five years is a forecast decision, not a historical fact. I would reconsider the assumption if tariffs increased costs or Apple’s product and services mix changed substantially.
2. What one number in Apple's filing surprised you, and why? Apple’s $33.18 billion in vendor non-trade receivables surprised me because it was much larger than its $5.72 billion in inventory at the end of FY2025. I had focused on Apple’s finished products without considering how its component arrangements with manufacturers affect working capital. That helped me understand why the model needs to track vendor receivables separately.


