from pcip.company_loader import load_companies
from pcip.excel.workbook import DashboardWorkbook
from pcip.scanner.career import scan_career_page
from pcip.scanner.job_parser import extract_jobs
from pcip.run_logger import write_scan_log
from pcip.utils.dedup import filter_new_jobs

import csv



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


            all_jobs.extend(
                jobs
            )



    write_scan_log(

        dashboard.file_path,

        scan_results

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
                new_jobs
            )


            print(
                "Jobs written:",
                len(new_jobs)
            )


        else:


            print(
                "No new jobs"
            )



    else:


        print(
            "No jobs found"
        )



    print(
        "Total Jobs Scanned:",
        len(all_jobs)
    )



if __name__ == "__main__":

    main()
