from openpyxl import Workbook, load_workbook
from pathlib import Path
from datetime import datetime
from openpyxl.styles import Font
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter



PIPELINE_OPTIONS = [
    "New",
    "Watch",
    "Applied",
    "Interview",
    "Offer",
    "Accepted",
    "Rejected",
    "Declined"
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


        if path.exists():

            return



        wb = Workbook()


        ws = wb.active

        ws.title = "Jobs"


        ws.append(

            [

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
                "Notes"

            ]

        )


        self.format_sheet(
            ws
        )


        self.add_pipeline_validation(
            ws
        )


        wb.create_sheet(
            "Companies"
        )

        wb.create_sheet(
            "Run_Log"
        )

        wb.create_sheet(
            "Run_Detail"
        )


        wb.save(
            self.file_path
        )



    # ==========================
    # Excel Formatting
    # ==========================


    def format_sheet(
        self,
        ws
    ):


        ws.freeze_panes = "A2"


        for cell in ws[1]:

            cell.font = Font(
                bold=True
            )



        for column in ws.columns:


            length = 0


            letter = get_column_letter(
                column[0].column
            )


            for cell in column:


                if cell.value:

                    length = max(
                        length,
                        len(str(cell.value))
                    )



            ws.column_dimensions[
                letter
            ].width = min(
                length + 3,
                40
            )



    def add_pipeline_validation(
        self,
        ws
    ):


        dv = DataValidation(

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
            dv
        )


        dv.add(
            "J2:J5000"
        )



    # ==========================
    # Company Sync
    # ==========================


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
                            "Enabled",
                            ""
                        ),
                        company.get(
                            "Tier",
                            ""
                        ),
                        company.get(
                            "Career URL",
                            ""
                        ),
                        "",
                        "",
                        ""

                    ]

                )



        wb.save(
            self.file_path
        )



    # ==========================
    # Job Write Engine
    # ==========================


    def write_jobs(
        self,
        jobs
    ):


        wb = load_workbook(
            self.file_path
        )


        ws = wb["Jobs"]


        existing_map = self.build_job_index(
            ws
        )


        today = datetime.now().strftime(
            "%Y-%m-%d"
        )


        new_count = 0

        updated_count = 0



        for job in jobs:


            key = self.create_key(
                job
            )


            if key in existing_map:


                row = existing_map[key]


                self.update_existing_job(
                    ws,
                    row,
                    job,
                    today
                )


                updated_count += 1



            else:


                job_id = self.generate_job_id(
                    ws
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
                            "Work Mode",
                            ""
                        ),

                        job.get(
                            "Match Score",
                            0
                        ),

                        job.get(
                            "Job URL",
                            ""
                        ),

                        today,

                        "",

                        "New",

                        "",

                        ""

                    ]

                )


                new_count += 1



        self.format_sheet(
            ws
        )


        self.add_pipeline_validation(
            ws
        )


        wb.save(
            self.file_path
        )



        return {

            "new": new_count,

            "updated": updated_count

        }



    # ==========================
    # Existing Job Update
    # ==========================


    def update_existing_job(
        self,
        ws,
        row,
        job,
        today
    ):


        # System fields only

        ws.cell(
            row=row,
            column=2
        ).value = job.get(
            "Company",
            ""
        )


        ws.cell(
            row=row,
            column=3
        ).value = job.get(
            "Job Title",
            ""
        )


        ws.cell(
            row=row,
            column=4
        ).value = job.get(
            "Location",
            ""
        )


        ws.cell(
            row=row,
            column=5
        ).value = job.get(
            "Work Mode",
            ""
        )


        ws.cell(
            row=row,
            column=6
        ).value = job.get(
            "Match Score",
            0
        )


        ws.cell(
            row=row,
            column=7
        ).value = job.get(
            "Job URL",
            ""
        )


        ws.cell(
            row=row,
            column=8
        ).value = today


        # IMPORTANT:
        #
        # Column 10 Pipeline Status
        # Column 11 Applied Date
        # Column 12 Notes
        #
        # NEVER TOUCH



    # ==========================
    # Helpers
    # ==========================


    def build_job_index(
        self,
        ws
    ):


        result = {}


        for row in range(
            2,
            ws.max_row + 1
        ):


            company = ws.cell(
                row=row,
                column=2
            ).value


            title = ws.cell(
                row=row,
                column=3
            ).value



            url = ws.cell(
                row=row,
                column=7
            ).value



            key = (

                str(company).lower()
                +
                "|"
                +
                str(title).lower()
                +
                "|"
                +
                str(url).lower()

            )



            result[key] = row



        return result



    def create_key(
        self,
        job
    ):


        return (

            str(
                job.get(
                    "Company",
                    ""
                )
            ).lower()

            +

            "|"

            +

            str(
                job.get(
                    "Job Title",
                    ""
                )
            ).lower()

            +

            "|"

            +

            str(
                job.get(
                    "Job URL",
                    ""
                )
            ).lower()

        )



    def generate_job_id(
        self,
        ws
    ):


        today = datetime.now().strftime(
            "%Y%m%d"
        )


        count = ws.max_row


        return (

            f"JOB-{today}-"
            f"{count:04d}"

        )
