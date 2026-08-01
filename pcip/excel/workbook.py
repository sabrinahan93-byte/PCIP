from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter
from pathlib import Path
from datetime import datetime



PIPELINE_OPTIONS = [
    "Observation",
    "Applied",
    "Recruiter Screen",
    "Interview",
    "Final Interview",
    "Offer",
    "Accepted",
    "Rejected",
    "Withdrawn"
]



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


        # 已存在文件，不重新创建
        if path.exists():

            return



        wb = Workbook()


        ws = wb.active

        ws.title = "Jobs"



        headers = [

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



        ws.append(headers)



        self._format_sheet(
            ws
        )


        self._add_pipeline_dropdown(
            ws
        )



        # Companies

        ws_company = wb.create_sheet(
            "Companies"
        )

        ws_company.append(

            [
                "Company",
                "Tier",
                "Enabled",
                "Priority",
                "Notes"
            ]

        )


        self._format_sheet(
            ws_company
        )



        # Run Log

        ws_log = wb.create_sheet(
            "Run_Log"
        )

        ws_log.append(

            [
                "Run Time",
                "Companies Scanned",
                "New Jobs",
                "Updated Jobs",
                "Closed Jobs",
                "Failed Companies",
                "Duration",
                "Result"
            ]

        )


        self._format_sheet(
            ws_log
        )



        # Run Detail

        ws_detail = wb.create_sheet(
            "Run_Detail"
        )

        ws_detail.append(

            [
                "Run Time",
                "Company",
                "Source Type",
                "Source URL",
                "Status",
                "Error Message"
            ]

        )


        self._format_sheet(
            ws_detail
        )



        wb.save(
            self.file_path
        )



    def _format_sheet(
        self,
        ws
    ):


        ws.freeze_panes = "A2"



        for cell in ws[1]:

            cell.font = Font(
                bold=True
            )



        for column in ws.columns:

            max_length = 0

            column_letter = get_column_letter(
                column[0].column
            )


            for cell in column:

                if cell.value:

                    max_length = max(
                        max_length,
                        len(str(cell.value))
                    )


            ws.column_dimensions[
                column_letter
            ].width = min(
                max_length + 3,
                40
            )



    def _add_pipeline_dropdown(
        self,
        ws
    ):


        validation = DataValidation(

            type="list",

            formula1='"' +
            ",".join(
                PIPELINE_OPTIONS
            )
            +
            '"',

            allow_blank=True

        )


        ws.add_data_validation(
            validation
        )


        validation.add(
            "H2:H5000"
        )



    def sync_companies(
        self,
        companies
    ):


        wb = load_workbook(
            self.file_path
        )


        ws = wb["Companies"]


        existing = set()


        for row in ws.iter_rows(
            min_row=2,
            values_only=True
        ):

            if row[0]:

                existing.add(
                    row[0]
                )



        for company in companies:


            name = company.get(
                "Company",
                ""
            )


            if name not in existing:


                ws.append(

                    [

                        name,

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



        self._format_sheet(
            ws
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


        counter = ws.max_row



        for job in jobs:


            counter += 1


            job_id = (

                f"JOB-{today}-"
                f"{counter-1:04d}"

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

                    job.get(
                        "Location",
                        ""
                    ),

                    job.get(
                        "Employment Type",
                        ""
                    ),

                    job.get(
                        "Seniority",
                        ""
                    ),

                    job.get(
                        "Posted Date",
                        ""
                    ),

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

                    job.get(
                        "Also Found On",
                        ""
                    )

                ]

            )


        # Applied Date格式

        for row in range(
            2,
            ws.max_row + 1
        ):

            ws.cell(
                row=row,
                column=9
            ).number_format = "yyyy-mm-dd"



        self._format_sheet(
            ws
        )


        self._add_pipeline_dropdown(
            ws
        )


        wb.save(
            self.file_path
        )
