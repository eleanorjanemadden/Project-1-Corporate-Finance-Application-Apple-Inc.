> Manual-upload package: finance code, assumptions, and saved results are unchanged. This package was assembled without executing models or tests.

## Included submission paths

Final PDFs: `docs/Decision-Memo.pdf`, `docs/Research-Evolution.pdf`, and `docs/Validation-and-AI-Use.pdf`. Actual supplied transcripts: `docs/transcript-video-1.txt`, `docs/transcript-video-2.txt`, and `docs/transcript-video-3.txt`. Recordings are excluded.

The supplied `docs/submission_manifest.csv`, completion records, validation logs, and hash inventories are preserved historical records. Some entries predate the final PDFs/transcripts and still say pending; they are not a current attachment checklist. The frozen inventory describes the earlier full project, including intentionally omitted preparation/draft files, and is not a checksum manifest of this package.

Launch directly from this folder using the saved results:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -B -m streamlit run app.py --browser.gatherUsageStats=false
```

`outputs/dated/` contains the final dated exports. `outputs/retrospective/visible_output.json` supports the app's optional retrospective view. Root exports are retained for document references. `existing_work/` contains all 19 protected originals required by the preservation test, including Original Edition A; `reproduction/`, `recovered_context/`, and selected `archive/retrospective_v1/` files preserve comparison and changed-input evidence. `tests/` and `scripts/cold_run.py` retain their fixtures. Historical `existing_work/lab11/capture_base.py` uses the original `Lab 10/Submission/` layout, which is not present here; retain it as evidence, not as an active entry point.

Excluded: duplicate final attachments, editable memo/evolution drafts, preparation outlines, course starter/templates, document-generation scripts, redundant archive exports, environments, caches, credentials, MP4s, and temporary renderings. Source course slides are retained as a required test fixture.

## Original model README (historical statements retained)

# Apple FIN43900 Project1 — existing model finished with dated extension

**Dated action: watch/defer; no position; do not initiate at July31,2026 close308.91 on these assumptions.** FCFF low/base/high **78.52/119.60/181.30** per estimated common equivalent. DecisioncutoffJuly31end-of-day17:00EDT; quote16:00close. This is a July31assessment, not anOctober19price target. Submission is NOT complete; see exact UNMETitems in [completionstatus](docs/completion_status.md).

The old September27,2025 retrospective illustration is preserved separately:72.74/125.23/172.33. Existing statement engine, tests and course evidence were reused. No push/publication or human media/evidence created.

## Dates, data and financial definitions
June27reported financials, July17reported basicshares, July30release and July31morning10-Q are used. Between-report balances are estimates, not invented observations. Newengine projects FY26Q4, interpolates estimatedJuly31balance, removes elapsedFCFF, then values remainingstub plus five full yearsFY2027–2031. Futurefiscalends/daycounts are explicit. USDmillions, sharesmillions, per-shareUSD, ratesdecimal. [Methods](docs/dates_and_methods.md), [sourceledger](docs/source_ledger.csv), [peerpolicy](docs/peer_policy_addendum.md).

FCFF=EBIT*(1−operatingtax)+operatingD&A−capex−otherreinvestment−ΔoperatingNWC. Vendorreceivables are operatingassets; otherD&A matchedbyreinvestment; debtprincipal/distributions excluded; signednegativeflowsretained. Cashroute=CFO+CFI+NOPAT−NI. Selectedmincash affects surplus; futureforecastcash neveradded. Zero modeledrevolver is an assumption.

WACC10.6055%: primaryJuly30DGS10 4.68%, assumedbeta1.10/ERP5.5%, debtcost5%/shield21%, grossdebtmarketweight. g2.5%; terminalshare68.91%; impliedcontinuingROIC64.3%. Shares14652.746m are estimated equivalents: July17basic14594.180 plus58.566 quarterlydilutionproxy. FutureSBC expensedascash, noaddback/newissuance; detailedawardclaims incomplete.

## Setup, execution and tests
TestedPython3.13.1. From thisfolder:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -B analysis.py
.venv/bin/python -B dated_refresh.py
.venv/bin/python -B -m unittest discover -s tests -v
.venv/bin/python -B -m streamlit run app.py --browser.gatherUsageStats=false
```

analysis.py regenerates RETROSPECTIVE outputs; dated_refresh.py regenerates primarydated contract and exports. Neither downloads live data. No credentials/.envneeded. If OneDriveblocks cachedbytecode/originalfiles, use a fresh venv on localdisk and clear/move only caches; do not overwrite evidence. Preservationtest uses15secondboundedread and reportsSKIP ratherthanpretendverification. Actual final outcomes: outputs/package_analysis_run.log, outputs/package_dated_run.log and outputs/package_tests.log. Both engines exited 0; 32 tests ran, 31 passed and one original-file preservation check skipped (existing_work/lab06/dcf.py unavailable). Prior floating-point assertion failure is preserved in outputs/refresh_tests_latest.log; corrected with a 12-decimal tolerance, without changing financial formulas. The ledger test emits a non-fatal unclosed-file ResourceWarning.

