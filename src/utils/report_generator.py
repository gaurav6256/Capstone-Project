from pathlib import Path
import pandas as pd

class ReportGenerator:
    @staticmethod
    def generate(results: list[dict], output_directory: Path):
        report_path = output_directory / "final_report.csv"
        pd.DataFrame(results).to_csv(report_path, index=False)
        return report_path
