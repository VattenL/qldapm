"""Tests for pm_calc.py. Run: uv run --with pytest pytest -q .claude/skills/pm/scripts

Worked examples come from the books where the books print them: Book of Forms
forms 2.17 and 2.21, PMBOK 6 Figure 11-5 and Figure 11-15. The books print no
numbers for earned value, so those cases are worked by hand from the formulas
of PMBOK 6 Table 7-1.
"""

import contextlib
import io
import json
import unittest
from decimal import Decimal
from pathlib import Path

import pm_calc as pc


def values(result):
    """Every row of a result as {label: value}, one dict per section title."""
    return {sec["title"]: {r["label"]: r["value"] for r in sec["rows"]} for sec in result["sections"]}


def flat(result):
    out = {}
    for sec in result["sections"]:
        for r in sec["rows"]:
            out[r["label"]] = r["value"]
    return out


def cli(*argv):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = pc.main(list(argv))
    return code, out.getvalue(), err.getvalue()


class BookExamples(unittest.TestCase):
    def test_form_2_17_parametric_duration_125_hours(self):
        # Table 2.16, PDF page 86 (printed page 75): 150 / (2 x .75 x .8) = 125 hours
        res = pc.effort_to_duration(150, 2, 0.75, 0.8)
        self.assertAlmostEqual(flat(res)["Duration estimate"], 125.0)

    def test_form_2_17_analogous_deck_12_5_days(self):
        # Table 2.16, PDF page 86 (printed page 75): 200/160 = 1.25 and 10 days x 1.25 = 12.5 days
        res = pc.analogous(10, 160, 200)
        self.assertAlmostEqual(flat(res)["Multiplier"], 1.25)
        self.assertAlmostEqual(flat(res)["Estimate"], 12.5)

    def test_form_2_17_beta_26_days(self):
        # Table 2.16, PDF page 87 (printed page 76): (20 + 4(25) + 36) / 6, expected duration 26 days
        self.assertAlmostEqual(flat(pc.pert(20, 25, 36))["Beta mean"], 26.0)

    def test_form_2_17_triangular_on_the_same_sample(self):
        # PMBOK 6 section 6.4.2.4 formula applied to the form 2.17 sample, (20 + 25 + 36) / 3
        self.assertAlmostEqual(flat(pc.pert(20, 25, 36))["Triangular mean"], 27.0)

    def test_form_2_21_analogous_deck_6250(self):
        # Table 2.19, PDF page 100 (printed page 89): $5,000 x 1.25 = $6,250
        self.assertAlmostEqual(flat(pc.analogous(5000, 160, 200))["Estimate"], 6250.0)

    def test_form_2_21_beta_5250(self):
        # Table 2.19, PDF page 100 (printed page 89): (4,000 + 4(5,000) + 7,500) / 6 = $5,250
        self.assertAlmostEqual(flat(pc.pert(4000, 5000, 7500))["Beta mean"], 5250.0)

    def test_figure_11_15_decision_tree(self):
        # PMBOK 6 Figure 11-15, printed page 435 (PDF page 474): Build 36, Upgrade 46, decision 46
        options = [("Build", 120.0, [(0.6, 200.0), (0.4, 90.0)]),
                   ("Upgrade", 50.0, [(0.6, 120.0), (0.4, 60.0)])]
        res = pc.emv([], options)
        got = flat(res)
        self.assertAlmostEqual(got["EMV of Build"], 36.0)
        self.assertAlmostEqual(got["EMV of Upgrade"], 46.0)
        self.assertAlmostEqual(got["Decision EMV"], 46.0)
        self.assertEqual([r["value"] for r in res["sections"][0]["rows"][:2]], [80.0, -30.0])

    def test_figure_11_15_branch_expression(self):
        # the figure prints $36M = .60 ($80M) + .40 (-$30M)
        self.assertAlmostEqual(flat(pc.emv([(0.6, 80.0), (0.4, -30.0)], []))["EMV"], 36.0)

    def test_figure_11_5_printed_scores(self):
        # PMBOK 6 Figure 11-5, printed page 408 (PDF page 447), threats side, rows very high down to very low
        printed = [["0.05", "0.09", "0.18", "0.36", "0.72"],
                   ["0.04", "0.07", "0.14", "0.28", "0.56"],
                   ["0.03", "0.05", "0.10", "0.20", "0.40"],
                   ["0.02", "0.03", "0.06", "0.12", "0.24"],
                   ["0.01", "0.01", "0.02", "0.04", "0.08"]]
        self.assertEqual([[str(c) for c in r] for r in pc.figure_grid()], printed)

    def test_figure_11_5_score_of_a_risk(self):
        res = pc.risk_score("high", "very high", "pmbok")
        self.assertAlmostEqual(flat(res)["Score"], 0.56)
        self.assertAlmostEqual(flat(pc.risk_score("0.3", "0.4", "pmbok"))["Score"], 0.12)


