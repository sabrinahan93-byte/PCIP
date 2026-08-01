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


    print(
        "Dedup reading file:",
        absolute_path
    )


    if not absolute_path.exists():

        print(
            "File not found"
        )

        return jobs



    wb = load_workbook(
        absolute_path
    )


    print(
        "Workbook sheets:",
        wb.sheetnames
    )


    ws = wb["Jobs"]


    existing_keys = set()



    print(
        "Jobs sheet max row:",
        ws.max_row
    )



    for row in ws.iter_rows(
        min_row=2,
        values_only=True
    ):


        company = row[1]

        title = row[2]

        url = row[9]


        if company or title or url:

            existing_keys.add(

                create_job_key(

                    company,

                    title,

                    url

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
