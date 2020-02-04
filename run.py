import os
import subprocess
import time
import win32com.client
import xlrd

port_sap_gui = {"K4D": 21, "K4Q": 11, "K4T": 41, "K4B": 61}


def open_sap_gui(system):
    application_server = "-system=10.200.81.100"
    client = "-client=001"
    sys_name = f"-system={system}"
    sap_server = f"-sapserver={port_sap_gui[system]}"
    user = f'-user={os.environ.get("SAP_USER")}'
    password = f'-pw={os.environ.get("SAP_PASS")}'
    language = "-language=CS"

    gui_path = "C:/Program Files (x86)/SAP/FrontEnd/SAPgui/"
    cmd_string = os.path.join(
        gui_path,
        f"sapshcut.exe {application_server} {client} {sys_name} {sap_server} {user} {password} {language}",
    )
    subprocess.call(cmd_string)


def initialization(system):
    try:
        sap_gui_auto = win32com.client.GetObject("SAPGUI")
        if not type(sap_gui_auto) == win32com.client.CDispatch:
            return

        application = sap_gui_auto.GetScriptingEngine
        if not type(application) == win32com.client.CDispatch:
            return

        connections = application.Children

        for connection in connections:
            # print(connection.Children(0).Info.SystemName)
            sessions = connection.Children
            for session in sessions:
                if session.Info.SystemName == system:
                    return session
    # print(session.Info.SystemName)
    # print(session.Id)

    except:
        return


def try_session(system):
    while True:
        try:
            session = initialization(system)
            if session:
                break

        except:
            time.sleep(1)

    return session


def main_session(system):
    session = initialization(system)
    if not session:
        open_sap_gui(system)
        session = try_session(system)
    return session


def enter_vl(session, transaction):
    session.StartTransaction(Transaction=transaction)


def get_excel_data():
    book = xlrd.open_workbook("data.xlsx")
    sheet = book.sheet_by_name("data")
    cell_value = sheet.cell_value(1, 3)
    return cell_value


if __name__ == "__main__":
    system = "K4D"
    session = main_session(system)
    transaction = get_excel_data()
    enter_vl(session, transaction)
