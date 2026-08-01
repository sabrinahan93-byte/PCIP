from openpyxl import load_workbook


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

    wb = load_workbook(
        file_path
    )


    ws = wb["Jobs"]


    existing_keys = set()


    # 读取Excel已有岗位
    for row in ws.iter_rows(
        min_row=2,
        values_only=True
    ):


        company = row[1]

        title = row[2]

        url = row[9]


        key = create_job_key(

            company,

            title,

            url

        )


        existing_keys.add(
            key
        )



    print(
        "Existing jobs count:",
        len(existing_keys)
    )



    new_jobs = []



    duplicate_count = 0



    # 检查新抓取岗位

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
