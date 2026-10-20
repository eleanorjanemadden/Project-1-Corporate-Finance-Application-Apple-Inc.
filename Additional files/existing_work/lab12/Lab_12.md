# Lab 12
**Eleanor Madden | Apple Inc. (AAPL) | Prepared October 1, 2026**

## D — Current conclusion
 My documented research conclusion is watch-defer: keep Apple under coverage rather than initiate a position on the existing evidence. Apple has strong hardware and Services businesses, but a strong company is not automatically an attractive investment at any price. My models produce different conditional values, and I need to reconcile their assumptions, timing, and share counts before making a stronger recommendation.

The question is: **How did I get from choosing Apple to my valuation conclusion, which assumptions drive it, and what evidence could change my mind?**

My $127.62 annual-base FCFE estimate is not an October 2026 price target. It discounts FY2026–FY2030 to the FY2025 opening-model date and uses 14,594.180 million shares dated July 17, 2026. The $224.00 earlier DCF uses a different cash-flow proxy and conventions.

Because this information is from last year's 10-k, I would continue to watch-defer until they release this years financial performance. 

## Evidence to open
| Evidence | Existing file | Use and limitation |
|---|---|---|
| Research and recorded investment thesis | [Apple research memo](https://github.com/eleanorjanemadden/AAPL-research/blob/main/Apple_2026-09-03_report.md) | Business, conditional watch-defer thesis, risks and research priorities |
| Research source record | [sources.md](https://github.com/eleanorjanemadden/AAPL-research/blob/main/sources.md) | Sources and periods; linked local PDFs are not uploaded in that repository |
| Earlier DCF and reverse DCF | [Lab6_.md](https://github.com/eleanorjanemadden/Lab-6/blob/main/Lab6_.md) | $224.00 value, market reference, held-fixed reverse-DCF assumptions |
| Peer-method exercise | [Lab7.md](https://github.com/eleanorjanemadden/Lab-7/blob/main/Lab7.md) | Asbury exercise, not Apple peer valuation |
| Apple history, assumptions and valuation | [Lab_10_Apple.md](https://github.com/eleanorjanemadden/Lab-10/blob/main/Lab_10_Apple.md) | Historical evidence, forecast judgments, model reasoning |
| Linked Apple engine | [apple_proforma.py](https://github.com/eleanorjanemadden/Lab-10/blob/main/apple_proforma.py) | Actual base rerun; full output reproduced in Appendix A |
| Driver choices and ranges | [Lab_11_Apple.md](https://github.com/eleanorjanemadden/Lab-11/blob/main/Lab_11_Apple.md) | Growth and margin chosen; no changed-case results uploaded |
| Base-capture script | [capture_base.py](https://github.com/eleanorjanemadden/Lab-11/blob/main/capture_base.py) | Base only; expects a Lab 10 folder layout absent from this repository |



## R — Six-stop presentation route


### 1. Target selection — about 1 minute
Apple is suitable for analysis because its hardware and Services businesses offer distinct revenue mechanisms, while its financial statements allow me to connect profitability, working capital, investment, and cash generation. My research focuses on whether its operating strengths justify its valuation.

My existing Lab 10 answer emphasizes Apple's leadership and its product and Services revenue streams. My research memo's documented starting call was watch-defer.

I originally chose to analyze Apple because I saw in the news that they got a new CEO, so I wanted to look further into the company. 

### 2. Company and evidence — about 2 minutes
 Apple earns money from products such as iPhones, Macs and iPads, and from Services. My saved research reports FY2025 revenue of $416,161 million: Products of $307,003 million and Services of $109,158 million. Its FY2026 nine-month update reports revenue of $364,357 million, versus $313,695 million a year earlier. These periods are not interchangeable with full fiscal years.

The historical forecast anchor is FY2025, with a September 27, 2025 opening balance sheet. My Lab 10 report references the FY2025 10-K's printed statement pages 29–33 and the Q3 FY2026 filing. The earlier research memo uses PDF-viewer page numbers, so I need to identify which pagination I mean.


### 3. Pro-forma — about 3 minutes
I built FY2026–FY2030 from history and labeled judgments. Growth is 15%, 8%, 6%, 5%, and 4%. Gross margin is 49%, R&D is 9.5% of revenue, and capex is 3% of revenue. These are forecast choices, not management guidance. The saved Lab 10 report supports the first-year growth judgment with nine-month revenue growth of 16.15%, and margin with a nine-month ratio of 49.07%.

Apple-specific vendor non-trade receivables are tied to cost of sales. They are operating assets, so an increase consumes operating cash. They do not create extra revenue. SG&A is 14.1398% of gross profit, so SG&A dollars change when gross profit changes even if its independent ratio stays fixed.

The model calculates income, operating balances, investment, financing, equity, and finally cash. FCFE is CFO less PP&E capex, other-asset reinvestment, and term-debt repayment. Buybacks and dividends are distributions below FCFE.


### 4. Valuation — about 3 minutes
| Convention | Earlier Lab 6 DCF | Lab 10/11 pro-forma valuation |
|---|---|---|
| Cash-flow basis | Annualized nine-month CFO less capex, labeled FCFF proxy; omits after-tax interest addback | Explicit linked-statement FCFE |
| Discount rate | 9.2462% WACC | 10% cost of equity |
| Terminal growth | 3.0% | 2.5% |
| Share basis | 14,714.676 million; latest-quarter weighted-average diluted proxy | 14,594.180 million; July 17, 2026 outstanding shares |
| Equity bridge | Enterprise value + $146,517m cash/securities − $84,344m debt | FCFE equity value + $102,420m opening surplus assets; no second debt subtraction |
| Reported value | $224.00 per diluted share | $127.62 per share at FY2025 opening-model date |
| Market reference | $315.34 regular-session close, September 10, 2026 | $337.01 intraday, September 24, 2026 at 3:03 p.m. EDT |
| Main limitation | Annualization assumes no seasonality; FCFF proxy and share basis need refinement | Annual-base timing and later share/price inputs; terminal and financing judgments |


The pro-forma bridge is $473,282.24 million of explicit FCFE present value plus $1,286,760.37 million of terminal present value plus $102,420 million of surplus assets, giving $1,862,462.61 million of equity value. Terminal value is 69.09% of total equity value. Debt is not subtracted again because this is an FCFE valuation.

My DCF estimated Apple’s intrinsic value at $224 per share. Since the market price exceeded that estimate ($269.37), Apple appeared overvalued under my assumptions.

### 5. Sensitivity and drivers — about 2 minutes

| Input | Lower | Base | Higher | Units and years |
|---|---|---|---|---|
| Growth | 13%, 6%, 4%, 3%, 2% | 15%, 8%, 6%, 5%, 4% | 17%, 10%, 8%, 7%, 6% | Annual revenue growth, FY2026–FY2030 respectively; ±2 percentage points |
| Gross margin | 47% | 49% | 51% | Gross profit / revenue, every year FY2026–FY2030 |

Growth changes revenue, which affects gross profit, SG&A, R&D, working capital and capex. Net income and these cash adjustments determine FCFE, which feeds equity value if the valuation is valid. Margin changes gross profit and cost of sales at unchanged revenue, also changing SG&A and cost-of-sales-linked working capital.

In this engine, operating income = revenue × [gross margin × (1 − SG&A/gross-profit ratio) − R&D/revenue ratio]. This explains why a margin improvement does not all become operating profit: SG&A rises with gross profit.

I think one of the most significant drivers for Apple is their loyal customer base too. This will continue to drive sales. 

### 6. Interpretation — about 1 minute
I can support a conditional watch-defer position from the existing memo, with unresolved valuation work clearly identified. I would research whether near-term growth and a 49% margin are durable, how hardware replacement cycles and Services economics affect that outlook, and whether AI investment improves monetization enough to justify its costs.

Evidence that would change my view includes verified forward earnings and cash-flow estimates, resilient Services economics, supported assumptions, and an acceptable expected return at a consistently dated purchase price. Weaker demand, lower margins, or a valuation dependent on multiple expansion would weaken the case.

## V - Questions and ask

My partner chose Duolingo because she was interested in a niche tech company that did a subscription-based revenue model. She thought that AI might significantly impact the share price, but hasn't shown to make much of a difference. Her DCF reasonably valued Duolingo, aligning closely to the actual share price. 

## Reflect
The useful question to reconsider is whether customer loyalty supports the actual forecast numbers, rather than only a positive business story. The model also shows that accounting consistency and forecast credibility are separate tests.



