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


        counter = (
            ws.max_row
        )



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



        wb.save(
            self.file_path
        )



    def update_existing_job(
        self,
        row_number,
        job
    ):


        wb = load_workbook(
            self.file_path
        )


        ws = wb["Jobs"]


        # 只更新系统字段
        # 不触碰人工字段


        ws.cell(
            row=row_number,
            column=2
        ).value = job.get(
            "Company",
            ""
        )


        ws.cell(
            row=row_number,
            column=3
        ).value = job.get(
            "Job Title",
            ""
        )


        ws.cell(
            row=row_number,
            column=10
        ).value = job.get(
            "Job URL",
            ""
        )


        ws.cell(
            row=row_number,
            column=11
        ).value = job.get(
            "Official Source",
            ""
        )


        # Column 8:
        # Pipeline Status
        #
        # 保留人工修改


        # Column 9:
        # Applied Date
        #
        # 保留人工修改



        wb.save(
            self.file_path
        )
