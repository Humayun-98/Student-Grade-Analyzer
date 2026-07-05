"""
report_generator.py

Takes the summary dict from PerformanceAnalyzer and produces:
1. A grade distribution bar chart (PNG)
2. A subject-wise average score bar chart (PNG)
3. A plain-text summary report

Matplotlib is set to the "Agg" backend so this also works fine on a
server / CI environment with no display attached.
"""

import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


class ReportGenerator:
    def __init__(self, summary: dict, output_dir: str = "output"):
        self.summary = summary
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def generate_grade_distribution_chart(self, filename: str = "grade_distribution.png") -> str:
        distribution = self.summary["grade_distribution"]
        grades = list(distribution.keys())
        counts = list(distribution.values())

        colors = ["#4CAF50", "#8BC34A", "#FFC107", "#FF9800", "#F44336"]

        plt.figure(figsize=(6, 4))
        plt.bar(grades, counts, color=colors)
        plt.title("Grade Distribution")
        plt.xlabel("Grade")
        plt.ylabel("Number of Students")
        plt.tight_layout()

        path = os.path.join(self.output_dir, filename)
        plt.savefig(path)
        plt.close()
        return path

    def generate_subject_average_chart(self, filename: str = "subject_averages.png") -> str:
        averages = self.summary["subject_averages"]
        subjects = list(averages.keys())
        scores = list(averages.values())

        plt.figure(figsize=(6, 4))
        plt.bar(subjects, scores, color="#2196F3")
        plt.title("Average Score by Subject")
        plt.xlabel("Subject")
        plt.ylabel("Average Score")
        plt.ylim(0, 100)
        plt.tight_layout()

        path = os.path.join(self.output_dir, filename)
        plt.savefig(path)
        plt.close()
        return path

    def generate_text_report(self, filename: str = "summary_report.txt") -> str:
        s = self.summary
        lines = []
        lines.append("=" * 50)
        lines.append("STUDENT PERFORMANCE SUMMARY REPORT")
        lines.append("=" * 50)
        lines.append(f"Total Students Analyzed : {s['total_students']}")
        lines.append(f"Overall Class Average   : {s['overall_class_average']}")
        lines.append(f"Average Attendance (%)  : {s['average_attendance']}")
        lines.append("")

        lines.append("Subject-wise Averages:")
        for subject, avg in s["subject_averages"].items():
            lines.append(f"  - {subject.capitalize():<10}: {avg}")
        lines.append("")

        lines.append("Grade Distribution:")
        for grade, count in s["grade_distribution"].items():
            lines.append(f"  - Grade {grade}: {count} student(s)")
        lines.append("")

        pf = s["pass_fail"]
        lines.append(
            f"Pass/Fail: {pf['passing']} passing, {pf['failing']} failing "
            f"({pf['pass_rate_percent']}% pass rate)"
        )
        lines.append("")

        lines.append("Top Performers:")
        for name, avg in s["top_performers"]:
            lines.append(f"  - {name}: {avg}")
        lines.append("")

        lines.append("Students Needing Attention (lowest averages):")
        for name, avg in s["bottom_performers"]:
            lines.append(f"  - {name}: {avg}")
        lines.append("")

        lines.append(f"Students with Attendance Below 75%: {s['low_attendance_count']}")
        lines.append("=" * 50)

        report_text = "\n".join(lines)

        path = os.path.join(self.output_dir, filename)
        with open(path, "w") as f:
            f.write(report_text)

        return path

    def generate_all(self) -> dict:
        """Convenience method to generate every report artifact at once."""
        return {
            "grade_chart": self.generate_grade_distribution_chart(),
            "subject_chart": self.generate_subject_average_chart(),
            "text_report": self.generate_text_report(),
        }
