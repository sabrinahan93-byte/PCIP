from pcip.company_loader import load_companies
from pcip.excel.workbook import DashboardWorkbook
from pcip.scanner.career import scan_career_page
from pcip.scanner.job_parser import extract_jobs
from pcip.run_logger import write_scan_log

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


    # 当前测试前5个source
    for source in sources[:5]:


        print(
            "\nScanning:",
            source["Company"],
            source["SourceType"]
        )


        result = scan_career_page(
            source["URL"]
        )


        if result[0]["status"] == "success":

            status = "Success"


        else:

            status = "Failed"



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


        print(scan_item)



        # 成功页面解析岗位

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



    # 写扫描日志

    write_scan_log(

        dashboard.file_path,

        scan_results

    )



    # 写岗位

    if all_jobs:


        dashboard.write_jobs(

            all_jobs

        )


        print(

            "Jobs written:",

            len(all_jobs)

        )



    print(

        "Total Jobs Found:",

        len(all_jobs)

    )




if __name__ == "__main__":

    main()
