from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter

from pathlib import Path
from datetime import datetime



# ===============================
# Frozen Schema Definition
# ===============================


JOBS_HEADERS = [
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


COMPANIES_HEADERS = [
    "Company",
    "Enabled",
    "Tier",
    "Career URL",
    "Last Scan",
    "Scan Status",
    "Notes"
]


RUN_LOG_HEADERS = [
    "Run Time",
    "Companies Scanned",
    "New Jobs",
    "Updated Jobs",
    "Closed Jobs",
    "Failed Companies",
    "Duration",
    "Result"
]


RUN_DETAIL_HEADERS = [
    "Run Time",
    "Change Type",
    "Company",
    "Job Title",
    "Match Score",
    "Job URL"
]


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



    # =====================================
    # Initialize
    # =====================================


    def initialize(self):

        path = Path(
            self.file_path
        )


        path.parent.mkdir(
            exist_ok=True
        )


        if not path.exists():

            self.create_workbook()

        else:

            self.migrate_workbook()



    # =====================================
    # Create New Workbook
    # =====================================


    def create_workbook(self):


        wb = Workbook()


        ws = wb.active

        ws.title = "Jobs"


        ws.append(
            JOBS_HEADERS
        )


        company_ws = wb.create_sheet(
            "Companies"
        )


        company_ws.append(
            COMPANIES_HEADERS
        )


        log_ws = wb.create_sheet(
            "Run_Log"
        )


        log_ws.append(
            RUN_LOG_HEADERS
        )


        detail_ws = wb.create_sheet(
            "Run_Detail"
        )


        detail_ws.append(
            RUN_DETAIL_HEADERS
        )


        for sheet in wb:

            self.format_sheet(
                sheet
            )


        self.add_pipeline_dropdown(
            ws
        )


        wb.save(
            self.file_path
        )



    # =====================================
    # Full Workbook Migration
    # =====================================


    def migrate_workbook(self):


        wb = load_workbook(
            self.file_path
        )


        self.migrate_sheet(
            wb,
            "Jobs",
            JOBS_HEADERS
        )


        self.migrate_sheet(
            wb,
            "Companies",
            COMPANIES_HEADERS
        )


        self.migrate_sheet(
            wb,
            "Run_Log",
            RUN_LOG_HEADERS
        )


        self.migrate_sheet(
            wb,
            "Run_Detail",
            RUN_DETAIL_HEADERS
        )


        self.add_pipeline_dropdown(
            wb["Jobs"]
        )


        wb.save(
            self.file_path
        )



    # =====================================
    # Generic Sheet Migration
    # =====================================


    def migrate_sheet(
        self,
        wb,
        sheet_name,
        target_headers
    ):


        if sheet_name not in wb.sheetnames:


            ws = wb.create_sheet(
                sheet_name
            )


            ws.append(
                target_headers
            )


            self.format_sheet(
                ws
            )


            return



        old_ws = wb[sheet_name]


        old_headers = [

            cell.value

            for cell in old_ws[1]

        ]



        if old_headers == target_headers:

            return



        # read old data

        old_records = []



        for row in old_ws.iter_rows(

            min_row=2,

            values_only=True

        ):


            old_records.append(

                dict(

                    zip(

                        old_headers,

                        row

                    )

                )

            )



        index = wb.sheetnames.index(
            sheet_name
        )


        wb.remove(
            old_ws
        )


        new_ws = wb.create_sheet(
            sheet_name,
            index
        )


        new_ws.append(
            target_headers
        )


        # field name based migration


        for record in old_records:


            new_ws.append(

                [

                    record.get(
                        field,
                        ""
                    )

                    for field in target_headers

                ]

            )


        self.format_sheet(
            new_ws
        )
            # =====================================
    # Formatting
    # =====================================


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


            max_length = 0


            column_letter = get_column_letter(
                column[0].column
            )


            for cell in column:


                if cell.value:


                    max_length = max(

                        max_length,

                        len(
                            str(
                                cell.value
                            )
                        )

                    )



            ws.column_dimensions[
                column_letter
            ].width = min(

                max_length + 3,

                45

            )



    # =====================================
    # Pipeline Dropdown
    # =====================================


    def add_pipeline_dropdown(
        self,
        ws
    ):


        dv = DataValidation(

            type="list",

            formula1='"New,Watch,Applied,Interview,Offer,Accepted,Rejected,Declined"',

            allow_blank=True

        )


        ws.add_data_validation(
            dv
        )


        dv.add(
            "J2:J5000"
        )



    # =====================================
    # Companies Sync
    # =====================================


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


            if not name:

                continue



            if name not in existing:


                ws.append(

                    [

                        name,

                        company.get(
                            "Enabled",
                            True
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



        self.format_sheet(
            ws
        )


        wb.save(
            self.file_path
        )



    # =====================================
    # Write Jobs
    # =====================================


    def write_jobs(
        self,
        jobs
    ):


        wb = load_workbook(
            self.file_path
        )


        ws = wb["Jobs"]



        existing_jobs = self.build_job_index(
            ws
        )


        today = datetime.now().strftime(
            "%Y-%m-%d"
        )


        new_count = 0

        updated_count = 0

        changes = []



        for job in jobs:



            key = self.create_key(
                job
            )



            if key in existing_jobs:



                row = existing_jobs[key]



                self.update_existing_job(

                    ws,

                    row,

                    job,

                    today

                )


                updated_count += 1



                changes.append(

                    {

                        "Change Type":
                            "UPDATED",

                        "Company":
                            job.get(
                                "Company",
                                ""
                            ),

                        "Job Title":
                            job.get(
                                "Job Title",
                                ""
                            ),

                        "Match Score":
                            job.get(
                                "Match Score",
                                0
                            ),

                        "Job URL":
                            job.get(
                                "Job URL",
                                ""
                            )

                    }

                )



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



                changes.append(

                    {

                        "Change Type":
                            "NEW",

                        "Company":
                            job.get(
                                "Company",
                                ""
                            ),

                        "Job Title":
                            job.get(
                                "Job Title",
                                ""
                            ),

                        "Match Score":
                            job.get(
                                "Match Score",
                                0
                            ),

                        "Job URL":
                            job.get(
                                "Job URL",
                                ""
                            )

                    }

                )



        self.format_sheet(
            ws
        )


        wb.save(
            self.file_path
        )



        return {

            "new":
                new_count,

            "updated":
                updated_count,

            "changes":
                changes

        }



    # =====================================
    # Existing Job Update
    # =====================================


    def update_existing_job(
        self,
        ws,
        row,
        job,
        today
    ):



        updates = {


            2:
                job.get(
                    "Company",
                    ""
                ),


            3:
                job.get(
                    "Job Title",
                    ""
                ),


            4:
                job.get(
                    "Location",
                    ""
                ),


            5:
                job.get(
                    "Work Mode",
                    ""
                ),


            6:
                job.get(
                    "Match Score",
                    0
                ),


            7:
                job.get(
                    "Job URL",
                    ""
                ),


            8:
                today

        }



        for col, value in updates.items():


            ws.cell(

                row=row,

                column=col

            ).value = value



        # IMPORTANT:
        #
        # Column 10 Pipeline Status
        # Column 11 Applied Date
        # Column 12 Notes
        #
        # NEVER TOUCH
            # =====================================
    # Run Log
    # =====================================


    def write_run_log(
        self,
        data
    ):


        wb = load_workbook(
            self.file_path
        )


        ws = wb["Run_Log"]



        ws.append(

            [

                data.get(
                    "Run Time",
                    ""
                ),

                data.get(
                    "Companies Scanned",
                    0
                ),

                data.get(
                    "New Jobs",
                    0
                ),

                data.get(
                    "Updated Jobs",
                    0
                ),

                data.get(
                    "Closed Jobs",
                    0
                ),

                data.get(
                    "Failed Companies",
                    0
                ),

                data.get(
                    "Duration",
                    ""
                ),

                data.get(
                    "Result",
                    ""
                )

            ]

        )


        self.format_sheet(
            ws
        )


        wb.save(
            self.file_path
        )



    # =====================================
    # Run Detail
    # =====================================


    def write_run_detail(
        self,
        changes
    ):


        if not changes:

            return



        wb = load_workbook(
            self.file_path
        )


        ws = wb["Run_Detail"]



        run_time = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )



        for item in changes:


            ws.append(

                [

                    run_time,

                    item.get(
                        "Change Type",
                        ""
                    ),

                    item.get(
                        "Company",
                        ""
                    ),

                    item.get(
                        "Job Title",
                        ""
                    ),

                    item.get(
                        "Match Score",
                        0
                    ),

                    item.get(
                        "Job URL",
                        ""
                    )

                ]

            )



        self.format_sheet(
            ws
        )


        wb.save(
            self.file_path
        )



    # =====================================
    # Build Job Index
    # =====================================


    def build_job_index(
        self,
        ws
    ):


        index = {}



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



            if not company or not title:

                continue



            key = self.create_key(

                {

                    "Company":
                        company,

                    "Job Title":
                        title

                }

            )


            index[key] = row



        return index



    # =====================================
    # Job Key
    # =====================================


    def create_key(
        self,
        job
    ):


        return (

            self.normalize(

                job.get(
                    "Company",
                    ""
                )

            )

            +

            "|"

            +

            self.normalize(

                job.get(
                    "Job Title",
                    ""
                )

            )

        )



    def normalize(
        self,
        text
    ):


        if text is None:

            return ""



        return (

            str(text)

            .lower()

            .strip()

        )



    # =====================================
    # Generate Job ID
    # =====================================


    def generate_job_id(
        self,
        ws
    ):


        today = datetime.now().strftime(
            "%Y%m%d"
        )


        number = ws.max_row



        return (

            "JOB-"

            +

            today

            +

            "-"

            +

            str(
                number
            ).zfill(4)

        )