class ProbabilityImpactRating(unittest.TestCase):
    # Form 2.35 blank, PDF page 154 (printed page 143), tones read from the page. Rows are
    # very high down to very low, columns very low to very high. dark = 3, mid = 2, light or white = 1.
    TONES = [[2, 2, 3, 3, 3],
             [2, 2, 2, 3, 3],
             [1, 2, 2, 2, 3],
             [1, 1, 2, 2, 2],
             [1, 1, 1, 2, 2]]
    WORD = {3: "H", 2: "M", 1: "L"}

    def test_table_2_31_rules_reproduce_the_printed_shading_of_form_2_35(self):
        # Table 2.31 (printed pages 138 to 139) written as rules, against the tones printed on form 2.35
        expected = [[self.WORD[t] for t in row] for row in self.TONES]
        got = [[c[0] for c in row] for row in pc.rating_grid()]
        self.assertEqual(got, expected)

    def test_every_cell_gets_exactly_one_rating(self):
        for p in range(5):
            for i in range(5):
                self.assertIn(pc.rating(p, i), ("High", "Medium", "Low"))

    def test_named_rules_of_table_2_31(self):
        self.assertEqual(pc.rating(2, 4), "High")      # medium probability and very high impact
        self.assertEqual(pc.rating(3, 3), "High")      # high and high
        self.assertEqual(pc.rating(4, 2), "High")      # very high and medium
        self.assertEqual(pc.rating(0, 3), "Medium")    # very low and high
        self.assertEqual(pc.rating(1, 2), "Medium")    # low and medium
        self.assertEqual(pc.rating(4, 1), "Medium")    # very high and low
        self.assertEqual(pc.rating(2, 0), "Low")       # medium and very low
        self.assertEqual(pc.rating(1, 1), "Low")       # low and low
        self.assertEqual(pc.rating(0, 2), "Low")       # very low and medium

    def test_level_words_and_codes(self):
        res = pc.risk_score("VH", "very-low", "rating")
        self.assertEqual(flat(res)["Risk rating"], "Medium")

    def test_percent_bands_of_table_2_31(self):
        # printed page 138: 1 to 20 very low, 21 to 40 low, 41 to 60 medium, 61 to 80 high, 80 or greater very high
        for text, level in (("1%", 0), ("20%", 0), ("21%", 1), ("40%", 1), ("41%", 2), ("60%", 2),
                            ("61%", 3), ("79%", 3), ("81%", 4), ("100%", 4)):
            self.assertEqual(pc.probability_level(text), level, text)

    def test_eighty_percent_is_printed_in_two_bands(self):
        with self.assertRaises(pc.CalcError) as ctx:
            pc.probability_level("80%")
        self.assertIn("two bands", str(ctx.exception))

    def test_percent_outside_the_bands_or_fractional_is_refused(self):
        for text in ("0%", "101%", "20.5%"):
            with self.assertRaises(pc.CalcError, msg=text):
                pc.probability_level(text)

    def test_bad_level_word(self):
        with self.assertRaises(pc.CalcError):
            pc.risk_score("often", "high", "rating")

    def test_doubling_scale_of_the_2_35_tip(self):
        # printed page 142: Very Low .5, Low 1, Medium 2, High 4, Very High 8
        res = pc.risk_score("0.5", "high", "doubling")
        self.assertAlmostEqual(flat(res)["Impact value"], 4.0)
        self.assertAlmostEqual(flat(res)["Score"], 2.0)
        with self.assertRaises(pc.CalcError):
            pc.risk_score("high", "high", "doubling")

    def test_matrix_prints_five_rows(self):
        res = pc.matrix("rating")
        self.assertEqual(len(res["matrix"]["rows"]), 5)
        self.assertEqual(res["matrix"]["rows"][0], ["Very High", "M", "M", "H", "H", "H"])


