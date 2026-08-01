from pcip.run_logger import write_scan_log
from pcip.company_loader import load_companies
from pcip.excel.workbook import DashboardWorkbook
from pcip.scanner.career import scan_career_page

import csv


def load_sources():

    sources = []

    with open(
        "config/company_sources.csv",
        encoding="utf-8-sig"
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            if row["Enabled"] == "TRUE":
                sources.append(row)

    return sources



def main():

    dashboard = DashboardWorkbook()

    dashboard.initialize()

    companies = load_companies()

    dashboard.sync_companies(companies)


    sources = load_sources()


    scan_results = []


for source in sources[:5]:

    print(
        "\nScanning:",
        source["Company"],
        source["SourceType"]
    )


    result = scan_career_page(
        source["URL"]
    )


    status = result[0]["status"]


    scan_results.append(
        {
            "Company": source["Company"],
            "SourceType": source["SourceType"],
            "URL": source["URL"],
            "Status": 
                "Success"
                if status == "success"
                else "Failed",
            "Error":
                result[0].get("error","")
        }
    )


write_scan_log(
    dashboard.file_path,
    scan_results
)


if __name__ == "__main__":

    main()
