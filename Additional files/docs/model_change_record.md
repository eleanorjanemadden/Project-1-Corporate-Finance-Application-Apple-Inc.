# Follow-up changes — existing project retained

Earlier change records, documents and unchanged engine snapshot are in archive/retrospective_v1/. existing_work/ was never edited.

1. Fixed both revenue locators to FY25 operations p29. Revolver zero now explicitly points to model convention; removed filing-verification/availability implications.
2. Fixed analysis.run_analysis(inputs): selected inputs define base and cases.base; causal scenarios inherit other selected assumptions; OAT centers on selected growth/margin paths; WACC/g table and reverse use selected baseline; restored base is recomputed with those same assumptions. Nonconstant margin paths supported. Added regression coverage.
3. Surplus uses selected min_cash, not module default; verified5000 increase in reserve reduces equity by5000. Existing retrospective results unchanged at display precision.
4. Archived prior code/documents/original outputs without rewriting original evidence. Retrospective code remains runnable; new retrospective exports have their own path. No date-only rename.
5. Extended existing statement engine with explicit opening balances/year labels/fractional first period. New dated_refresh.py uses June27actuals, estimates FY26Q4 and July31 balance bridge, excludes elapsed FCFF and adds five full annual forecasts FY2027–2031. Both statement and bridge checks run. Added FY2031 by explicit3% base revenue-growth judgment, not a sourced fact.
6. Selected July31end-of-day decision with July31regular close. Verified Apple filing accepted06:01:02; latest quarterly balances and July17share count can be used as dated inputs. Intervening balances are estimated, not required exact observations.
7. Replaced illustrative4% risk-free component only in dated model with primary FRED/H.15 July30observation4.68%; beta1.10,ERP5.5%,debtcost5% remain assumptions. Base WACC10.6055%. Prior9.867% retrospective model stays separate.
8. Replaced stale-period MSFT comparison with July29release FY2026June figures, matched AppleTTMJune, commonJuly31prices. One enterprise/equity multiple calculated; Alphabet excluded for unresolved preferred/investment definitions. Multi-peer range not claimed.
9. Kept app thin; date-basis selector defaults to dated model; bounded shifts and reset now preserve each baseline’s nonconstant margin path. Dated failure demonstration corrupts a separate FY2027copy and invokes the actual extended accounting gate, then recovers.
10. OneDrive placeholder reads stalled old cached bytecode and original evidence. Moved old caches to archive and used fresh external venv. Preservation test now uses bounded read; unavailable evidence is a skip, never verification. Runtime cold staging copies selected runtime/source fixtures and explicitly excludes unavailable originals/archive; preservation is skipped. No human review or AI-off execution claimed.

11. Final packaging: corrected only the float-equality test to 12-decimal tolerance; reran both engines once (exit 0) and 32 tests once (31 passed, 1 skipped). Prior failure retained; no new research, installation or cold run. See outputs/validation_results.md.