class EarnedValue(unittest.TestCase):
    # No worked numbers are printed in the books; these are hand calculations from Table 7-1.
    # BAC 1000, PV 400, EV 350, AC 450.
    def setUp(self):
        self.res = pc.evm(1000, 400, 350, 450)
        self.by = values(self.res)
        self.base = self.by["Variances and indexes (no assumption beyond the inputs)"]

    def test_variances_and_indexes(self):
        self.assertAlmostEqual(self.base["CV"], -100)
        self.assertAlmostEqual(self.base["SV"], -50)
        self.assertAlmostEqual(self.base["CPI"], 350 / 450)
        self.assertAlmostEqual(self.base["SPI"], 350 / 400)

    def test_percents_of_form_4_4(self):
        self.assertAlmostEqual(self.base["Percent planned"], 40)
        self.assertAlmostEqual(self.base["Percent earned (percent complete)"], 35)
        self.assertAlmostEqual(self.base["Percent spent"], 45)

    def test_status_words_of_table_7_1(self):
        rows = {r["label"]: r["status"] for r in self.res["sections"][0]["rows"]}
        self.assertEqual(rows["CV"], "over planned cost")
        self.assertEqual(rows["SV"], "behind schedule")
        self.assertEqual(rows["CPI"], "over planned cost")
        self.assertEqual(rows["SPI"], "behind schedule")
        good = {r["label"]: r["status"] for r in pc.evm(1000, 400, 500, 450)["sections"][0]["rows"]}
        self.assertEqual(good["CV"], "under planned cost")
        self.assertEqual(good["SV"], "ahead of schedule")
        even = {r["label"]: r["status"] for r in pc.evm(1000, 400, 400, 400)["sections"][0]["rows"]}
        self.assertEqual(even["CV"], "on planned cost")
        self.assertEqual(even["SPI"], "on schedule")

    def test_three_eac_variants(self):
        cpi, spi = 350 / 450, 350 / 400
        self.assertAlmostEqual(self.by["EAC at the present CPI"]["EAC"], 1000 / cpi)
        self.assertAlmostEqual(self.by["EAC at the budgeted rate"]["EAC"], 450 + (1000 - 350))
        self.assertAlmostEqual(self.by["EAC with CPI and SPI"]["EAC"], 450 + (1000 - 350) / (cpi * spi))

    def test_etc_and_vac_follow_each_eac(self):
        for title in ("EAC at the present CPI", "EAC at the budgeted rate", "EAC with CPI and SPI"):
            sec = self.by[title]
            self.assertAlmostEqual(sec["ETC"], sec["EAC"] - 450)
            self.assertAlmostEqual(sec["VAC"], 1000 - sec["EAC"])

    def test_cpi_eac_equals_ac_plus_remaining_work_at_that_cpi(self):
        # BAC / CPI = AC + (BAC - EV) / CPI because AC = EV / CPI
        cpi = 350 / 450
        self.assertAlmostEqual(self.by["EAC at the present CPI"]["EAC"], 450 + (1000 - 350) / cpi)

    def test_both_index_eac_equals_cpi_eac_when_spi_is_one(self):
        by = values(pc.evm(1000, 350, 350, 450))
        self.assertAlmostEqual(by["EAC with CPI and SPI"]["EAC"], by["EAC at the present CPI"]["EAC"])

    def test_tcpi_to_bac_and_to_eac(self):
        self.assertAlmostEqual(self.by["TCPI to complete on plan"]["TCPI to BAC"], (1000 - 350) / (1000 - 450))
        self.assertAlmostEqual(self.by["EAC at the budgeted rate"]["TCPI to this EAC"], 1.0)
        eac = self.by["EAC at the present CPI"]["EAC"]
        self.assertAlmostEqual(self.by["EAC at the present CPI"]["TCPI to this EAC"],
                               (1000 - 350) / (eac - 450))

    def test_tcpi_words(self):
        rows = {r["label"]: r["status"] for r in self.res["sections"][1]["rows"]}
        self.assertEqual(rows["TCPI to BAC"], "harder to complete")
        self.assertEqual(pc.tcpi_state(1.0), "same to complete")
        self.assertEqual(pc.tcpi_state(0.5), "easier to complete")

    def test_bottom_up_and_approved_eac(self):
        res = pc.evm(1000, 400, 350, 450, bottom_up_etc=800, approved_eac=1200)
        by = values(res)
        self.assertAlmostEqual(by["EAC bottom-up"]["EAC"], 1250)
        self.assertAlmostEqual(by["EAC bottom-up"]["ETC"], 800)
        self.assertAlmostEqual(by["EAC approved"]["VAC"], -200)
        self.assertAlmostEqual(by["EAC approved"]["TCPI to this EAC"], 650 / 750)

    def test_every_eac_names_its_assumption(self):
        for sec in self.res["sections"][2:]:
            self.assertTrue(sec["rows"][0]["assumption"], sec["title"])

    def test_zero_actual_cost_is_not_computable(self):
        res = pc.evm(100, 0, 0, 0)
        by = values(res)
        self.assertIsNone(by["Variances and indexes (no assumption beyond the inputs)"]["CPI"])
        self.assertIsNone(by["Variances and indexes (no assumption beyond the inputs)"]["SPI"])
        self.assertIsNone(by["EAC at the present CPI"]["EAC"])
        self.assertIsNone(by["EAC with CPI and SPI"]["EAC"])
        self.assertAlmostEqual(by["EAC at the budgeted rate"]["EAC"], 100)

    def test_no_funds_left_has_no_tcpi(self):
        res = pc.evm(100, 100, 80, 100)
        self.assertIsNone(values(res)["TCPI to complete on plan"]["TCPI to BAC"])

    def test_ev_above_bac_is_flagged(self):
        notes = " ".join(pc.evm(100, 100, 120, 100)["notes"])
        self.assertIn("EV is above BAC", notes)

    def test_negative_input_refused(self):
        with self.assertRaises(pc.CalcError):
            pc.evm(100, -1, 0, 0)


class Estimating(unittest.TestCase):
    def test_standard_deviation_is_not_stated(self):
        row = [r for r in pc.pert(1, 2, 3)["sections"][0]["rows"] if r["label"] == "Standard deviation"][0]
        self.assertIsNone(row["value"])
        self.assertIn("not stated in the book", row["why"])

    def test_pert_order_warning(self):
        self.assertTrue(pc.pert(30, 25, 20)["notes"][0].startswith("The inputs are not in the order"))

    def test_availability_forms(self):
        self.assertAlmostEqual(pc.parse_share("75%", "availability"), 0.75)
        self.assertAlmostEqual(pc.parse_share("0.75", "availability"), 0.75)
        self.assertAlmostEqual(pc.parse_share("1", "availability"), 1.0)
        with self.assertRaises(pc.CalcError):
            pc.parse_share("75", "availability")

    def test_effort_rejects_zero_resources(self):
        with self.assertRaises(pc.CalcError):
            pc.effort_to_duration(10, 0, 1, 1)

    def test_productive_note_is_quoted_with_the_page(self):
        notes = " ".join(pc.effort_to_duration(150, 2, 0.75, 0.8)["notes"])
        self.assertIn("about 75 percent of the time", notes)
        self.assertIn("PDF page 84 (printed page 73)", notes)

    def test_bottom_up_sum_and_omitted_parts(self):
        res = pc.bottom_up(40, 50, material=300, reserve=100)
        self.assertAlmostEqual(flat(res)["Total labor"], 2000)
        self.assertAlmostEqual(flat(res)["Estimate"], 2400)
        self.assertIn("Supplies", res["notes"][1])
        self.assertNotIn("Material", res["notes"][1])


