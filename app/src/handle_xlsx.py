
import logging
from pandas import read_excel

logger = logging.getLogger(__name__)

def get_xlsx_rows(file_path: str) -> dict:
    logger.info(f"Processing Excel file: {file_path}")

    lst: dict = {}
    excel_lst = read_excel(file_path)
    for item in excel_lst.to_dict(orient="records"):
        if item.keys() != {"Name", "Description"}:
            logging.info(f"Invalid keys found in the Excel file: {file_path}")
            raise ValueError(f"Invalid keys in the Excel file: {file_path}")
        lst[item["Name"]] = item["Description"]
    return lst