from openpyxl import Workbook, load_workbook
from pathlib import Path
from datetime import datetime


class DashboardWorkbook:


    def __init__(self):

        self.file_path = (
            "output/Job_Dashboard.xlsx"
        )



    def initialize(self):

        path = Path(
            self.file_path
        )


        path.parent.mkdir(
            exist_ok=True
        )


        if path.exists():
            return


        wb = Workbook()


        # 删除默认sheet
        ws = wb.active
        ws.title = "Jobs"


        jobs_headers = [

            "Job ID",
            "Company",
            "Job Title",
            "Location",
            "Employment Type",
            "Seniority",
            "Posted Date",
            "Pipeline Status",
            "Applied Date",
            "Job URL",
            "Official Source",
            "Also Found On"

        ]


        for col, header in enumerate(
            jobs_headers,
            1
        ):

            ws.cell(
                row=1,
                column=col
            ).value = header



        ws_company = wb.create_sheet(
            "Companies"
        )


        company_headers = [

            "Company",
            "Tier",
            "Enabled",
            "Priority",
            "Notes"

        ]


        for col, header in enumerate(
            company_headers,
            1
        ):

            ws_company.cell(
                row=1,
                column=col
            ).value = header



        ws_log = wb.create_sheet(
            "Run_Log"
        )


        log_headers = [

            "Run Time",
            "Companies Scanned",
            "New Jobs",
            "Updated Jobs",
            "Closed Jobs",
            "Failed Companies",
            "Duration",
            "Result"

        ]


        for col, header in enumerate(
            log_headers,
            1
        ):

            ws_log.cell(
                row=1,
                column=col
            ).value = header



        ws_detail = wb.create_sheet(
            "Run_Detail"
        )


        detail_headers = [

            "Run Time",
            "Company",
            "Source Type",
            "Source URL",
            "Status",
            "Error Message"

        ]


        for col, header in enumerate(
            detail_headers,
            1
        ):

            ws_detail.cell(
                row=1,
                column=col
            ).value = header



        wb.save(
            self.file_path
        )



    def sync_companies(
        self,
        companies
    ):

        wb = load_workbook(
            self.file_path
        )


        ws = wb["Companies"]


        for company in companies:

            ws.append(
                [
                    company.get(
                        "Company",
                        ""
                    ),

                    company.get(
                        "Tier",
                        ""
                    ),

                    company.get(
                        "Enabled",
                        ""
                    ),

                    company.get(
                        "Priority",
                        ""
                    ),

                    company.get(
                        "Notes",
                        ""
                    )
                ]
            )


        wb.save(
            self.file_path
        )



    def write_jobs(
        self,
        jobs
    ):


        wb = load_workbook(
            self.file_path
        )


        ws = wb["Jobs"]


        today = datetime.now().strftime(
            "%Y%m%d"
        )


        existing_rows = (
            ws.max_row - 1
        )


        counter = existing_rows + 1



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

                    "",

                    "",

                    "",

                    "",

                    "Observation",

                    "",

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