class Selection(unittest.TestCase):
    def test_weighted_score_and_winner(self):
        res = pc.weighted_score([30, 20, 50], [[4, 3, 5], [3, 5, 4]], ["A", "B"], 5)
        got = values(res)
        self.assertAlmostEqual(got["A"]["Total"], 0.3 * 4 + 0.2 * 3 + 0.5 * 5)
        self.assertAlmostEqual(got["B"]["Total"], 0.3 * 3 + 0.2 * 5 + 0.5 * 4)
        self.assertTrue(any("A with" in n for n in res["notes"]))

    def test_weights_must_total_100_percent(self):
        with self.assertRaises(pc.CalcError) as ctx:
            pc.weighted_score([30, 20, 40], [[1, 2, 3]], None, None)
        self.assertIn("100 percent", str(ctx.exception))

    def test_rating_outside_chosen_range(self):
        with self.assertRaises(pc.CalcError):
            pc.weighted_score([50, 50], [[1, 6]], None, 5)

    def test_count_mismatch(self):
        with self.assertRaises(pc.CalcError):
            pc.weighted_score([50, 50], [[1, 2, 3]], None, None)

    def test_tie_is_reported_without_a_rule(self):
        res = pc.weighted_score([50, 50], [[2, 4], [4, 2]], ["A", "B"], None)
        self.assertTrue(any("tie" in n for n in res["notes"]))

    def test_emv_probabilities_not_adding_to_one_are_noted(self):
        res = pc.emv([(0.5, 10.0), (0.3, 20.0)], [])
        self.assertTrue(any("not 1" in n for n in res["notes"]))

    def test_emv_parse_outcome_percent(self):
        self.assertEqual(pc.parse_outcome("60%:80"), (0.6, 80.0))
        with self.assertRaises(pc.CalcError):
            pc.parse_outcome("6:80")

    def test_channels(self):
        for people, expected in ((1, 0), (2, 1), (5, 10), (10, 45)):
            self.assertEqual(flat(pc.comms_channels(people))["Channels"], expected)
        with self.assertRaises(pc.CalcError):
            pc.comms_channels(0)

    def test_channels_says_the_formula_is_not_in_the_book(self):
        res = pc.comms_channels(5)
        self.assertIn("not stated in the book", res["sections"][0]["rows"][0]["cite"])


class CommandLine(unittest.TestCase):
    def test_text_output_cites_both_page_numbers(self):
        code, out, _err = cli("evm", "--bac", "1000", "--pv", "400", "--ev", "350", "--ac", "450")
        self.assertEqual(code, 0)
        self.assertIn("PDF page 301", out)
        self.assertIn("printed page 262", out)
        self.assertIn("over planned cost", out)

    def test_json_output_parses(self):
        code, out, _err = cli("pert", "--o", "20", "--m", "25", "--p", "36", "--json")
        self.assertEqual(code, 0)
        data = json.loads(out)
        self.assertAlmostEqual(data["sections"][0]["rows"][0]["value"], 26.0)

    def test_matrix_flag(self):
        code, out, _err = cli("risk-score", "--matrix")
        self.assertEqual(code, 0)
        self.assertIn("Very High", out)

    def test_risk_score_needs_both_inputs(self):
        code, _out, err = cli("risk-score", "--probability", "high")
        self.assertEqual(code, 2)
        self.assertIn("--impact", err)

    def test_bad_input_exits_2_with_a_reason(self):
        code, _out, err = cli("weighted-score", "--weights", "60", "30", "--scores", "1", "2")
        self.assertEqual(code, 2)
        self.assertIn("100 percent", err)

    def test_option_syntax(self):
        code, out, _err = cli("emv", "--option", "Build", "120", "0.6:200", "0.4:90",
                              "--option", "Upgrade", "50", "0.6:120", "0.4:60")
        self.assertEqual(code, 0)
        self.assertIn("option Upgrade", out)

    def test_no_dashes_or_emoji_in_source_or_output(self):
        source = Path(pc.__file__).read_text(encoding="utf-8")
        outputs = [source]
        for argv in (("evm", "--bac", "10", "--pv", "5", "--ev", "4", "--ac", "6"),
                     ("pert", "--o", "1", "--m", "2", "--p", "3"),
                     ("risk-score", "--matrix"), ("risk-score", "--matrix", "--scale", "pmbok"),
                     ("comms-channels", "--people", "4")):
            outputs.append(cli(*argv)[1])
        for text in outputs:
            for ch in text:
                self.assertNotIn(ch, "–—", "en or em dash")
                self.assertLess(ord(ch), 0x2190, "non-ASCII symbol %r" % ch)

    def test_decimal_import_used_for_figure_rounding(self):
        self.assertEqual(pc.figure_round(Decimal("0.015")), Decimal("0.02"))
        self.assertEqual(pc.figure_round(Decimal("0.045")), Decimal("0.05"))


