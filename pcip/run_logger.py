# pcip/run_logger.py

from openpyxl import load_workbook
from datetime import datetime


def write_scan_log(
    file_path,
    scan_results
):

    """
    Release 5.4

    Only writes Sheet 3 Run_Log.

    Sheet 4 Run_Detail ownership:
    DashboardWorkbook.write_jobs()
    DashboardWorkbook.write_scan_failure()

    This function MUST NOT write Run_Detail.
    """



    wb = load_workbook(
        file_path
    )


    ws = wb["Run_Log"]



    run_time = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )



    companies_scanned = len(
        scan_results
    )



    failed_companies = 0



    new_jobs = 0

    updated_jobs = 0



    for record in scan_results:


        if record.get(
            "Status"
        ) != "Success":

            failed_companies += 1



    result = (

        "Success"

        if failed_companies == 0

        else "Partial"

    )



    ws.append([

        run_time,

        companies_scanned,

        new_jobs,

        updated_jobs,

        0,

        failed_companies,

        "",

        result

    ])



    wb.save(
        file_path
    )
