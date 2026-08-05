from openpyxl import load_workbook
from openpyxl.worksheet.datavalidation import DataValidation


file_path = "output/Job_Dashboard.xlsx"


wb = load_workbook(file_path)


ws = wb["Jobs"]


# Remove old validation if exists
ws.data_validations.dataValidation = []


# Create Pipeline Status dropdown

pipeline_validation = DataValidation(
    type="list",
    formula1='"New,Watching,Applied,Interview,Rejected,Offer"',
    allow_blank=True
)


ws.add_data_validation(
    pipeline_validation
)


pipeline_validation.add(
    "J2:J1000"
)


wb.save(file_path)


print("Pipeline Status dropdown restored successfully")
