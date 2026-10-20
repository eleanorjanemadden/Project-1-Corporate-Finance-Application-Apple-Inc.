# Validation and AI Use — follow-up

## Scope, dates and environment
Primary July31,2026end-of-day17:00EDT investment assessment, using16:00close. Recorded execution date is in tool/test/cold logs; this is not a historical precommit. Retrospective model and prior AI/validation records preserved in archive/retrospective_v1/. Existing_work unchanged by editing actions. Python3.13.1 and requirements unchanged; fresh environment used outside OneDrive for this rerun. No new commit/push/publication.

## Load-bearing evidence and conventions
Source_ledger.csv identifies every reported opening field, share measurement date, source availability, proxy transformation and assumption. Apple filing indexacceptedJuly31 06:01:02 establishes cover-share availability before close. June27actuals anchor model;July31balances are interpolation estimates. Primary July30DGS10 4.68% downloaded; beta/ERP/debtcost remain assumed. Market quotes are dated secondary unadjusted closes; adjusted alternatives rejected. MSFTrelease downloaded; SEC directcurl403 while web tool returned filing/index, recorded without pretending all files downloaded. Dates_and_methods.md details prorating, working-capital balance proxies, cash-equivalentSBC, dilution proxy and bridge.

## Validation register

| Check | Actual method/evidence | Limitation/status |
|---|---|---|
| Revenue/revolver provenance | test_ledger_fact_assumption_separation; actual p29 operations locator and assumption text | Reported zero revolver not asserted |
| Selected baseline | Nondefault GM/R&D/capex/shares/mincash; recompute every OATdelta and WACCcell; compare cases.base | Regression tests execute; no default-base mixing |
| Cash reserve | Min_cash+5000 reduces surplus/equity5000 in both models | No hidden module-default floor |
| Reported source anchor | June27assets383266/liabilities275746; source inputs checked | Dated reported balances, not July31measured |
| Forecast and stub | Existing checks extended to explicit opening/year labels; FCFF two routes; all cases | Q4calendar/seasonality are estimates |
| Elapsed flows/timing | Stubsplit sums to full Q4FCFF;57/365firsttime; five full years beyond; independentPV recomputation | No elapsedFY26whole-year cash retained |
| EV/equity | Estimated bridge balances; EV+surplus−debt; selectedreserve; no futurecash addition | Detailed incremental claims remain uncompleted |
| DCF boundaries/directions | WACC/g refusal and monotonicity, signed flows retained, reverse reprices308.91 | Reverse fixes base bridge; future buyback changes cannot rewrite elapsed cash |
| Peer definitions | July31close, JuneendingTTM, GAAPEBIT/NI, correctbookdebt/cash sums | One peer; strategic-equity/earnings-quality limits disclosed, no fake peer range |
| Product | AppTest operates defaultdatedcontrols/reset, lower margin and real failure/recovery | No browser/human recording asserted |
| Frozen output | Both datedJSONpaths equal new engine; retrospectivecontract equals corrected engine | Regenerate both after edits |
| Published training and prior finance tests | Existing ABGroundedknownanswer, FCFF definition, accounting/refusal tests retained | Ordinary assisted validation, no human AI-off claim |
| Preservation | Bounded subprocess attempts original checksum manifest and every protected file | Timeout producesSKIP with exactpath, notPASS. Prior successful hash record is historical only |
| Cold run | Fresh venv; selected runtime/source fixtures copied, originals/archive excluded; compare generated contract hashes; local HTTP health | Any skipped original-content read remains unverified. No complete-copy or human-access claim |

Final packaging outcomes are in outputs/package_tests.log and the two package engine logs; the earlier runtime-only cold evidence is in outputs/cold_run_log.txt. Failed/stalled attempts are retained in outputs/refresh_tests_first.log/second.log and original archived logs. First test attempts stalled on OneDrive-backed originals and old bytecode; old caches moved aside, no original evidence overwritten. A15second preservation-read boundary now yields an explicit skip if unavailable. No financial result changed merely to force a pass.