class BookCheckedEdges(unittest.TestCase):
    """Cases found by checking the tool against the printed pages."""

    def test_tcpi_table_7_1_words_are_the_printed_ones(self):
        # PMBOK 6 Table 7-1, printed page 267 (PDF page 306): CV and CPI use "planned cost" wording
        res = pc.evm(1000, 400, 350, 450)
        rows = {r["label"]: r["status"] for r in res["sections"][0]["rows"]}
        self.assertEqual(rows["CV"], "over planned cost")
        self.assertEqual(rows["CPI"], "over planned cost")

    def test_zero_ac_says_which_index_is_missing(self):
        res = pc.evm(100, 50, 30, 0)
        rows = {sec["title"]: sec["rows"][0] for sec in res["sections"][2:]}
        self.assertIn("AC is zero", rows["EAC at the present CPI"]["why"])
        self.assertIn("AC is zero", rows["EAC with CPI and SPI"]["why"])
        self.assertIsNone(rows["EAC at the budgeted rate"]["why"])

    def test_zero_ev_makes_cpi_zero_not_missing(self):
        res = pc.evm(100, 50, 0, 20)
        rows = {sec["title"]: sec["rows"][0] for sec in res["sections"][2:]}
        self.assertIn("CPI is zero", rows["EAC at the present CPI"]["why"])
        self.assertIsNone(rows["EAC at the present CPI"]["value"])

    def test_zero_pv_blocks_only_the_cpi_spi_variant(self):
        # CPI = 30/20 is fine, SPI = 30/0 is not
        by = values(pc.evm(100, 0, 30, 20))
        self.assertAlmostEqual(by["EAC at the present CPI"]["EAC"], 100 / 1.5)
        self.assertIsNone(by["EAC with CPI and SPI"]["EAC"])

    def test_both_index_eac_by_hand(self):
        # BAC 1000, PV 400, EV 350, AC 450: CPI 7/9, SPI 7/8, EAC = 450 + 650 / (49/72)
        by = values(pc.evm(1000, 400, 350, 450))
        self.assertAlmostEqual(by["EAC with CPI and SPI"]["EAC"], 450 + 650 * 72 / 49)

    def test_tcpi_for_the_chosen_eac_by_hand(self):
        # approved EAC 1200: remaining work 650, remaining funds 1200 - 450 = 750
        by = values(pc.evm(1000, 400, 350, 450, approved_eac=1200))
        self.assertAlmostEqual(by["EAC approved"]["TCPI to this EAC"], 650 / 750)
        self.assertAlmostEqual(by["TCPI to complete on plan"]["TCPI to BAC"], 650 / 550)

    def test_approved_eac_not_above_actual_cost_has_no_tcpi(self):
        by = values(pc.evm(1000, 400, 350, 450, approved_eac=450))
        self.assertIsNone(by["EAC approved"]["TCPI to this EAC"])

    def test_etc_is_not_attributed_to_form_4_4(self):
        # Table 4.4 prints no ETC; only PMBOK 6 Table 7-1 does
        res = pc.evm(1000, 400, 350, 450)
        etc = res["sections"][2]["rows"][1]
        self.assertEqual(etc["label"], "ETC")
        self.assertNotIn("Form 4.4", etc["cite"])
        self.assertNotIn("form 4.4", etc["cite"])

    def test_negative_and_nonfinite_numbers_are_refused_everywhere(self):
        for call in (lambda: pc.evm(1, 1, -1, 1), lambda: pc.evm(1, 1, 1, -1),
                     lambda: pc.evm(float("nan"), 1, 1, 1), lambda: pc.evm(float("inf"), 1, 1, 1),
                     lambda: pc.evm(10, 1, 1, 1, bottom_up_etc=-1), lambda: pc.evm(10, 1, 1, 1, approved_eac=-1),
                     lambda: pc.pert(-1, 2, 3), lambda: pc.pert(1, float("nan"), 3),
                     lambda: pc.analogous(-1, 1, 1), lambda: pc.analogous(1, 0, 1),
                     lambda: pc.bottom_up(-1, 1), lambda: pc.bottom_up(1, 1, material=-5),
                     lambda: pc.effort_to_duration(10, 1, 0.5, -1), lambda: pc.effort_to_duration(10, 1, -0.5, 1),
                     lambda: pc.effort_to_duration(float("inf"), 1, 0.5, 1)):
            with self.assertRaises(pc.CalcError):
                call()

    def test_negative_flags_exit_2_on_the_command_line(self):
        for argv in (("evm", "--bac", "-5", "--pv", "1", "--ev", "1", "--ac", "1"),
                     ("evm", "--bac", "nan", "--pv", "1", "--ev", "1", "--ac", "1"),
                     ("effort-to-duration", "--effort-hours", "10", "--resources", "1", "--availability", "-0.5"),
                     ("emv", "--outcome", "-10%:80"), ("emv", "--outcome", "150%:80"),
                     ("emv", "--outcome", "-0.5:80"), ("emv", "--option", "A", "-5", "1:3"),
                     ("weighted-score", "--weights", "50", "50", "--scores", "1", "-2"),
                     ("risk-score", "--probability", "1.5", "--impact", "high", "--scale", "pmbok"),
                     ("risk-score", "--probability", "-0.2", "--impact", "high", "--scale", "doubling"),
                     ("risk-score", "--matrix", "--scale", "doubling")):
            try:
                code, _out, err = cli(*argv)
            except SystemExit as stop:
                # argparse itself refuses a token such as -10%:80 that looks like an option
                code, err = stop.code, "error:"
            self.assertEqual(code, 2, argv)
            self.assertTrue(err.startswith("error:"), argv)

    def test_default_performance_factor_is_announced(self):
        res = pc.effort_to_duration(150, 2, 0.75)
        self.assertAlmostEqual(flat(res)["Duration estimate"], 100.0)
        self.assertIn("No performance factor given", res["notes"][0])
        given = pc.effort_to_duration(150, 2, 0.75, 1.0)
        self.assertNotIn("No performance factor given", " ".join(given["notes"]))

    def test_the_book_equation_and_prose_disagreement_is_reported(self):
        # Table 2.16, PDF page 86 (printed page 75): the example divides by .8 and gives 125 hours
        res = pc.effort_to_duration(150, 2, 0.75, 0.8)
        self.assertAlmostEqual(flat(res)["Duration estimate"], 125.0)
        self.assertIn("divides by the performance factor", " ".join(res["notes"]))

    def test_percent_probability_text_is_exact(self):
        self.assertEqual(pc._probability_text("35%"), "0.35")
        self.assertEqual(pc._probability_text("0.3"), "0.3")
        self.assertAlmostEqual(flat(pc.risk_score("7%", "0.4", "pmbok"))["Score"], 0.028)

    def test_probabilities_in_percent_sum_with_tolerance(self):
        res = pc.emv([(0.333333, 3.0), (0.333333, 3.0), (0.333334, 3.0)], [])
        self.assertFalse(any("not 1" in n for n in res["notes"]))

    def test_ratings_must_not_be_negative(self):
        with self.assertRaises(pc.CalcError):
            pc.weighted_score([50, 50], [[1, -2]], None, None)

    def test_payback_period_section_is_the_success_measures_one(self):
        # PMBOK 6 section 1.2.6.4 Project success measures, printed page 34 (PDF page 73)
        self.assertIn("section 1.2.6.4,", pc.__doc__)
        self.assertNotIn("1.2.6.1", pc.__doc__)

    def test_help_text_cites_the_variance_page_once(self):
        text = pc.build_parser().format_help()
        sub = pc.build_parser()._subparsers._group_actions[0].choices["evm"].format_help()
        self.assertIn("printed page 262, PDF page 301", " ".join(sub.split()))
        self.assertNotIn("261 to 263", " ".join(sub.split()))
        self.assertTrue(text)



