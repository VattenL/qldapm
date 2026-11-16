"""Unit tests for cost_estimate.py: the payroll arithmetic and the invariants the two forms rely on."""

import datetime as dt
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import cost_estimate as ce


class Arithmetic(unittest.TestCase):
    def test_loaded_below_ceiling_adds_23_5_percent(self):
        self.assertAlmostEqual(ce.loaded(30_000_000), 30_000_000 * 1.235)

    def test_loaded_above_ceiling_caps_the_capped_share(self):
        gross = 60_000_000
        self.assertAlmostEqual(ce.loaded(gross), gross + 0.225 * ce.CAP + 0.01 * gross)

    def test_rates_round_to_thousands(self):
        for role in list(ce.RATES.values()) + list(ce.SENIOR_RATES.values()):
            self.assertEqual(role.rate % 1000, 0)
        self.assertEqual(ce.RATES["DEV"].rate, 157_000)
        self.assertEqual(ce.SENIOR_RATES["DEV"].rate, 266_000)

    def test_cone_weighting(self):
        self.assertAlmostEqual(ce.CONE_E, (0.67 + 4 + 1.5) / 6)
        self.assertEqual(ce.factor(1), 1.0)

    def test_payroll_months_counts_whole_and_part_months(self):
        self.assertAlmostEqual(ce.payroll_months(dt.date(2026, 10, 1), dt.date(2026, 10, 31)), 1.0)
        half = ce.payroll_months(dt.date(2026, 10, 1), dt.date(2026, 10, 15))
        self.assertTrue(0.4 < half < 0.6)

    def test_billed_months_is_inclusive(self):
        self.assertEqual(ce.billed_months(dt.date(2026, 9, 20), dt.date(2027, 3, 19)), 7)

    def test_item_with_uncertain_quantity_weights_the_quantity(self):
        item = ce.Item("1.5.4.3", "1.5.4", "Software", "Other Direct Costs", 2, "x", "x",
                       (1000,) * 3, (750, 1500, 3000), ())
        self.assertEqual(item.expected, 1_625_000)
        self.assertEqual(item.amounts(), (750_000, 1_500_000, 3_000_000))


class Scope(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.hours = ce.read_scope(ce.SCOPE)

    def test_deferred_packages_exist_in_the_dictionary(self):
        for wp in ce.DEFERRED:
            self.assertIn(wp, self.hours)

    def test_scaling_only_shrinks(self):
        for f in ce.scope_scale(self.hours, set(ce.DEFERRED)).values():
            self.assertTrue(0 < f <= 1)

    def test_full_scope_scales_only_the_lean_packages(self):
        self.assertEqual(set(ce.scope_scale(self.hours, set())), set(ce.LEAN))

    def test_coverage_never_counts_assurance_as_build_work(self):
        for wp in ce.build_packages(self.hours):
            self.assertTrue(wp.startswith(ce.BUILD_PREFIXES))
            self.assertNotIn(wp, ce.COVERS)


class Invariants(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.hours = ce.read_scope(ce.SCOPE)
        cls.est, cls.full, cls.senior = ce.estimates(cls.hours)

    def test_estimate_meets_the_target(self):
        self.assertLess(self.est.total(), ce.TARGET)

    def test_full_scope_does_not(self):
        self.assertGreater(self.full.total(), ce.CHARTER_TOTAL)

    def test_deferred_work_is_not_costed(self):
        cas = {a.ca for a in self.est.accounts}
        for ca in ("1.4.4", "1.5.4", "1.9.1"):
            self.assertNotIn(ca, cas)

    def test_budget_lines_add_up_to_the_total(self):
        for e in (self.est, self.full, self.senior):
            self.assertEqual(sum(e.budget_lines()), e.total())

    def test_range_brackets_the_estimate(self):
        self.assertLessEqual(self.est.low, self.est.total())
        self.assertLessEqual(self.est.total(), self.est.high)

    def test_timesheets_charge_no_idle_time(self):
        self.assertEqual(self.est.idle(), 0)
        self.assertEqual(self.est.thirteenth(), 0)

    def test_monthly_pay_charges_idle_time_unless_hours_overflow(self):
        self.assertGreater(self.senior.idle(), 0)
        self.assertEqual(self.senior.idle(2), 0)

    def test_reduced_work_does_not_lengthen_the_window(self):
        self.assertLessEqual(self.est.m7, self.full.m7)

    def test_build_renders_without_em_dash(self):
        md = ce.build(self.est, self.full)
        self.assertNotIn(chr(0x2014), md)
        self.assertIn("#### ACTIVITY COST ESTIMATES, page 1 of 1", md)
        cr = ce.build_cr(self.est, self.full, self.senior)
        self.assertNotIn(chr(0x2014), cr)


if __name__ == "__main__":
    unittest.main()
