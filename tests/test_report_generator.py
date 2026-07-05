import os
import shutil
import tempfile
import unittest

from src.report_generator import ReportGenerator


class TestReportGenerator(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.summary = {
            "total_students": 3,
            "subject_averages": {"math": 56.67, "science": 58.33, "english": 62.67, "history": 56.33},
            "overall_class_average": 58.5,
            "grade_distribution": {"A": 1, "B": 0, "C": 1, "D": 0, "F": 1},
            "pass_fail": {"passing": 2, "failing": 1, "pass_rate_percent": 66.67},
            "average_attendance": 75.0,
            "top_performers": [("Ali", 88.75)],
            "bottom_performers": [("Bilal", 22.5)],
            "low_attendance_count": 1,
        }
        self.generator = ReportGenerator(self.summary, output_dir=self.tmp_dir)

    def tearDown(self):
        shutil.rmtree(self.tmp_dir, ignore_errors=True)

    def test_output_dir_created(self):
        self.assertTrue(os.path.isdir(self.tmp_dir))

    def test_grade_distribution_chart_created(self):
        path = self.generator.generate_grade_distribution_chart()
        self.assertTrue(os.path.exists(path))
        self.assertGreater(os.path.getsize(path), 0)

    def test_subject_average_chart_created(self):
        path = self.generator.generate_subject_average_chart()
        self.assertTrue(os.path.exists(path))
        self.assertGreater(os.path.getsize(path), 0)

    def test_text_report_created_and_contains_key_data(self):
        path = self.generator.generate_text_report()
        self.assertTrue(os.path.exists(path))
        with open(path) as f:
            content = f.read()
        self.assertIn("STUDENT PERFORMANCE SUMMARY REPORT", content)
        self.assertIn("Ali", content)
        self.assertIn("Bilal", content)
        self.assertIn("66.67", content)

    def test_generate_all_returns_all_paths(self):
        result = self.generator.generate_all()
        self.assertEqual(set(result.keys()), {"grade_chart", "subject_chart", "text_report"})
        for path in result.values():
            self.assertTrue(os.path.exists(path))


if __name__ == "__main__":
    unittest.main()
