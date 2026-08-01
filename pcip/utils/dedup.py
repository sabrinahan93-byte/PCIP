from openpyxl import load_workbook


def normalize(value):

    if not value:
        return ""

    return (
        str(value)
        .strip()
        .lower()
        .rstrip("/")
    )



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


        company = normalize(
            row[1]
        )


        title = normalize(
            row[2]
        )


        url = normalize(
            row[9]
        )


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

            normalize(
                job.get(
                    "Company"
                )
            ),

            normalize(
                job.get(
                    "Job Title"
                )
            ),

            normalize(
                job.get(
                    "Job URL"
                )
            )

        )


        if key not in existing:


            new_jobs.append(
                job
            )



    return new_jobs
