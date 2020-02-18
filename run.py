import xlrd
from stuff import main_session
from json_creater import create_json_for_so
from sap_create_so import create_so_from_sa38

book = xlrd.open_workbook("C:/Users/s1617/Desktop/sap_excel/data.xlsm")
sheet = book.sheet_by_name("data")


def get_system():
    system = sheet.cell_value(0, 1)
    return system


def get_order_data():
    material = int(sheet.cell_value(4, 0))
    amount = int(sheet.cell_value(4, 1))
    unit = str(sheet.cell_value(4, 2))
    return material, amount, unit


def make_order_data():
    so_data_list = [
        {
            "items": [(get_order_data())],
            "time_from": 165900,
            "customer": 1000022112,
            "payment_method": "H",
        }
    ]

    data = {
        "so_list": so_data_list,
        "system": get_system(),
        "session": main_session(get_system()),
        "so": [],
        "deliveries": [],
        "future_day_process": None,  # "12.02.2020" , None -> dnes
        "B2B": False,
        "process_target": None,
    }
    return data


if __name__ == "__main__":
    data = make_order_data()
    for sales_order_data in data["so_list"]:
        json = create_json_for_so(sales_order_data, data["system"], data["B2B"], data["future_day_process"])
    create_so_from_sa38(data["session"], json)
