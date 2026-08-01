from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font


class DashboardWorkbook:
    """
    Responsible for creating and maintaining Job_Dashboard.xlsx
    """

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
        """
        Create dashboard only if it does not already exist.
        """

        if self.file_path.exists():

            print("Job_Dashboard.xlsx already exists.")

            return

        workbook = Workbook()

        workbook.remove(workbook.active)

        for sheet_name, headers in self.SHEETS.items():

            ws = workbook.create_sheet(title=sheet_name)

            for column, header in enumerate(headers, start=1):

                cell = ws.cell(row=1, column=column)

                cell.value = header

                cell.font = Font(bold=True)

            ws.freeze_panes = "A2"

            self._adjust_column_width(ws)

        workbook.save(self.file_path)

        print(f"Dashboard created successfully:\n{self.file_path}")

    @staticmethod
    def _adjust_column_width(ws):
        """
        Auto adjust column width according to header length.
        """

        for column in ws.columns:

            header = column[0].value

            width = max(len(str(header)) + 5, 15)

            ws.column_dimensions[column[0].column_letter].width = width
def write_companies(self, companies):

    from openpyxl import load_workbook

    workbook = load_workbook(self.file_path)

    ws = workbook["Companies"]

    if ws.max_row > 1:
        ws.delete_rows(2, ws.max_row)

    for company in companies:

        ws.append([
            company["Company"],
            company["Enabled"],
            company["Tier"],
            company["CareerURL"],
            "",
            "",
            company["Notes"],
        ])

    workbook.save(self.file_path)

    print(f"Loaded {len(companies)} companies.")