## Human locked record and boundary
Unchanged supplied locked record contains a student prediction/AI-closure confirmation claim but lacks original immutable pre-run timestamp/commit. It is not authenticated here. Current model changes, tests and demonstration are AI-assisted ordinary validation. Original EditionA receipt remains unverified. No prediction, receipt, timestamp, human review or historical authorship has been fabricated.

## Material AI-use register
Exposed surface: Codex, GPT-6; finer model version not exposed. Toolsfunctions.exec/exec_command/write_stdin andweb.run. Session work: code fixes, source inspection, dated modeling/assumptions, peer screening/calculation, regression tests and document/video-outline preparation. Newprimaryrate modified preliminary datedbase130.32 to final119.60. Assistant accepted baseline/cash fixes after regression calculations; modified date method to reportedopening+estimatedstub/bridge; rejected stale annual peers and unreconciled Alphabet metrics. These are assistant dispositions, not the student's independent decisions. Student review/dispositions still pending.

## Remaining limitations and conditions
See completion_status.md: multi-peer distribution, detailed claims/normalized earnings, human source review, EditionA/locked record, finalPDFs/media/access/submission and any skipped checksum verification remain UNMET. The dated model itself is implemented; estimates do not become reported facts. Base119.60, low78.52,high181.30; terminalshare68.91%. Watch/defer at308.91 subject to stated assumptions, not a currentOctoberclaim.

## Submission packaging check — October 19, 2026 (local)
Research and feature work stopped at the user's request. Final saved code is the existing engine plus dated_refresh.py, with corrected retrospective baseline/reserve handling. The last correction changed only a risk-free source test from exact float equality to a 12-decimal tolerance and closed its input file; no valuation formula changed.

Executed once using the already installed local environment (no installation or new cold run):
```sh
/tmp/apple-project-refresh-venv/bin/python -B analysis.py > outputs/package_analysis_run.log 2>&1
/tmp/apple-project-refresh-venv/bin/python -B dated_refresh.py > outputs/package_dated_run.log 2>&1
/tmp/apple-project-refresh-venv/bin/python -B -m unittest discover -s tests -v > outputs/package_tests.log 2>&1
```
All three commands exited 0. Tests: 32 run in 16.181 seconds; 31 passed, 1 skipped. Exact skip: `OneDrive read unavailable; preservation NOT reverified: READ existing_work/lab06/dcf.py`. A non-fatal ResourceWarning remains for an unclosed ledger input in test_refresh.py; it is recorded, not concealed.

The preceding failed run is retained in outputs/refresh_tests_latest.log: 32 tests, one failure and one skip. Failure: test_refresh.RefreshChecks.test_risk_free_observation_and_wacc, `AssertionError: 0.046799999999999994 != 0.0468`. The tolerance correction addresses binary floating-point representation; financial inputs and results were unchanged.

Final saved dated low/base/high: $78.52 / $119.60 / $181.30, July 31, 2026 end-of-day assessment against $308.91 close. Retrospective low/base/high: $72.74 / $125.23 / $172.33. Root visible_output.json and outputs/dated/ are primary; outputs/retrospective/ remains separate. No October current valuation is claimed.

Earlier cold_run_log.txt is a runtime-only check: selected runtime/source fixtures copied to a fresh environment; original evidence/archive excluded and preservation explicitly skipped. It ran the then-current 29 tests (28 passed, 1 skipped), regenerated matching contracts and received local HTTP health 200. It predates the last test additions/correction and is not a final full-repository cold run. No cold run was repeated for packaging.

Stalled prior Python test/read processes and git-status reads were terminated. Git status could not complete against OneDrive; no claim of a complete VCS diff inventory is made. Saved file pointers and scoped hashes are in docs/frozen_manifest.csv. An initial broader manifest read also stalled on OneDrive and was stopped; the final manifest intentionally hashes only selected active, readable files. It is not a complete repository freeze. No content reset/discard was performed. Original-content checksum verification remains incomplete; all peer/claim/human requirements in completion_status.md remain unmet. No human review, recordings, transcripts, publication or receipt was created.
