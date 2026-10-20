# Lab 11 — Apple pro-forma sensitivity


| FY2030 base output | Value | Units |
|---|---:|---|
| Operating profit | 194,871.942549 | USD millions |
| FCFE | 146,540.355224 | USD millions |
| Existing model value | 127.616804 | USD/share |

All five forecast years pass the existing accounting and cash-floor checks. Tolerance: 0.000001 USD million ($1); largest residual: 5.82076609135e-11 USD million. Every statement value matches the prior Lab 10 CSV exactly (maximum difference 0). Generated Markdown also matches the previously saved output exactly. The source hash is saved for later preservation checks. This baseline verification is **not** the required post-sensitivity restored-base check, which remains pending.

Full visible statements, checks and valuation: [base_output.md](base_output.md). Unrounded inputs, opening balances, history, all statement lines, checks and valuation: [base_snapshot.json](base_snapshot.json). CSV details: [base_statements.csv](base_statements.csv), [base_checks.csv](base_checks.csv). Verification: [base_verification.txt](base_verification.txt). Reproducible capture code: [capture_base.py](capture_base.py).

### Existing valuation scope and limitations

The existing method discounts FCFE at 10% cost of equity, uses 2.5% terminal growth and 14,594.180 million shares, normalizes terminal debt repayment/interest, and adds $102,420 million opening surplus assets once. FCFE = CFO − PP&E capex − other-asset reinvestment − term-debt repayment. Distributions occur below FCFE. This is an annual-base classroom valuation at the FY2025 opening-model date, using the existing July 17, 2026 share basis; the saved September 24, 2026 market quote is not contemporaneous with that model date. The base supports the existing conditional valuation; no current-market recommendation is inferred.

The engine uses `max(0, fcfe)` inside its present-value sum. This has no effect on the positive base cash flows. If a changed case has negative interim FCFE, retain its signed cash flows and mark valuation unavailable because that existing implementation would omit the negative cash flow. Do not silently use the resulting value or invent terminal assumptions. Other valuation refusals (including nonpositive terminal FCFE or revolver financing) must also remain visible. Accounting failures make runs invalid for ranking.

## D — Define

Which assumptions drive my company's forecast and value, and what explains their effects?

Apple's loyal customer base, and the beleif that they will continue to grow sales is a main driver. They have hardware sales as well as their services revenue which continues to grow. Additionally, their products are high margin which increases profitability. 

## R — Represent inputs and comparisons

Existing independent operating inputs are listed below, without selecting drivers or ranges. Scalar inputs currently apply to every FY2026–FY2030 year. Growth already supports a separate rate each year. A selected subset-year change to another input requires extending a separate analysis copy to support annual values, with the unchanged base verified first.

| Model key | Independent operating input | Existing base | Units |
|---|---|---:|---|
| `growth` | Revenue growth | 15%, 8%, 6%, 5%, 4% | % per year; path FY2026–FY2030 |
| `gross_margin` | Gross profit / revenue | 49.00000000% | % of revenue |
| `sga_ratio` | SG&A / gross profit | 14.13978412% | % of gross profit |
| `rd_ratio` | R&D / revenue | 9.50000000% | % of revenue |
| `depreciation_ratio` | PP&E depreciation / opening PP&E | 16.05329695% | % of opening net PP&E |
| `other_da_ratio` | Residual D&A / revenue | 0.88859840% | % of revenue; matched by other reinvestment |
| `capex_ratio` | PP&E capex / revenue | 3.00000000% | % of revenue |
| `inventory_days` | Inventory holding period | 9.44546524 | days, 365-day convention |
| `receivables_ratio` | Trade receivables / revenue | 9.55807969% | % of revenue |
| `vendor_ratio` | Vendor non-trade receivables / cost of sales | 15.01629254% | % of cost of sales |
| `other_current_assets_ratio` | Other current assets / revenue | 3.50465325% | % of revenue |
| `payables_ratio` | Accounts payable / cost of sales | 31.61658219% | % of cost of sales |
| `deferred_revenue_ratio` | Deferred revenue / revenue | 2.17584060% | % of revenue |

Tax rate is also an independent model input (18%) but is a tax assumption; borrowing, distributions, discount rate, terminal growth and shares are not substitutes for the lab's two operating drivers. Operating profit and FCFE are calculated outputs, not independent inputs. All other base assumptions are retained in the snapshot and original assumption table.

### Driver selection and ranges

Which two existing operating inputs do you select, and why? For each, provide lower/base/higher values with units and affected years. For a path, supply every affected year's values or an explicit percentage-point shift. What company evidence (source and period) or explicitly labeled judgment supports each endpoint? Explain percentage points versus relative percent changes where applicable. Base values must match the model.

Driver: Revenue growth. Lower: 13%, 6%, 4%, 3%, 2%. Base: 15%, 8%, 6%, 5%, 4%. Higher: 17%, 10%, 8%, 7%, 6%. Units: Annual revenue growth; ±2 percentage points from base. Affected years: FY2026–FY2030, respectively.
Driver: Gross margin. Lower: 47%. Base 49%. Higher 51%. Units: Gross profit / revenue; ±2 percentage points from base. Affected years:FY2026–FY2030

I've selected revenue growth because it changes projected sales and affects multiple lines throughout the financial statements. I selected gross margin because it changes how much revenue remains after cost of sales, affecting operating profit and cash flow. These ranges are my judgment for testing sensitivity, rather than estimates supported by historical research. For growth, I increased or decreased each year’s base assumption by two percentage points. For gross margin, I tested 47% and 51% around the 49% base. These changes allow me to compare two operating assumptions while holding the other independent inputs constant.




