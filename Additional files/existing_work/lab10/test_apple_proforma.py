"""Meaningful accounting/refusal tests. Run: python3 -m unittest -v test_apple_proforma.py"""
import copy
import unittest
import apple_proforma as model


class AppleChecks(unittest.TestCase):
    def setUp(self):
        self.rows = model.project()

    def test_base_case_balances_and_has_positive_fcfe(self):
        model.assert_balanced(self.rows)
        self.assertTrue(all(r['fcfe'] > 0 for r in self.rows))
        self.assertTrue(all(r['cash'] >= 30000 for r in self.rows))
        self.assertAlmostEqual(model.balance_gap(model.OPENING), 0)
        self.assertGreater(model.value_equity(self.rows)['per_share'], 0)

    def test_typed_cash_refuses_even_without_updating_cached_totals(self):
        self.rows[0]['cash'] = model.OPENING['cash']
        with self.assertRaisesRegex(ValueError, 'FY2026: balance gap'):
            model.value_equity(self.rows)

    def test_vendor_receivable_omission_from_cash_flow_refuses(self):
        amount = self.rows[0]['change_vendor_receivables']
        # Make the balance sheet tie despite an omitted operating cash outflow:
        # the independent CFO reconciliation must still catch the error.
        for key in ('cfo', 'fcfe', 'cash', 'assets', 'equity'):
            self.rows[0][key] += amount
        with self.assertRaisesRegex(ValueError, 'FY2026: cfo gap'):
            model.value_equity(self.rows)

    def test_ppe_error_hidden_by_offsetting_other_asset_refuses(self):
        self.rows[0]['ppe'] += 100
        self.rows[0]['other_assets'] -= 100
        with self.assertRaisesRegex(ValueError, 'FY2026: ppe gap'):
            model.value_equity(self.rows)

    def test_cash_floor_refuses_even_though_balance_sheet_balances(self):
        args = dict(buyback=95000.)
        rows = model.project(args)
        self.assertAlmostEqual(model.balance_gap(rows[0]), 0, places=6)
        with self.assertRaisesRegex(ValueError, 'cash_floor_shortfall'):
            model.value_equity(rows, args)

    def test_terminal_growth_must_be_below_discount_rate(self):
        for g in (.10, .11):
            with self.assertRaisesRegex(ValueError, 'Terminal growth'):
                model.value_equity(self.rows, dict(terminal_growth=g))

    def test_nan_refuses(self):
        self.rows[2]['cash'] = float('nan')
        with self.assertRaisesRegex(ValueError, 'FY2028: cash is not finite'):
            model.value_equity(self.rows)

    def test_cash_distributions_do_not_create_value(self):
        # A different payout changes cash and equity, not pre-distribution FCFE.
        args = dict(buyback=60000.)
        alternative = model.project(args)
        self.assertAlmostEqual(model.value_equity(self.rows)['per_share'],
                               model.value_equity(alternative, args)['per_share'])
        self.assertGreater(alternative[-1]['cash'], self.rows[-1]['cash'])

    def test_larger_rd_reduces_value(self):
        args = dict(rd_ratio=.105)
        alternative = model.project(args)
        self.assertLess(model.value_equity(alternative, args)['per_share'],
                        model.value_equity(self.rows)['per_share'])

    def test_missing_year_refuses(self):
        with self.assertRaisesRegex(ValueError, 'All five'):
            model.value_equity(self.rows[:-1])


if __name__ == '__main__':
    unittest.main()
