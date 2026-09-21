import datetime
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import p5_Stojanovic_Veljko as p5


class ObservationTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.input_file = Path(self.directory.name) / "observations.txt"
        self.output_file = Path(self.directory.name) / "statistics.txt"

    def read_rows(self, rows):
        self.input_file.write_text("\n".join(rows), encoding="utf-8")
        return p5.read_observations(self.input_file)

    def test_several_stations_and_sorted_dates(self):
        observations, errors = self.read_rows([
            "B,09:00:00 AM 04/21/2026,20",
            "A,09:00:00 AM 04/20/2026,10",
            "B,09:00:00 AM 04/19/2026,15",
            "C,09:00:00 AM 04/20/2026,30",
        ])
        self.assertEqual(errors, [])
        self.assertEqual(set(observations), {"A", "B", "C"})
        self.assertEqual(observations["B"], [
            (datetime.datetime(2026, 4, 19, 9), 15.0),
            (datetime.datetime(2026, 4, 21, 9), 20.0),
        ])

    def test_negative_temperatures_and_inclusive_limits(self):
        observations, errors = self.read_rows([
            "A,09:00:00 AM 04/19/2026,-100",
            "A,09:00:00 AM 04/20/2026,-12.5",
            "A,09:00:00 AM 04/21/2026,150",
        ])
        self.assertEqual(errors, [])
        self.assertEqual([temp for date, temp in observations["A"]],
                         [-100.0, -12.5, 150.0])

    def test_duplicate_station_date_rejected(self):
        observations, errors = self.read_rows([
            "A,09:00:00 AM 04/20/2026,10",
            "A,09:00:00 AM 04/20/2026,20",
            "B,09:00:00 AM 04/20/2026,30",
        ])
        self.assertEqual(len(observations["A"]), 1)
        self.assertEqual(observations["A"][0][1], 10.0)
        self.assertIn("B", observations)
        self.assertEqual(errors[0][0], 2)
        self.assertIn("Duplicate", errors[0][1])
        self.assertEqual(len(errors), 1)

    def test_invalid_temperatures(self):
        for temperature in ["-100.1", "150.1", "abc", "nan", "inf", "-inf"]:
            with self.subTest(temperature=temperature):
                observations, errors = self.read_rows([
                    f"A,09:00:00 AM 04/20/2026,{temperature}",
                ])
                self.assertEqual(observations, {})
                self.assertEqual(len(errors), 1)
                self.assertEqual(errors[0][0], 1)
                self.assertIn("Invalid temperature", errors[0][1])

    def test_malformed_lines_and_invalid_dates(self):
        observations, errors = self.read_rows([
            "bad", "", ",09:00:00 AM 04/20/2026,10",
            "A,invalid,10", "A,09:00:00 AM 02/30/2026,10",
            "A,09:00:00 AM 04/20/2026,10,extra",
        ])
        self.assertEqual(observations, {})
        self.assertEqual([number for number, message in errors], list(range(1, 7)))

    def test_calculated_statistics(self):
        observations, _ = self.read_rows([
            "A,09:00:00 AM 04/19/2026,-10",
            "A,09:00:00 AM 04/20/2026,5",
            "A,09:00:00 AM 04/21/2026,20",
            "B,09:00:00 AM 04/20/2026,7.5",
        ])
        self.assertEqual(p5.station_statistics(observations),
                         {"A": (-10.0, 20.0, 5.0), "B": (7.5, 7.5, 7.5)})

    def test_outliers_use_latest_date_and_call_statistics(self):
        early = datetime.datetime(2026, 4, 19)
        late = datetime.datetime(2026, 4, 20)
        observations = {
            "rising": [(late, 20), (early, 0)],
            "falling": [(early, 20), (late, 0)],
            "equal": [(early, 10), (late, 10)],
        }
        with patch.object(p5, "station_statistics", wraps=p5.station_statistics) as stats:
            self.assertEqual(p5.station_outliers(observations),
                             {"rising": (late, 20, 10.0)})
            stats.assert_called_once_with(observations)

    def test_sorted_output_and_one_decimal_place(self):
        p5.write_statistics(self.output_file, {
            "Zulu": (1, 3, 2), "Alpha": (-12.25, 15.75, 1.75),
            "Beta": (0, 10, 5),
        })
        self.assertEqual(self.output_file.read_text(encoding="utf-8"),
                         "Alpha,-12.2,15.8,1.8\nBeta,0.0,10.0,5.0\nZulu,1.0,3.0,2.0\n")

    def test_missing_input_file(self):
        with self.assertRaises(FileNotFoundError):
            p5.read_observations(self.input_file)

    def test_main_handles_missing_file(self):
        with patch.object(p5.sys, "argv", ["p5.py", str(self.input_file), str(self.output_file)]), \
                patch("sys.stderr", new_callable=io.StringIO) as stderr:
            self.assertEqual(p5.main(), 1)
            self.assertIn("File access error", stderr.getvalue())

    def test_main_success(self):
        self.read_rows(["A,09:00:00 AM 04/20/2026,10"])
        with patch.object(p5.sys, "argv", ["p5.py", str(self.input_file), str(self.output_file)]), \
                patch("sys.stdout", new_callable=io.StringIO) as stdout:
            self.assertEqual(p5.main(), 0)
            self.assertIn("Statistics:", stdout.getvalue())
            self.assertIn("Outliers:", stdout.getvalue())
        self.assertEqual(self.output_file.read_text(encoding="utf-8"), "A,10.0,10.0,10.0\n")

    def test_main_handles_output_access_error(self):
        self.read_rows(["A,09:00:00 AM 04/20/2026,10"])
        with patch.object(p5.sys, "argv", ["p5.py", str(self.input_file), str(self.output_file)]), \
                patch.object(p5, "write_statistics", side_effect=PermissionError("Access denied")), \
                patch("sys.stdout", new_callable=io.StringIO), \
                patch("sys.stderr", new_callable=io.StringIO) as stderr:
            self.assertEqual(p5.main(), 1)
            self.assertIn("File access error", stderr.getvalue())

    def test_main_requires_two_filenames(self):
        with patch.object(p5.sys, "argv", ["p5.py"]), \
                patch("sys.stderr", new_callable=io.StringIO) as stderr:
            self.assertEqual(p5.main(), 1)
            self.assertIn("Usage:", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
