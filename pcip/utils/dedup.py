from openpyxl import load_workbook
from pathlib import Path


def normalize(value):

    if value is None:

        return ""

    return (

        str(value)

        .strip()

        .lower()

        .replace("\n", " ")

        .rstrip("/")

    )



def create_job_key(
    company,
    title,
    url
):

    return (

        normalize(company),

        normalize(title),

        normalize(url)

    )



def filter_new_jobs(
    file_path,
    jobs
):


    absolute_path = Path(
        file_path
    ).resolve()


    wb = load_workbook(
        absolute_path
    )


    ws = wb["Jobs"]


    existing_keys = set()



    for row in ws.iter_rows(

        min_row=2,

        values_only=True

    ):


        existing_keys.add(

            create_job_key(

                row[1],

                row[2],

                row[9]

            )

        )



    print(
        "Existing jobs count:",
        len(existing_keys)
    )



    new_jobs = []

    duplicate_count = 0



    for job in jobs:


        key = create_job_key(

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


        if key in existing_keys:


            duplicate_count += 1


        else:


            print(
                "NEW JOB KEY:",
                key
            )


            new_jobs.append(
                job
            )


            existing_keys.add(
                key
            )



    print(
        "Duplicate jobs:",
        duplicate_count
    )


    print(
        "New jobs after filtering:",
        len(new_jobs)
    )



    return new_jobs
