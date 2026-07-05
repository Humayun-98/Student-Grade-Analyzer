# Student Performance Data Pipeline

A small Python data pipeline that reads student CSV data, classifies grades using OOP,
analyzes class-wide performance metrics, and generates automated summary reports
(text + Matplotlib charts).

Built as a mini project to practice data pipelines with Pandas, OOP design, and
Matplotlib visualization.

## Features

- **Data Ingestion** — Reads and validates CSV datasets using Pandas (handles missing
  columns, missing values, duplicate rows, and out-of-range scores).
- **Grade Classification (OOP)** — A `Student` class and `GradeClassifier` class
  automatically compute each student's average and letter grade (A–F), replacing
  what would otherwise be manual spreadsheet work.
- **Performance Analysis** — Computes subject averages, overall class average, grade
  distribution, pass/fail rate, top/bottom performers, and attendance flags.
- **Automated Reports** — Generates a plain-text summary report plus two Matplotlib
  charts (grade distribution and subject-wise averages).
- **Fully Tested** — Unit tests for every module using `unittest`.

## Project Structure

```
student_performance_pipeline/
│
├── README.md                     # This file
├── requirements.txt               # Python dependencies
├── .gitignore
├── run.py                         # Entry point (CLI)
│
├── data/
│   └── sample_students.csv        # Sample dataset (15 students)
│
├── src/
│   ├── __init__.py
│   ├── data_loader.py             # CSV ingestion + cleaning/validation
│   ├── grade_classifier.py        # Student class + OOP grade classification
│   ├── analyzer.py                # Performance metrics / class statistics
│   ├── report_generator.py        # Text report + Matplotlib charts
│   └── main.py                    # Pipeline orchestration + CLI args
│
├── tests/
│   ├── __init__.py
│   ├── test_data_loader.py
│   ├── test_grade_classifier.py
│   ├── test_analyzer.py
│   └── test_report_generator.py
│
└── output/                        # Generated reports/charts land here
    ├── grade_distribution.png
    ├── subject_averages.png
    └── summary_report.txt
```

## Setup

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd student_performance_pipeline

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

## Usage

Run the pipeline on the included sample dataset:

```bash
python run.py
```

Or specify a custom input file / output folder:

```bash
python run.py --input data/sample_students.csv --output output
```

This will print a summary to the console and generate the following inside
`output/`:

- `summary_report.txt` — full text breakdown of class performance
- `grade_distribution.png` — bar chart of how many students got each grade
- `subject_averages.png` — bar chart of average score per subject

### Expected CSV format

Your input CSV must contain these columns:

| Column                 | Description                          |
|------------------------|---------------------------------------|
| student_id             | Unique student identifier              |
| name                   | Student name                           |
| math                   | Math score (0–100)                     |
| science                | Science score (0–100)                  |
| english                | English score (0–100)                  |
| history                | History score (0–100)                  |
| attendance_percentage  | Attendance percentage (0–100)          |

## Running Tests

Tests are written with `unittest` and can be run with either `unittest` or `pytest`:

```bash
# Using unittest
python -m unittest discover tests

# Using pytest
pytest tests/ -v
```

## Grading Logic

| Average Score | Grade |
|---------------|-------|
| 85 – 100       | A     |
| 70 – 84        | B     |
| 55 – 69        | C     |
| 40 – 54        | D     |
| Below 40       | F     |

## Possible Future Improvements

- Support for exporting the summary report as PDF
- A simple web dashboard (Flask/Streamlit) instead of static charts
- Configurable grade bands via a config file instead of hardcoded values
- Support for multiple CSV files / merging datasets over time
