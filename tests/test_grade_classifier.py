import unittest
import pandas as pd

from src.grade_classifier import GradeClassifier, Student


class TestGradeClassifierStatic(unittest.TestCase):

    def test_classify_grade_a(self):
        self.assertEqual(GradeClassifier.classify(90), "A")
        self.assertEqual(GradeClassifier.classify(85), "A")  # boundary

    def test_classify_grade_b(self):
        self.assertEqual(GradeClassifier.classify(75), "B")
        self.assertEqual(GradeClassifier.classify(70), "B")  # boundary

    def test_classify_grade_c(self):
        self.assertEqual(GradeClassifier.classify(60), "C")
        self.assertEqual(GradeClassifier.classify(55), "C")  # boundary

    def test_classify_grade_d(self):
        self.assertEqual(GradeClassifier.classify(45), "D")
        self.assertEqual(GradeClassifier.classify(40), "D")  # boundary

    def test_classify_grade_f(self):
        self.assertEqual(GradeClassifier.classify(39), "F")
        self.assertEqual(GradeClassifier.classify(0), "F")


class TestStudent(unittest.TestCase):

    def test_average_is_calculated_correctly(self):
        student = Student(
            student_id=1,
            name="Ali",
            scores={"math": 80, "science": 90, "english": 70, "history": 100},
            attendance_percentage=95,
        )
        self.assertEqual(student.average, 85.0)
        self.assertEqual(student.grade, "A")

    def test_is_passing_true_for_non_f_grade(self):
        student = Student(
            student_id=1, name="Ali",
            scores={"math": 50, "science": 50, "english": 50, "history": 50},
            attendance_percentage=80,
        )
        self.assertTrue(student.is_passing())

    def test_is_passing_false_for_f_grade(self):
        student = Student(
            student_id=1, name="Ali",
            scores={"math": 10, "science": 20, "english": 15, "history": 5},
            attendance_percentage=50,
        )
        self.assertFalse(student.is_passing())


class TestClassifyDataframe(unittest.TestCase):

    def test_classify_dataframe_returns_student_objects(self):
        df = pd.DataFrame([
            {"student_id": 1, "name": "Ali", "math": 90, "science": 85,
             "english": 88, "history": 92, "attendance_percentage": 95},
            {"student_id": 2, "name": "Sara", "math": 30, "science": 25,
             "english": 35, "history": 20, "attendance_percentage": 50},
        ])
        classifier = GradeClassifier()
        students = classifier.classify_dataframe(df)

        self.assertEqual(len(students), 2)
        self.assertEqual(students[0].grade, "A")
        self.assertEqual(students[1].grade, "F")


if __name__ == "__main__":
    unittest.main()
