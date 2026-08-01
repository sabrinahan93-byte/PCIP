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


    for source in sources[:5]:

        print(
            "\nScanning:",
            source["Company"],
            source["SourceType"]
        )

        result = scan_career_page(
            source["URL"]
        )

        print(result)



if __name__ == "__main__":

    main()
