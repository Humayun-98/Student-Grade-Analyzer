import os
import tempfile
import unittest

from src.data_loader import DataLoader, DataLoadError


class TestDataLoader(unittest.TestCase):

    def setUp(self):
        # Create a temp CSV with valid data for most tests.
        self.tmp_dir = tempfile.mkdtemp()
        self.valid_csv = os.path.join(self.tmp_dir, "valid.csv")
        with open(self.valid_csv, "w") as f:
            f.write(
                "student_id,name,math,science,english,history,attendance_percentage\n"
                "1,Ali,80,70,90,85,95\n"
                "2,Sara,60,65,70,75,80\n"
            )

    def test_load_valid_csv_returns_dataframe(self):
        loader = DataLoader(self.valid_csv)
        df = loader.load()
        self.assertEqual(len(df), 2)
        self.assertIn("math", df.columns)

    def test_missing_file_raises_error(self):
        loader = DataLoader(os.path.join(self.tmp_dir, "does_not_exist.csv"))
        with self.assertRaises(DataLoadError):
            loader.load()

    def test_missing_required_column_raises_error(self):
        bad_csv = os.path.join(self.tmp_dir, "bad.csv")
        with open(bad_csv, "w") as f:
            f.write("student_id,name,math\n1,Ali,80\n")

        loader = DataLoader(bad_csv)
        with self.assertRaises(DataLoadError):
            loader.load()

    def test_empty_file_raises_error(self):
        empty_csv = os.path.join(self.tmp_dir, "empty.csv")
        open(empty_csv, "w").close()

        loader = DataLoader(empty_csv)
        with self.assertRaises(DataLoadError):
            loader.load()

    def test_missing_score_is_filled_with_zero(self):
        csv_path = os.path.join(self.tmp_dir, "missing_score.csv")
        with open(csv_path, "w") as f:
            f.write(
                "student_id,name,math,science,english,history,attendance_percentage\n"
                "1,Ali,,70,90,85,95\n"
            )
        loader = DataLoader(csv_path)
        df = loader.load()
        self.assertEqual(df.loc[0, "math"], 0)

    def test_scores_out_of_range_are_clipped(self):
        csv_path = os.path.join(self.tmp_dir, "out_of_range.csv")
        with open(csv_path, "w") as f:
            f.write(
                "student_id,name,math,science,english,history,attendance_percentage\n"
                "1,Ali,150,-20,90,85,95\n"
            )
        loader = DataLoader(csv_path)
        df = loader.load()
        self.assertEqual(df.loc[0, "math"], 100)
        self.assertEqual(df.loc[0, "science"], 0)

    def test_duplicate_rows_are_dropped(self):
        csv_path = os.path.join(self.tmp_dir, "dupes.csv")
        with open(csv_path, "w") as f:
            f.write(
                "student_id,name,math,science,english,history,attendance_percentage\n"
                "1,Ali,80,70,90,85,95\n"
                "1,Ali,80,70,90,85,95\n"
            )
        loader = DataLoader(csv_path)
        df = loader.load()
        self.assertEqual(len(df), 1)

    def test_row_missing_student_id_is_dropped(self):
        csv_path = os.path.join(self.tmp_dir, "missing_id.csv")
        with open(csv_path, "w") as f:
            f.write(
                "student_id,name,math,science,english,history,attendance_percentage\n"
                ",Ali,80,70,90,85,95\n"
                "2,Sara,60,65,70,75,80\n"
            )
        loader = DataLoader(csv_path)
        df = loader.load()
        self.assertEqual(len(df), 1)
        self.assertEqual(df.loc[0, "name"], "Sara")


if __name__ == "__main__":
    unittest.main()
