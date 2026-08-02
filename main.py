# main.py

from datetime import datetime
import csv


from pcip.company_loader import load_companies
from pcip.excel.workbook import DashboardWorkbook

from pcip.scanner.career import scan_career_page
from pcip.scanner.job_parser import extract_jobs

from pcip.run_logger import write_scan_log
from pcip.dashboard.html_report import generate_html_dashboard

from pcip.filtering.job_filter import (
    apply_match_score,
    is_relevant_job
)

from pcip.scanner.ats.detector import detect_ats



def load_sources():

    sources = []


    with open(
        "config/company_sources.csv",
        encoding="utf-8-sig"
    ) as file:


        reader = csv.DictReader(
            file
        )


        for row in reader:


            if row["Enabled"].upper() == "TRUE":

                sources.append(
                    row
                )


    return sources




def run_ats_detection(
    sources
):

    print(
        "\nATS Detection Started"
    )


    ats_results = []


    for source in sources:


        result = detect_ats(
            source["URL"]
        )


        record = {


            "Company":

                source["Company"],


            "ATS":

                result.get(
                    "ATS",
                    "Unknown"
                ),


            "ATS_URL":

                result.get(
                    "ATS_URL",
                    ""
                ),


            "Confidence":

                result.get(
                    "Confidence",
                    0
                )

        }


        ats_results.append(
            record
        )


        print(
            record
        )


    return ats_results




def main():


    start_time = datetime.now()



    dashboard = DashboardWorkbook()


    dashboard.initialize()



    companies = load_companies()



    dashboard.sync_companies(
        companies
    )



    sources = load_sources()



    #
    # ATS Detection
    #

    run_ats_detection(
        sources
    )



    scan_results = []

    all_jobs = []



    #
    # Release 5.4
    # Remove source limit
    #

    for source in sources:



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



        scan_record = {


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

            scan_record

        )



        print(

            scan_record

        )



        #
        # Scan Failed
        #

        if result[0]["status"] != "success":


            continue




        jobs = extract_jobs(

            result[0]["html"],

            source["URL"],

            source["Company"]

        )



        print(

            "Jobs Found:",

            len(jobs)

        )



        for job in jobs:



            job = apply_match_score(

                job

            )



            if is_relevant_job(

                job

            ):


                all_jobs.append(

                    job

                )




    print(

        "Relevant Jobs:",

        len(all_jobs)

    )



    new_jobs = 0

    updated_jobs = 0



    if all_jobs:


        write_result = dashboard.write_jobs(

            all_jobs

        )


        new_jobs = write_result["new"]

        updated_jobs = write_result["updated"]



        print(

            "New Jobs:",

            new_jobs

        )


        print(

            "Updated Jobs:",

            updated_jobs

        )



    else:


        print(

            "No relevant jobs found"

        )




    #
    # Release 5.4
    # Write failed scan events into Sheet 4
    #

    failures = [

        item

        for item in scan_results

        if item["Status"] != "Success"

    ]



    if failures:


        dashboard.write_scan_failure(

            failures

        )



    duration = (

        datetime.now()

        -

        start_time

    )



    #
    # Run Log
    #

    write_scan_log(

        dashboard.file_path,

        scan_results

    )
    generate_html_dashboard(

    dashboard.file_path

)


    print(

        "Duration:",

        duration

    )





if __name__ == "__main__":

    main()
