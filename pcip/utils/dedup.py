from openpyxl import load_workbook



def filter_new_jobs(
    file_path,
    jobs
):

    wb = load_workbook(
        file_path
    )


    ws = wb["Jobs"]


    existing = set()


    for row in ws.iter_rows(
        min_row=2,
        values_only=True
    ):

        company = row[1]

        title = row[2]

        url = row[9]


        existing.add(
            (
                company,
                title,
                url
            )
        )


    new_jobs = []


    for job in jobs:

        key = (

            job.get(
                "Company",
                ""
            ),

            job.get(
                "Job Title",
                ""
            ),

            job.get(
                "Job URL",
                ""
            )

        )


        if key not in existing:

            new_jobs.append(
                job
            )


    return new_jobs
