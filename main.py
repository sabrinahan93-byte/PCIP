import csv
from datetime import datetime

from pcip.company_loader import load_companies
from pcip.excel.workbook import DashboardWorkbook
from pcip.scanner.career import scan_career_page
from pcip.scanner.job_parser import extract_jobs
from pcip.run_logger import write_scan_log
from pcip.utils.dedup import filter_new_jobs

from pcip.filtering.job_filter import apply_match_score



def load_sources():

    sources = []

    with open(
        "config/company_sources.csv",
        encoding="utf-8-sig"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            if row["Enabled"].upper() == "TRUE":

                sources.append(row)


    return sources





def main():


    start_time = datetime.now()



    dashboard = DashboardWorkbook()

    dashboard.initialize()



    companies = load_companies()


    dashboard.sync_companies(
        companies
    )



    sources = load_sources()



    scan_results = []

    all_jobs = []



    for source in sources[:5]:


        print(
            "\nScanning:",
            source["Company"],
            source["SourceType"]
        )



        result = scan_career_page(
            source["URL"]
        )



        status = (

            "Success"

            if result[0]["status"] == "success"

            else "Failed"

        )



        scan_item = {

            "Company":
                source["Company"],


            "SourceType":
                source["SourceType"],


            "URL":
                source["URL"],


            "Status":
                status,


            "Error":
                result[0].get(
                    "error",
                    ""
                )

        }



        scan_results.append(
            scan_item
        )



        print(
            scan_item
        )



        if result[0]["status"] == "success":


            jobs = extract_jobs(

                result[0]["html"],

                source["URL"],

                source["Company"]

            )



            print(
                "Jobs Found:",
                len(jobs)
            )



            # ==========================
            # Release 5.2 Commit 2
            # Apply Match Score
            # ==========================


            scored_jobs = []



            for job in jobs:


                job = apply_match_score(
                    job
                )


                scored_jobs.append(
                    job
                )



            all_jobs.extend(
                scored_jobs
            )



    # Write scan detail log

    write_scan_log(

        dashboard.file_path,

        scan_results

    )



    print(
        "Total Jobs Scanned:",
        len(all_jobs)
    )



    if all_jobs:


        new_jobs = filter_new_jobs(

            dashboard.file_path,

            all_jobs

        )



        print(
            "New Jobs:",
            len(new_jobs)
        )



        if new_jobs:


            dashboard.write_jobs(
                all_jobs
            )


            print(
                "Jobs written:",
                len(new_jobs)
            )


        else:


            print(
                "No new jobs"
            )



    duration = (
        datetime.now()
        -
        start_time
    )



    print(
        "Duration:",
        duration
    )





if __name__ == "__main__":

    main()
