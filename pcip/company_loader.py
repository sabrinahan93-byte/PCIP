import csv
from pathlib import Path


def load_companies(csv_path="config/companies.csv"):

    companies = []

    csv_file = Path(csv_path)

    if not csv_file.exists():
        raise FileNotFoundError(f"{csv_path} not found.")

    with open(csv_file, newline="", encoding="utf-8-sig") as file:

        reader = csv.DictReader(file)

        for row in reader:

            companies.append(row)

    return companies
