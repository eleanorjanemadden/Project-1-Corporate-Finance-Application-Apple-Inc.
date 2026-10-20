# Actual final validation results

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

Stalled prior Python test/read processes and git-status reads were terminated. Git status could not complete against OneDrive; no claim of a complete VCS diff inventory is made. Saved file pointers and scoped hashes are in docs/frozen_manifest.csv. An initial broader manifest read stalled and was stopped; the final manifest is a selected-file snapshot, not a complete repository freeze. No content reset/discard was performed. Original-content checksum verification remains incomplete; all peer/claim/human requirements in completion_status.md remain unmet. No human review, recordings, transcripts, publication or receipt was created.
