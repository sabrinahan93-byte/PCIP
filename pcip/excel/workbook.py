from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter
from pathlib import Path
from datetime import datetime



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



class DashboardWorkbook:



    def __init__(self):

        self.file_path = (
            "output/Job_Dashboard.xlsx"
        )



    # =================================
    # Initialize + Migration
    # =================================


    def initialize(self):


        path = Path(
            self.file_path
        )


        path.parent.mkdir(
            exist_ok=True
        )


        if not path.exists():


            self.create_new_workbook()


        else:


            self.migrate_schema()



    def create_new_workbook(self):


        wb = Workbook()


        ws = wb.active

        ws.title = "Jobs"


        ws.append(
            JOBS_HEADERS
        )


        companies = wb.create_sheet(
            "Companies"
        )


        companies.append(
            COMPANIES_HEADERS
        )


        run_log = wb.create_sheet(
            "Run_Log"
        )


        run_log.append(
            RUN_LOG_HEADERS
        )


        run_detail = wb.create_sheet(
            "Run_Detail"
        )


        run_detail.append(
            RUN_DETAIL_HEADERS
        )


        for sheet in wb:

            self.format_sheet(
                sheet
            )


        self.add_pipeline_validation(
            ws
        )


        wb.save(
            self.file_path
        )



    # =================================
    # Schema Migration
    # =================================


    def migrate_schema(self):


        wb = load_workbook(
            self.file_path
        )


        self.migrate_jobs_sheet(
            wb
        )


        self.ensure_sheet(
            wb,
            "Companies",
            COMPANIES_HEADERS
        )


        self.ensure_sheet(
            wb,
            "Run_Log",
            RUN_LOG_HEADERS
        )


        self.ensure_sheet(
            wb,
            "Run_Detail",
            RUN_DETAIL_HEADERS
        )


        wb.save(
            self.file_path
        )



    def migrate_jobs_sheet(
        self,
        wb
    ):


        if "Jobs" not in wb.sheetnames:


            ws = wb.create_sheet(
                "Jobs"
            )


            ws.append(
                JOBS_HEADERS
            )

            return



        ws = wb["Jobs"]



        old_headers = [

            cell.value

            for cell in ws[1]

        ]



        if old_headers == JOBS_HEADERS:

            return



        old_data = []



        for row in ws.iter_rows(
            min_row=2,
            values_only=True
        ):


            old_data.append(
                dict(
                    zip(
                        old_headers,
                        row
                    )
                )
            )



        wb.remove(
            ws
        )


        ws = wb.create_sheet(
            "Jobs",
            0
        )


        ws.append(
            JOBS_HEADERS
        )



        for item in old_data:


            ws.append(

                [

                    item.get(
                        "Job ID",
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
                        "Location",
                        ""
                    ),

                    item.get(
                        "Work Mode",
                        ""
                    ),

                    item.get(
                        "Match Score",
                        0
                    ),

                    item.get(
                        "Job URL",
                        ""
                    ),

                    item.get(
                        "Last Seen",
                        ""
                    ),

                    item.get(
                        "Last Notified",
                        ""
                    ),

                    item.get(
                        "Pipeline Status",
                        "New"
                    ),

                    item.get(
                        "Applied Date",
                        ""
                    ),

                    item.get(
                        "Notes",
                        ""
                    )

                ]

            )


        self.add_pipeline_validation(
            ws
        )


        self.format_sheet(
            ws
        )    
    # =================================
    # Sheet Helpers
    # =================================


    def ensure_sheet(
        self,
        wb,
        name,
        headers
    ):


        if name not in wb.sheetnames:


            ws = wb.create_sheet(
                name
            )


            ws.append(
                headers
            )


            self.format_sheet(
                ws
            )



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
                        len(
                            str(
                                cell.value
                            )
                        )
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

            formula1='"'
            +
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



    # =================================
    # Job Write Engine
    # =================================


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


        changes = []


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




    # =================================
    # Existing Job Update
    # =================================


    def update_existing_job(
        self,
        ws,
        row,
        job,
        today
    ):


        system_updates = {


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



        for column, value in system_updates.items():


            ws.cell(

                row=row,

                column=column

            ).value = value



        # NEVER UPDATE:
        #
        # Column 10 Pipeline Status
        # Column 11 Applied Date
        # Column 12 Notes



    # =================================
    # Run Log
    # =================================


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


        wb.save(
            self.file_path
        )



    # =================================
    # Run Detail
    # =================================


    def write_run_detail(
        self,
        changes
    ):


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


        wb.save(
            self.file_path
        )



    # =================================
    # Job Identity
    # =================================


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


            result[key] = row



        return result




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


        if not text:

            return ""


        return (

            str(text)

            .lower()

            .strip()

        )



    def generate_job_id(
        self,
        ws
    ):


        today = datetime.now().strftime(
            "%Y%m%d"
        )


        return (

            "JOB-"

            +

            today

            +

            "-"

            +

            str(
                ws.max_row
            ).zfill(4)

        )
