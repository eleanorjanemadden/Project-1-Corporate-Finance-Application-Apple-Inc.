# Dated Apple peer analysis — July31,2026

Read peer_policy.md and peer_policy_addendum.md. Price date matches for both companies; earnings cover June-ending trailing12months, within three days. Values are USD millions. Latest measured cash/debt/share counts remain dated reported proxies, not exactJuly31 balances.

| Company | TTM period end | Common shares/date | Close | EBIT | GAAP NI | Debt | Liquid cash/securities | EV/EBIT | Common equity/NI |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| AAPL | Jun27,2026 |14594.180m/Jul17|308.91|154859|128930|84344|146517|28.71x|34.97x|
| MSFT | Jun30,2026 |7427m/Jun30|464.72|155237|133749|40294|76843|22.00x|25.81x|

Apple TTM = FY25+FY26nine months−FY25nine months. Microsoft FY2026 annual release was publicJuly29. Source rows and transformations are in source_ledger.csv; downloaded MSFT release in sources/. Prices are secondary Yahoo unadjusted close rows; FinanceCharts corroborates them. Dividend-adjusted closes308.64/463.85 were rejected. P/E uses total common-market-equity/GAAP NI consistently, not EPS computed with a different weighted-average share basis. EV adds book interest debt and subtracts liquid cash/securities. Operating leases stay operating; no lease debt added while retaining rent expense. Strategic equity investments are not stripped from enterprise values, a remaining limit of the unadjusted EV diagnostic.

Apply MSFT EV/EBIT to Apple TTM EBIT and latest reported net cash, then divide target equity by the same estimated14652.746m equivalents as DCF: **236.73/share**. Apply MSFT common-equity/NI to Apple GAAP NI with the same target denominator: **227.06/share**. Basic-share equivalents are237.68/227.98. These are two method diagnostics from ONE admitted peer, not a two-observation peer range, and are not averaged.

Both peer diagnostics exceed DCF base119.60 yet are below dated market308.91. Disagreement reflects growth/mix, investment/required-return assumptions, and earnings quality: Microsoft's GAAP NI includes disclosed4963million net OpenAI investment gain; Apple's earnings include temporary refund effects. Do not compare adjusted providerEPS against GAAPEBIT or mechanically average the methods. A pure operating-EV/normalized-common-earnings comparison remains uncompleted; it is not a missing unknowable exact date balance.

Alphabet remains excluded after examination of its June filing: new mandatory convertible preferred stock/capped calls, share classes and very large investment gains require claim/investment normalization. Precise uncompleted reconciliation is in peer_policy_addendum.md. Expanded peer distribution and leave-one-out robustness are not completed. No transaction evidence is used.