class NewCalculators(unittest.TestCase):
    """Earned schedule, critical path, velocity, CD3 and payback; the cpm network is PMBOK 6 Figure 6-16."""

    FIG_616 = dict(activities=[("A", 5.0), ("B", 5.0), ("C", 10.0), ("D", 15.0)],
                   links=[("A", "B", "FS", 0.0), ("A", "C", "FS", 0.0), ("B", "D", "FS", 0.0), ("C", "D", "FS", 0.0)])

    def test_earned_schedule_equations(self):
        res = pc.earned_schedule(6, 8)
        got = flat(res)
        self.assertAlmostEqual(got["SV(t)"], -2)
        self.assertAlmostEqual(got["SPI(t)"], 0.75)
        self.assertIn("233", res["sections"][0]["rows"][0]["cite"])

    def test_earned_schedule_refuses_zero_actual_time(self):
        with self.assertRaises(pc.CalcError):
            pc.earned_schedule(1, 0)

    def test_cpm_matches_figure_6_16(self):
        res = pc.cpm(**self.FIG_616)
        by = {t["activity"]: t for t in res["table"]}
        self.assertEqual((by["A"]["ES"], by["A"]["EF"]), (1, 5))
        self.assertEqual((by["B"]["ES"], by["B"]["EF"], by["B"]["LS"], by["B"]["LF"]), (6, 10, 11, 15))
        self.assertEqual((by["B"]["total_float"], by["B"]["free_float"]), (5, 5))
        self.assertEqual((by["D"]["ES"], by["D"]["EF"]), (16, 30))
        self.assertEqual([a for a, t in by.items() if t["critical"]], ["A", "C", "D"])
        self.assertEqual(flat(res)["Project duration (early finish of the last activity)"], 30)

    def test_cpm_deadline_gives_positive_and_negative_float(self):
        late = pc.cpm(**self.FIG_616, deadline=35)
        self.assertEqual({t["activity"]: t["total_float"] for t in late["table"]}["D"], 5)
        tight = pc.cpm(**self.FIG_616, deadline=28)
        self.assertEqual({t["activity"]: t["total_float"] for t in tight["table"]}["D"], -2)
        self.assertIn("Negative total float", " ".join(tight["notes"]))

    def test_cpm_slip_on_float_moves_nothing_and_on_the_path_moves_the_finish(self):
        off = pc.cpm(**self.FIG_616, slip=("B", 4))
        self.assertEqual(flat(off)["Project finish moves by"], 0)
        on = pc.cpm(**self.FIG_616, slip=("C", 3))
        self.assertEqual(flat(on)["Project finish moves by"], 3)

    def test_cpm_start_to_start_with_lag(self):
        res = pc.cpm([("A", 5.0), ("B", 3.0)], [("A", "B", "SS", 2.0)])
        by = {t["activity"]: t for t in res["table"]}
        self.assertEqual((by["B"]["ES"], by["B"]["EF"]), (3, 5))
        self.assertEqual(by["A"]["total_float"], 0)
        self.assertEqual(by["B"]["total_float"], 0)

    def test_cpm_finish_to_finish_and_start_to_finish(self):
        ff = pc.cpm([("A", 5.0), ("B", 2.0)], [("A", "B", "FF", 0.0)])
        self.assertEqual({t["activity"]: t["EF"] for t in ff["table"]}, {"A": 5, "B": 5})
        sf = pc.cpm([("A", 5.0), ("B", 2.0)], [("A", "B", "SF", 3.0)])
        self.assertEqual({t["activity"]: t["EF"] for t in sf["table"]}["B"], 3)

    def test_cpm_refuses_a_loop_an_unknown_name_and_a_bad_link(self):
        with self.assertRaises(pc.CalcError):
            pc.cpm([("A", 1.0), ("B", 1.0)], [("A", "B", "FS", 0.0), ("B", "A", "FS", 0.0)])
        with self.assertRaises(pc.CalcError):
            pc.cpm([("A", 1.0)], [("A", "Z", "FS", 0.0)])
        with self.assertRaises(pc.CalcError):
            pc.parse_link("A,B,XX")
        self.assertEqual(pc.parse_link("A,B,ss,2"), ("A", "B", "SS", 2.0))

    def test_cpm_cli(self):
        code, out, _ = cli("cpm", "--activity", "A=5", "--activity", "B=5", "--activity", "C=10",
                           "--activity", "D=15", "--link", "A,B", "--link", "A,C", "--link", "B,D",
                           "--link", "C,D")
        self.assertEqual(code, 0)
        self.assertIn("A - C - D", out)
        self.assertIn("outside arithmetic aid", out)

    def test_velocity_and_forecast_example_of_the_guide(self):
        res = pc.velocity([50, 50, 50, 50], 500)
        got = flat(res)
        self.assertAlmostEqual(got["Average velocity"], 50)
        self.assertAlmostEqual(got["Iterations remaining"], 10)
        self.assertFalse([n for n in res["notes"] if "four to eight" in n])
        self.assertTrue([n for n in pc.velocity([50, 50])["notes"] if "four to eight" in n])

    def test_cd3_ranks_highest_first_and_reports_ties(self):
        res = pc.cd3([("a", 100, 10), ("b", 90, 3), ("c", 30, 3)])
        self.assertEqual([r["label"][3:] for r in res["sections"][0]["rows"]], ["b", "a", "c"])
        tie = pc.cd3([("x", 10, 2), ("y", 20, 4)])
        self.assertIn("tie", " ".join(tie["notes"]))
        with self.assertRaises(pc.CalcError):
            pc.cd3([("z", 10, 0)])

    def test_payback_first_period_and_not_reached(self):
        res = pc.payback(360, [50, 120, 150, 160])
        self.assertEqual(flat(res)["Payback period"], 4)
        self.assertEqual(flat(pc.payback(1000, [10, 10]))["Payback period"], "not reached in the periods given")
        self.assertIn("no equation", " ".join(res["notes"]))

    def test_evm_refuses_a_zero_budget_and_notes_a_start_with_no_work(self):
        with self.assertRaises(pc.CalcError):
            pc.evm(0, 0, 0, 0)
        self.assertEqual(pc.main(["evm", "--bac", "0", "--pv", "0", "--ev", "0", "--ac", "0"]), 2)
        notes = " ".join(pc.evm(100, 0, 0, 0)["notes"])
        self.assertIn("nothing was planned or done", notes)

    def test_evm_states_the_rounding_convention(self):
        notes = " ".join(pc.evm(700000000, 280000000, 252000000, 294000000)["notes"])
        self.assertIn("Rounding is not stated in either book", notes)


