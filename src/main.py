"""
main.py

Orchestrates the full pipeline:
CSV file -> DataLoader -> GradeClassifier -> PerformanceAnalyzer -> ReportGenerator

Run from the project root with:
    python run.py --input data/sample_students.csv --output output
"""

import argparse
import sys

from src.data_loader import DataLoader, DataLoadError
from src.grade_classifier import GradeClassifier
from src.analyzer import PerformanceAnalyzer
from src.report_generator import ReportGenerator


def run_pipeline(input_path: str, output_dir: str = "output") -> dict:
    """Runs the full pipeline and returns the summary dict. Raises
    DataLoadError if the input CSV is invalid, so the CLI can catch it."""

    loader = DataLoader(input_path)
    df = loader.load()

    classifier = GradeClassifier()
    students = classifier.classify_dataframe(df)

    analyzer = PerformanceAnalyzer(students)
    summary = analyzer.summary()

    reporter = ReportGenerator(summary, output_dir=output_dir)
    generated_files = reporter.generate_all()

    return {"summary": summary, "files": generated_files}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Student Performance Data Pipeline - reads a CSV, "
        "classifies grades, and generates summary reports."
    )
    parser.add_argument(
        "--input", "-i",
        default="data/sample_students.csv",
        help="Path to the input student CSV file (default: data/sample_students.csv)",
    )
    parser.add_argument(
        "--output", "-o",
        default="output",
        help="Directory to write reports/charts to (default: output)",
    )
    return parser.parse_args()


def main():
    args = parse_args()

    try:
        result = run_pipeline(args.input, args.output)
    except DataLoadError as e:
        print(f"[ERROR] {e}")
        sys.exit(1)

    print("Pipeline finished successfully.\n")
    print(f"Total students processed : {result['summary']['total_students']}")
    print(f"Overall class average    : {result['summary']['overall_class_average']}")
    print(f"Pass rate                : {result['summary']['pass_fail']['pass_rate_percent']}%")
    print("\nGenerated files:")
    for name, path in result["files"].items():
        print(f"  - {name}: {path}")


if __name__ == "__main__":
    main()
