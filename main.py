from pcip.company_loader import load_companies
from pcip.excel.workbook import DashboardWorkbook


def main():

    dashboard = DashboardWorkbook()

    dashboard.initialize()

    companies = load_companies()

    dashboard.sync_companies(companies)


if __name__ == "__main__":

    main()