The earlier outputs/cold_run_log.txt records a runtime-only fresh environment: selected runtime/source fixtures copied, original evidence/archive excluded, preservation explicitly skipped; 28 of 29 then-current tests passed, contracts matched and local HTTP health was 200. It predates the final test additions. No full cold run or installation was performed during final packaging. Do not interpret it as full original-evidence verification. No hosting.

## Visible results and controls
[Primarysummary](outputs/valuation_summary.md), [datedJSON](outputs/visible_output.json), [datedexports](outputs/dated/), [retrospectiveJSON](outputs/retrospective/visible_output.json). Defaultapp isdated; selector also retainsretrospective. Growthpathshift−5to+2pp, marginpathshift−4to+4pp are analyststressbounds. Both applyrelative toselectedbase; datedQ4stubheldfixed forOAT. Reset restores fullselectedpath, includingnonconstantmargins. Livechanges callengine and neveroverwritefrozenoutputs. Base-versus-changed statements/FCFF/checks/table/rankings visible. These bounds are not guidance/probabilities.

Real separate-copydemo adds1000 to FY2027cash, invokesactualbalancecheck, showsredfailure and untouched-copyrecovery; clearbuttonrestoresdisplay. No corruptedvalidforecast saved.

## Peer results and limits
MSFTlatestJune-endingTTM with commonJuly31price yields22.00xEV/EBIT and25.81xcommon-equity/GAAPNI. ImpliedApple236.73/227.06use same estimatedtargetdenominatorasDCF. One admittedpeer, two methoddiagnostics; not apeer-range or average. Alphabetexcluded for unresolvedconvertiblepreferred/cappedcalls/investmentgainreconciliation. Expandedpeerdistribution and pureoperatingEV/normalizedearnings remain UNCOMPLETED. [Details](docs/comparables.md).

## File map
- apple_proforma.py: existingstatementengine, now acceptsdatedopening/yearlabels/stubfraction.
- analysis.py: correctedretrospective selectedbaseline, FCFF/scenarios/sensitivities.
- dated_refresh.py: datedreported/estimated bridge, fivefullannualforecasts, DCF/peers/reverse andexports.
- app.py: thinUI callsselectedengine; tests/: originaltests plusregressions/datechecks/AppTest.
- existing_work/: protectedoriginals; reproduction/: originalLab10reproduction; archive/retrospective_v1/: priorprojectfiles/originaloutputs/documents; recovered_context/: historicalLab11records.
- sources/: officialreports/primaryrateCSV; docs/: source/challengeledgers, changes, memo, evolution, validation, exactcompletionstatus andvideooutlines.
- outputs/: primarydatedvisiblecontract, dated/ andretrospective/ exports andactualexecutionlogs.

## Conditions and unfinished requirements
Consider initiation only after supportedforecasts, independentreview and price≥20%belowdatedbase (illustrative95.68, notOctobertradelimit). Reassess on two quarters revenuegrowth<6%, refund-adjustedmargin<47%, capex/revenue>4%, changedclaims orfailedchecks. Analystreviews eachfiling; committeeownsaction. Sourceestimates, selectedreserve, highterminalreturn, flatliability/refinancingpolicy andonepeerlimitconfidence.

[Memo](docs/Decision-Memo.pdf), [research evolution](docs/Research-Evolution.pdf), [validation/AIuse](docs/validation-and-ai-use.md), three supplied transcripts in `docs/`. OriginalEditionAreceipt/lockedAI-offevidence, independentstudentreview, finalPDFs, actualrecordings/transcripts andsubmissionaccess remain incomplete. Disclosure is not completion. AIassistance: Codex(GPT-6; finerversionnotexposed), exposedexec/webtools, actualsessiondatesinlogs. No humanreview or historicalreceipt claimed.


## Package file list