class PercentCalendarAndAids(unittest.TestCase):
    def test_overrun_percent_is_labelled_and_tested_against_a_threshold(self):
        res = pc.evm(700000000, 280000000, 252000000, 294000000, threshold=5, bases=["bac", "pv"])
        titles = [sec["title"] for sec in res["sections"]]
        self.assertTrue([t for t in titles if t.startswith("Overrun as a percent of BAC")])
        self.assertTrue(all("not stated in the book" in t for t in titles if t.startswith("Overrun")))
        bac = [s for s in res["sections"] if s["title"].startswith("Overrun as a percent of BAC")][0]
        by = {r["label"]: r for r in bac["rows"]}
        self.assertAlmostEqual(by["Cost overrun to date (AC - EV)"]["value"], 6.0)
        self.assertEqual(by["Cost overrun to date (AC - EV)"]["status"], "beyond the 5% threshold")
        within = pc.evm(1000, 400, 400, 410, threshold=5)
        first = within["sections"][-1]["rows"][0]
        self.assertEqual(first["status"], "within the 5% threshold")

    def test_threshold_is_optional_and_exact_edge_is_within(self):
        res = pc.evm(1000, 400, 400, 450, threshold=5)
        self.assertEqual(res["sections"][-1]["rows"][0]["status"], "within the 5% threshold")
        plain = pc.evm(1000, 400, 400, 450)
        self.assertIsNone(plain["sections"][-1]["rows"][0]["status"])

    def test_cpm_calendar_dates_and_a_break(self):
        args = [("A", 5.0), ("B", 3.0)]
        links = [("A", "B", "FS", 0.0)]
        spans = pc.parse_breaks(["2027-02-06:2027-02-14"])
        res = pc.cpm(args, links, slip=("A", 4.0), start=pc.parse_date("2027-01-25", "x"), holidays=spans)
        flat_rows = flat(res)
        self.assertEqual(flat_rows["Project finish"], "2027-02-03")
        self.assertEqual(flat_rows["Project finish date before and after"], "2027-02-03 then 2027-02-16")
        self.assertIn("2027-02-06", flat_rows["Break between the old and the new finish"])

    def test_cpm_without_start_has_no_calendar_and_holiday_needs_start(self):
        res = pc.cpm([("A", 2.0)], [])
        self.assertNotIn("Project finish", flat(res))
        code, _out, err = cli("cpm", "--activity", "A=2", "--holiday", "2027-02-06")
        self.assertEqual(code, 2)
        self.assertIn("--start", err)

    def test_weekend_start_rolls_to_monday(self):
        cal = pc.WorkCalendar(pc.parse_date("2027-01-23", "x"), [])
        self.assertEqual(cal.date(1).isoformat(), "2027-01-25")

    def test_reserve_compares_remaining_with_open_risk(self):
        res = pc.reserve(28000000, 5000000, [("R5", 0.3, 12000000), ("R7", 0.2, 8000000)])
        by = flat(res)
        self.assertAlmostEqual(by["Contingency reserve remaining"], 23000000)
        self.assertAlmostEqual(by["Expected value of the open risks"], 5200000)
        self.assertAlmostEqual(by["Remaining minus the full impact of every open risk"], 3000000)
        self.assertIn("no equation", " ".join(res["notes"]))
        with self.assertRaises(pc.CalcError):
            pc.reserve(10, 20, [])

    def test_funding_steps_against_cost_to_date(self):
        res = pc.funding([("M0", 140.0), ("M3", 175.0), ("M4", 210.0)], 300.0, "M3", 525.0)
        by = flat(res)
        self.assertAlmostEqual(by["Funds released through M3"], 315)
        self.assertAlmostEqual(by["Released minus spent"], 15)
        with self.assertRaises(pc.CalcError):
            pc.funding([("M0", 1.0)], 0.0, "M9")
        bad = pc.funding([("M0", 100.0)], 0.0, "M0", 200.0)
        self.assertIn("add to", " ".join(bad["notes"]))

    def test_response_effectiveness_ratio(self):
        res = pc.response_effectiveness([("a", 10, 4, 3), ("b", 10, 7, 1)])
        by = flat(res)
        self.assertAlmostEqual(by["a"], 2)
        self.assertAlmostEqual(by["b"], 3)
        with self.assertRaises(pc.CalcError):
            pc.response_effectiveness([("z", 10, 4, 0)])

    def test_new_subcommands_cite_both_page_numbers(self):
        for argv in (("reserve", "--contingency", "10", "--risk", "R1=0.5:4"),
                     ("funding", "--tranche", "M0=5", "--through", "M0", "--spent", "3"),
                     ("response-effectiveness", "--option", "x", "5", "2", "1")):
            code, out, _err = cli(*argv)
            self.assertEqual(code, 0)
            self.assertRegex(out, r"printed page \d+ \(PDF page \d+\)")
        code, out, _err = cli("cpm", "--activity", "A=2", "--start", "2027-01-25", "--json")
        self.assertEqual(code, 0)
        json.loads(out)

    def test_rounding_note_asks_for_the_printed_decimals(self):
        notes = " ".join(pc.evm(700000000, 300000000, 250000000, 290000000)["notes"])
        self.assertIn("four decimals", notes)
        self.assertIn("Table 7-1 words", notes)


