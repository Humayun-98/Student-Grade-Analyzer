import unittest

from src.grade_classifier import Student
from src.analyzer import PerformanceAnalyzer


def make_student(student_id, name, math, science, english, history, attendance):
    return Student(
        student_id=student_id,
        name=name,
        scores={"math": math, "science": science, "english": english, "history": history},
        attendance_percentage=attendance,
    )


class TestPerformanceAnalyzer(unittest.TestCase):

    def setUp(self):
        self.students = [
            make_student(1, "Ali", 90, 85, 88, 92, 95),    # A
            make_student(2, "Sara", 60, 65, 70, 62, 80),   # C
            make_student(3, "Bilal", 20, 25, 30, 15, 50),  # F
        ]
        self.analyzer = PerformanceAnalyzer(self.students)

    def test_empty_list_raises_error(self):
        with self.assertRaises(ValueError):
            PerformanceAnalyzer([])

    def test_total_students(self):
        self.assertEqual(self.analyzer.total_students(), 3)

    def test_subject_averages(self):
        averages = self.analyzer.subject_averages()
        expected_math = round((90 + 60 + 20) / 3, 2)
        self.assertEqual(averages["math"], expected_math)

    def test_overall_class_average(self):
        expected = round((self.students[0].average + self.students[1].average + self.students[2].average) / 3, 2)
        self.assertEqual(self.analyzer.overall_class_average(), expected)

    def test_grade_distribution_counts_all_bands(self):
        distribution = self.analyzer.grade_distribution()
        self.assertEqual(set(distribution.keys()), {"A", "B", "C", "D", "F"})
        self.assertEqual(distribution["A"], 1)
        self.assertEqual(distribution["C"], 1)
        self.assertEqual(distribution["F"], 1)

    def test_pass_fail_rate(self):
        result = self.analyzer.pass_fail_rate()
        self.assertEqual(result["passing"], 2)
        self.assertEqual(result["failing"], 1)
        self.assertAlmostEqual(result["pass_rate_percent"], 66.67, places=1)

    def test_top_performers_ordering(self):
        top = self.analyzer.top_performers(n=1)
        self.assertEqual(top[0].name, "Ali")

    def test_bottom_performers_ordering(self):
        bottom = self.analyzer.bottom_performers(n=1)
        self.assertEqual(bottom[0].name, "Bilal")

    def test_average_attendance(self):
        expected = round((95 + 80 + 50) / 3, 2)
        self.assertEqual(self.analyzer.average_attendance(), expected)

    def test_low_attendance_students_default_threshold(self):
        low_attendance = self.analyzer.low_attendance_students()
        names = [s.name for s in low_attendance]
        self.assertIn("Bilal", names)
        self.assertNotIn("Ali", names)

    def test_summary_contains_expected_keys(self):
        summary = self.analyzer.summary()
        expected_keys = {
            "total_students", "subject_averages", "overall_class_average",
            "grade_distribution", "pass_fail", "average_attendance",
            "top_performers", "bottom_performers", "low_attendance_count",
        }
        self.assertEqual(set(summary.keys()), expected_keys)


if __name__ == "__main__":
    unittest.main()
