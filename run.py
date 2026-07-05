"""
Entry point for the project. Just delegates to src/main.py so the
pipeline can be run with:

    python run.py --input data/sample_students.csv --output output
"""

from src.main import main

if __name__ == "__main__":
    main()
