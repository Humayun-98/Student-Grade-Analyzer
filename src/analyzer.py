"""
analyzer.py

Computes class-wide performance metrics from a list of Student objects:
subject averages, grade distribution, pass/fail rate, top/bottom
performers, and a simple attendance-vs-performance check.
"""

from typing import List
from collections import Counter
from src.grade_classifier import Student, SUBJECT_COLUMNS


class PerformanceAnalyzer:
    """Runs summary statistics over a batch of classified students."""

    def __init__(self, students: List[Student]):
        if not students:
            raise ValueError("Cannot analyze an empty student list.")
        self.students = students

    def total_students(self) -> int:
        return len(self.students)

    def subject_averages(self) -> dict:
        """Average score per subject, across all students."""
        averages = {}
        for subject in SUBJECT_COLUMNS:
            total = sum(s.scores[subject] for s in self.students)
            averages[subject] = round(total / len(self.students), 2)
        return averages

    def overall_class_average(self) -> float:
        total = sum(s.average for s in self.students)
        return round(total / len(self.students), 2)

    def grade_distribution(self) -> dict:
        """How many students fall into each grade band, e.g. {'A': 3, 'B': 5, ...}"""
        counts = Counter(s.grade for s in self.students)
        # Keep a consistent order: A, B, C, D, F
        return {grade: counts.get(grade, 0) for grade in ["A", "B", "C", "D", "F"]}

    def pass_fail_rate(self) -> dict:
        passing = sum(1 for s in self.students if s.is_passing())
        failing = len(self.students) - passing
        total = len(self.students)
        return {
            "passing": passing,
            "failing": failing,
            "pass_rate_percent": round((passing / total) * 100, 2),
        }

    def top_performers(self, n: int = 3) -> List[Student]:
        return sorted(self.students, key=lambda s: s.average, reverse=True)[:n]

    def bottom_performers(self, n: int = 3) -> List[Student]:
        return sorted(self.students, key=lambda s: s.average)[:n]

    def average_attendance(self) -> float:
        total = sum(s.attendance_percentage for s in self.students)
        return round(total / len(self.students), 2)

    def low_attendance_students(self, threshold: float = 75.0) -> List[Student]:
        """Students whose attendance is below the given threshold - useful
        for flagging students who might be at risk regardless of grade."""
        return [s for s in self.students if s.attendance_percentage < threshold]

    def summary(self) -> dict:
        """Bundles everything together into one dict, handy for reporting."""
        return {
            "total_students": self.total_students(),
            "subject_averages": self.subject_averages(),
            "overall_class_average": self.overall_class_average(),
            "grade_distribution": self.grade_distribution(),
            "pass_fail": self.pass_fail_rate(),
            "average_attendance": self.average_attendance(),
            "top_performers": [(s.name, s.average) for s in self.top_performers()],
            "bottom_performers": [(s.name, s.average) for s in self.bottom_performers()],
            "low_attendance_count": len(self.low_attendance_students()),
        }
