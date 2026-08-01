from datetime import datetime
from openpyxl import load_workbook


def write_scan_log(
        file_path,
        scan_results
):

    wb = load_workbook(file_path)

    ws_detail = wb["Run_Detail"]

    failed = []

    success_count = 0


    now = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


    for item in scan_results:

        ws_detail.append(
            [
                now,
                item["Company"],
                item["SourceType"],
                item["URL"],
                item["Status"],
                item.get("Error", "")
            ]
        )


        if item["Status"] == "Success":
            success_count += 1
        else:
            failed.append(
    f'{item["Company"]}({item["SourceType"]}:{item.get("Error","Unknown")})'
)


    ws_log = wb["Run_Log"]


    ws_log.append(
        [
            now,
            len(scan_results),
            "",
            success_count,
            ",".join(list(set(failed))),
            "",
            "",
            "Completed"
        ]
    )


    wb.save(file_path)