class RoundSevenAdditions(unittest.TestCase):
    def test_threshold_alone_prints_the_amount_of_the_bac(self):
        res = pc.evm(700000000, None, None, None, threshold=5, bases=["bac"])
        self.assertEqual(flat(res)["Threshold amount"], 35000000)

    def test_threshold_alone_refuses_another_base_and_missing_data(self):
        with self.assertRaises(pc.CalcError):
            pc.evm(700, None, None, None, threshold=5, bases=["bac", "pv"])
        with self.assertRaises(pc.CalcError):
            pc.evm(700, 300, None, None)
        code, out, _err = cli("evm", "--bac", "700", "--threshold", "5")
        self.assertEqual(code, 0)
        self.assertIn("35", out)

    def test_full_run_lists_the_threshold_amount_per_base(self):
        res = pc.evm(700, 300, 240, 280, threshold=5, bases=["bac", "pv"])
        amounts = [r["value"] for sec in res["sections"] for r in sec["rows"] if r["label"] == "Threshold amount"]
        self.assertEqual(amounts, [35, 15])

    def test_present_cpi_and_budgeted_rate_tcpi_carry_no_table_words(self):
        res = pc.evm(700, 300, 240, 280)
        by = {sec["title"]: {r["label"]: r for r in sec["rows"]} for sec in res["sections"]}
        present = by["EAC at the present CPI"]["TCPI to this EAC"]
        self.assertAlmostEqual(present["value"], 240 / 280)
        self.assertIsNone(present["status"])
        self.assertIn("equals the CPI", present["assumption"])
        self.assertIsNone(by["EAC at the budgeted rate"]["TCPI to this EAC"]["status"])
        self.assertIsNotNone(by["EAC with CPI and SPI"]["TCPI to this EAC"]["status"])

    def test_evm_note_places_other_eacs_in_the_selected_eac_row(self):
        notes = " ".join(pc.evm(700, 300, 240, 280)["notes"])
        self.assertIn("Selected EAC, Justification, and Explanation", notes)
        self.assertIn("PDF page 219 (printed page 208)", notes)

    def test_deadline_as_a_date_needs_start_and_converts_to_working_days(self):
        code, _out, err = cli("cpm", "--activity", "A=5", "--deadline", "2027-02-05")
        self.assertEqual(code, 2)
        self.assertIn("--start", err)
        code, out, _err = cli("cpm", "--activity", "A=5", "--start", "2027-01-25", "--deadline", "2027-01-29",
                              "--json")
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(out)["inputs"]["deadline"], 5)
        code, out, _err = cli("cpm", "--activity", "A=5", "--start", "2027-01-25", "--deadline", "2027-02-02",
                              "--holiday", "2027-02-01", "--json")
        self.assertEqual(json.loads(out)["inputs"]["deadline"], 6)

    def test_crash_ranks_by_extra_cost_per_day_saved(self):
        res = pc.crash([("A", 10, 7, 30), ("B", 8, 6, 12)], needed=4)
        rows = res["sections"][0]["rows"]
        self.assertEqual([r["label"] for r in rows], ["B", "A"])
        self.assertAlmostEqual(rows[0]["value"], 6)
        self.assertAlmostEqual(rows[1]["value"], 10)
        self.assertEqual(res["sections"][1]["rows"][-1]["value"], 4)
        self.assertIn("critical path", " ".join(res["notes"]))
        self.assertIn("printed page 215 (PDF page 254)", " ".join(res["notes"]))

    def test_crash_refuses_an_option_that_saves_nothing(self):
        with self.assertRaises(pc.CalcError):
            pc.crash([("A", 5, 5, 10)])
        code, _out, err = cli("crash")
        self.assertEqual(code, 2)


if __name__ == "__main__":
    unittest.main()
