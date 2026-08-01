from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font


class DashboardWorkbook:

    FILE_NAME = "Job_Dashboard.xlsx"

    SHEETS = {
        "Jobs": [
            "Job ID",
            "Company",
            "Job Title",
            "Location",
            "Work Mode",
            "Match Score",
            "Job URL",
            "Last Seen",
            "Last Notified",
            "Pipeline Status",
            "Applied Date",
            "Notes",
        ],
        "Companies": [
            "Company",
            "Enabled",
            "Tier",
            "Career URL",
            "Last Scan",
            "Scan Status",
            "Notes",
        ],
        "Run_Log": [
            "Run Time",
            "Companies Scanned",
            "New Jobs",
            "Updated Jobs",
            "Closed Jobs",
            "Failed Companies",
            "Duration",
            "Result",
        ],
        "Run_Detail": [
            "Run Time",
            "Change Type",
            "Company",
            "Job Title",
            "Match Score",
            "Job URL",
        ],
    }

    def __init__(self, output_folder="output"):
        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(parents=True, exist_ok=True)

        self.file_path = self.output_folder / self.FILE_NAME

    def initialize(self):

        workbook = Workbook()

        default_sheet = workbook.active
        workbook.remove(default_sheet)

        for sheet_name, headers in self.SHEETS.items():

            ws = workbook.create_sheet(title=sheet_name)

            for column, header in enumerate(headers, start=1):

                cell = ws.cell(row=1, column=column)

                cell.value = header

                cell.font = Font(bold=True)

            ws.freeze_panes = "A2"

        workbook.save(self.file_path)

        print(f"Dashboard created: {self.file_path}")
