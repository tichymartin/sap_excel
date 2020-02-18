import xlrd
from stuff import main_session


def get_excel_data():
    book = xlrd.open_workbook("C:/Users/s1617/Desktop/sap_excel/data.xlsm")
    sheet = book.sheet_by_name("data")
    cell_value = sheet.cell_value(1, 3)
    return cell_value


def enter_vl(session, transaction):
    session.StartTransaction(Transaction=transaction)


def main():
    system = "K4D"
    session = main_session(system)
    cell_value = get_excel_data()
    enter_vl(session, cell_value)


if __name__ == "__main__":
    main()
