"""
data_loader.py

Handles reading the raw student CSV file and doing basic validation/
cleaning before it gets passed on to the rest of the pipeline.
"""

import os
import pandas as pd

# Columns we expect every dataset to have. If any of these are missing
# we can't really trust the file, so we raise an error early instead of
# letting garbage flow through the pipeline.
REQUIRED_COLUMNS = [
    "student_id",
    "name",
    "math",
    "science",
    "english",
    "history",
    "attendance_percentage",
]

SUBJECT_COLUMNS = ["math", "science", "english", "history"]


class DataLoadError(Exception):
    """Raised when the CSV file can't be loaded or is missing required data."""
    pass


class DataLoader:
    """Reads a student CSV file into a clean pandas DataFrame."""

    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self) -> pd.DataFrame:
        """
        Reads the CSV, validates it, and returns a cleaned DataFrame.

        Raises:
            DataLoadError: if the file doesn't exist, is empty, or is
                           missing required columns.
        """
        if not os.path.exists(self.file_path):
            raise DataLoadError(f"File not found: {self.file_path}")

        try:
            df = pd.read_csv(self.file_path)
        except pd.errors.EmptyDataError:
            raise DataLoadError(f"File is empty: {self.file_path}")
        except pd.errors.ParserError as e:
            raise DataLoadError(f"Could not parse CSV file: {e}")

        self._validate_columns(df)
        df = self._clean(df)
        return df

    def _validate_columns(self, df: pd.DataFrame) -> None:
        missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
        if missing:
            raise DataLoadError(f"Missing required column(s): {missing}")

    def _clean(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Basic cleaning:
        - drop rows that are missing a student_id or name
        - drop exact duplicate rows
        - make sure numeric columns are actually numeric
        - clip scores into a sane 0-100 range (bad data guard)
        """
        df = df.copy()

        df = df.dropna(subset=["student_id", "name"])
        df = df.drop_duplicates()

        numeric_cols = SUBJECT_COLUMNS + ["attendance_percentage"]
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # Any row where all subject scores failed to convert is useless data.
        df = df.dropna(subset=SUBJECT_COLUMNS, how="all")

        # Fill any single missing subject score with 0 rather than dropping
        # the whole student - a missing score most likely means the student
        # did not sit that particular exam.
        df[SUBJECT_COLUMNS] = df[SUBJECT_COLUMNS].fillna(0)
        df["attendance_percentage"] = df["attendance_percentage"].fillna(0)

        for col in numeric_cols:
            df[col] = df[col].clip(lower=0, upper=100)

        df = df.reset_index(drop=True)
        return df
