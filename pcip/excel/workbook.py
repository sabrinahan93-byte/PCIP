from pathlib import Path
from datetime import datetime
from openpyxl import Workbook, load_workbook
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
            "Company",
            "Source Type",
            "Source URL",
            "Status",
            "Error Message",
        ],
    }
    def write_jobs(self, jobs):

    from datetime import datetime

    wb = load_workbook(
        self.file_path
    )

    ws = wb["Jobs"]


    today = datetime.now().strftime(
        "%Y%m%d"
    )


    # 获取已有JOB数量
    existing = ws.max_row - 1


    counter = existing + 1


    for job in jobs:


        job_id = (
            f"JOB-{today}-"
            f"{counter:04d}"
        )


        ws.append(

            [
                job_id,

                job.get(
                    "Company",
                    ""
                ),

                job.get(
                    "Job Title",
                    ""
                ),

                "",      # Location

                "",      # Employment Type

                "",      # Seniority

                "",      # Posted Date

                "Observation",

                "",      # Applied Date

                job.get(
                    "Job URL",
                    ""
                ),

                job.get(
                    "Official Source",
                    ""
                ),

                ""

            ]

        )


        counter += 1


    wb.save(
        self.file_path
    )
    def __init__(self, output_folder="output"):

        self.output_folder = Path(output_folder)
        self.output_folder.mkdir(parents=True, exist_ok=True)

        self.file_path = self.output_folder / self.FILE_NAME

    def initialize(self):

        if self.file_path.exists():
            print("Job_Dashboard.xlsx already exists.")
            return

        wb = Workbook()

        wb.remove(wb.active)

        for sheet_name, headers in self.SHEETS.items():

            ws = wb.create_sheet(sheet_name)

            ws.freeze_panes = "A2"

            for col, header in enumerate(headers, start=1):

                cell = ws.cell(row=1, column=col)

                cell.value = header

                cell.font = Font(bold=True)

                ws.column_dimensions[cell.column_letter].width = max(
                    len(header) + 5,
                    18
                )

        wb.save(self.file_path)

        print(f"Dashboard created successfully:\n{self.file_path}")

    def sync_companies(self, companies):

        wb = load_workbook(self.file_path)

        ws = wb["Companies"]

        # 删除除标题外所有内容
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

        wb.save(self.file_path)

        print(f"Companies synced: {len(companies)}")
