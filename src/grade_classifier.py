"""
grade_classifier.py

OOP-based grade classification logic. This is the part of the pipeline
that used to be done manually (someone opening Excel and eyeballing
which grade band each student falls into) - now it's automated.
"""

from dataclasses import dataclass, field
from typing import List

SUBJECT_COLUMNS = ["math", "science", "english", "history"]

# Grade boundaries, checked from highest to lowest.
GRADE_BANDS = [
    ("A", 85),
    ("B", 70),
    ("C", 55),
    ("D", 40),
    ("F", 0),
]


@dataclass
class Student:
    """A single student's record, with computed average and grade."""

    student_id: int
    name: str
    scores: dict
    attendance_percentage: float
    average: float = field(init=False)
    grade: str = field(init=False)

    def __post_init__(self):
        self.average = self._calculate_average()
        self.grade = GradeClassifier.classify(self.average)

    def _calculate_average(self) -> float:
        if not self.scores:
            return 0.0
        return round(sum(self.scores.values()) / len(self.scores), 2)

    def is_passing(self) -> bool:
        return self.grade != "F"


class GradeClassifier:
    """
    Converts a numeric average into a letter grade.

    Kept as a class (rather than a bare function) so grading rules can be
    swapped out or extended later, e.g. GradeClassifier(bands=custom_bands).
    """

    def __init__(self, bands=None):
        self.bands = bands or GRADE_BANDS

    @staticmethod
    def classify(average: float) -> str:
        """Static convenience method using the default grade bands."""
        for letter, threshold in GRADE_BANDS:
            if average >= threshold:
                return letter
        return "F"

    def classify_with_custom_bands(self, average: float) -> str:
        for letter, threshold in self.bands:
            if average >= threshold:
                return letter
        return "F"

    def classify_dataframe(self, df) -> List[Student]:
        """
        Takes a cleaned DataFrame (from DataLoader) and returns a list of
        Student objects, each with its average and grade already computed.
        """
        students = []
        for _, row in df.iterrows():
            scores = {subject: float(row[subject]) for subject in SUBJECT_COLUMNS}
            student = Student(
                student_id=int(row["student_id"]),
                name=str(row["name"]),
                scores=scores,
                attendance_percentage=float(row["attendance_percentage"]),
            )
            students.append(student)
        return students
