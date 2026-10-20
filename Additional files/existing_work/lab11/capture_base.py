"""Capture only the unchanged Lab 10 base. Never runs changed assumptions."""
import csv
import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path

FOLDER = Path(__file__).resolve().parent
SOURCE = FOLDER.parent / 'Lab 10' / 'Submission' / 'apple_proforma.py'
spec = importlib.util.spec_from_file_location('apple_base', SOURCE)
model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)


def main():
    target = FOLDER / 'base_snapshot.json'
    if target.exists():
        raise SystemExit('Original snapshot already exists; refusing to overwrite it.')
    source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    rows = model.project()
    model.assert_balanced(rows)
    checks = model.check_rows(rows)
    value = model.value_equity(rows)
    previous = FOLDER.parent / 'Lab 10' / 'apple_forecast.csv'
    with previous.open() as f:
        prior = list(csv.DictReader(f))
    assert len(prior) == len(rows)
    assert set(prior[0]) == set(rows[0])
    max_difference = max(abs(float(old[k]) - row[k])
                         for old, row in zip(prior, rows) for k in row)
    assert max_difference <= model.TOLERANCE
    original_output = (FOLDER / 'base_output.md').read_text()
    assert original_output == model.render(rows) + '\n'
    saved_output_matches = (FOLDER.parent / 'Lab 10' / 'apple_results.md').read_text() == model.render(rows)
    snapshot = dict(captured_at=datetime.now(timezone.utc).isoformat(),
                    source=str(SOURCE.relative_to(FOLDER.parent)), source_sha256=source_hash,
                    years=model.YEARS, units='USD millions except USD/share',
                    assumptions=model.DEFAULTS, opening=model.OPENING, history=model.HISTORY,
                    market_price=model.MARKET_PRICE, market_timestamp=model.MARKET_TIMESTAMP,
                    rows=rows, checks=checks, valuation=value,
                    tolerance=model.TOLERANCE, previous_csv_max_difference=max_difference,
                    previous_markdown_matches=saved_output_matches)
    target.write_text(json.dumps(snapshot, indent=2, allow_nan=False) + '\n')
    for filename, data in [('base_statements.csv', rows), ('base_checks.csv', checks)]:
        with (FOLDER / filename).open('w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=list(data[0]))
            writer.writeheader()
            writer.writerows(data)
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == source_hash
    print('Base only: PASS; Lab 10 source unchanged.')
    print(f'Prior CSV maximum difference: {max_difference}; tolerance: {model.TOLERANCE} USD million.')
    print(f'Prior Markdown matches: {saved_output_matches}. Original stdout matches: True.')
    print(f'Maximum absolute accounting residual: {max(abs(v) for c in checks for k, v in c.items() if k != "year"):.12g} USD million.')
    print(f'FY2030 operating profit: {rows[-1]["operating_income"]:.6f} USD million.')
    print(f'FY2030 FCFE: {rows[-1]["fcfe"]:.6f} USD million.')
    print(f'Existing annual-base valuation: {value["per_share"]:.6f} USD/share.')
    print('Changed-input scenarios and tests: NOT RUN; independent prediction and partner review pending.')


if __name__ == '__main__':
    main()

