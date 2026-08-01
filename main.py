from pcip.excel.workbook import DashboardWorkbook
from pcip.company_loader import load_companies


def main():

    dashboard = DashboardWorkbook()

    dashboard.initialize()

    companies = load_companies()

    dashboard.write_companies(companies)


if __name__ == "__main__":

    main()