- `.gitignore`
- `FILE-INVENTORY.csv`
- `README.md`
- `analysis.py`
- `app.py`
- `apple_proforma.py`
- `archive/retrospective_v1/analysis.py`
- `archive/retrospective_v1/app.py`
- `archive/retrospective_v1/apple_proforma.py`
- `archive/retrospective_v1/original_outputs/checks.csv`
- `archive/retrospective_v1/original_outputs/cold_run_first_failure.txt`
- `archive/retrospective_v1/original_outputs/cold_run_log.txt`
- `archive/retrospective_v1/original_outputs/test_run_final_validated.log`
- `archive/retrospective_v1/original_outputs/validation_results.md`
- `archive/retrospective_v1/original_outputs/valuation_summary.md`
- `archive/retrospective_v1/original_outputs/visible_output.json`
- `dated_refresh.py`
- `docs/Decision-Memo.pdf`
- `docs/Research-Evolution.pdf`
- `docs/Validation-and-AI-Use.pdf`
- `docs/assumption_challenges.csv`
- `docs/comparables.md`
- `docs/completion_status.md`
- `docs/dates_and_methods.md`
- `docs/frozen_manifest.csv`
- `docs/model_change_record.md`
- `docs/peer_policy.md`
- `docs/peer_policy_addendum.md`
- `docs/preservation_manifest.json`
- `docs/source_ledger.csv`
- `docs/submission_manifest.csv`
- `docs/supplied_inventory.csv`
- `docs/transcript-video-1.txt`
- `docs/transcript-video-2.txt`
- `docs/transcript-video-3.txt`
- `docs/validation-and-ai-use.md`
- `existing_work/lab06/Lab6_.md`
- `existing_work/lab06/dcf.py`
- `existing_work/lab07/Lab7.md`
- `existing_work/lab07/peer_pe_valuation.py`
- `existing_work/lab10/Lab_10_Apple.md`
- `existing_work/lab10/apple_forecast.csv`
- `existing_work/lab10/apple_proforma.py`
- `existing_work/lab10/apple_results.md`
- `existing_work/lab10/test_apple_proforma.py`
- `existing_work/lab11/Lab_11_Apple.md`
- `existing_work/lab11/Locked_Changed_Input_Record(1).md`
- `existing_work/lab11/base_output(1).md`
- `existing_work/lab11/base_snapshot(1).json`
- `existing_work/lab11/base_verification(1).txt`
- `existing_work/lab11/capture_base.py`
- `existing_work/lab12/Lab_12.md`
- `existing_work/research/Apple_2026-09-03_report.md`
- `existing_work/research/Project 1 Edition A.md`
- `existing_work/research/sources.md`
- `outputs/bridge_reported_vs_estimated.csv`
- `outputs/checks.csv`
- `outputs/cold_run_log.txt`
- `outputs/comparables.csv`
- `outputs/dated/bridge_reported_vs_estimated.csv`
- `outputs/dated/checks.csv`
- `outputs/dated/comparables.csv`
- `outputs/dated/failure_demo.json`
- `outputs/dated/forecast.csv`
- `outputs/dated/peer_implied.csv`
- `outputs/dated/scenario_implied_q4.csv`
- `outputs/dated/scenario_statements.csv`
- `outputs/dated/scenarios.csv`
- `outputs/dated/sensitivity.csv`
- `outputs/dated/sensitivity_deltas.csv`
- `outputs/dated/sensitivity_statements.csv`
- `outputs/dated/stub_forecast.csv`
- `outputs/dated/timing_cashflows.csv`
- `outputs/dated/valuation_summary.md`
- `outputs/dated/visible_output.json`
- `outputs/dated/wacc_growth.csv`
- `outputs/forecast.csv`
- `outputs/history_normalization.csv`
- `outputs/package_analysis_run.log`
- `outputs/package_dated_run.log`
- `outputs/package_tests.log`
- `outputs/peer_implied.csv`
- `outputs/refresh_fix_run.log`
- `outputs/refresh_tests_latest.log`
- `outputs/retrospective/valuation_summary.md`
- `outputs/retrospective/visible_output.json`
- `outputs/scenario_implied_q4.csv`
- `outputs/scenario_statements.csv`
- `outputs/scenarios.csv`
- `outputs/sensitivity.csv`
- `outputs/sensitivity_deltas.csv`
- `outputs/sensitivity_statements.csv`
- `outputs/stub_forecast.csv`
- `outputs/timing_cashflows.csv`
- `outputs/validation_results.md`
- `outputs/valuation_summary.md`
- `outputs/visible_output.json`
- `outputs/wacc_growth.csv`
- `recovered_context/base_checks.csv`
- `recovered_context/base_statements.csv`
- `recovered_context/partner_discussion_notes.md`
- `recovered_context/selected_ranges.json`
- `reproduction/apple_forecast.csv`
- `reproduction/apple_proforma.py`
- `reproduction/apple_results.md`
- `reproduction/comparison.json`
- `reproduction/run.log`
- `reproduction/test_apple_proforma.py`
- `reproduction/tests.log`
- `requirements.txt`
- `scripts/cold_run.py`
- `sources/aapl-20250927.pdf`
- `sources/aapl-20250927.txt`
- `sources/apple_fy26q3.pdf`
- `sources/apple_fy26q3.txt`
- `sources/apple_q3_release.html`
- `sources/course_abg_slides.html`
- `sources/course_abg_tutorial.md`
- `sources/curl_retrieval_log.json`
- `sources/damodaran_fcff.pdf`
- `sources/damodaran_fcff.txt`
- `sources/dated_refresh_verification.md`
- `sources/dgs10_july2026.csv`
- `sources/microsoft_ar25.html`
- `sources/msft_fy26_release.html`
- `sources/msft_fy26_release.txt`
- `sources/retrieval_log.json`
- `sources/verification_notes.md`
- `tests/test_analysis.py`
- `tests/test_app.py`
- `tests/test_refresh.py`
- `tests/test_supplied.py`
