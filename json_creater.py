import json
import codecs
import copy
import random
import time
from datetime import datetime, date

from system_data import outbound_b2b_customer_dict


def create_json_for_so(sales_order_data, system, B2B, future_day):
    header = {
        "sd_doc": "",
        "sales_org": "1000",
        "plant": "1000",
        "purch_no_c": "TEST",
        "purch_date": "",
        "pymt_meth": "H",
        "create_date": "20180503",
        "create_time": "080106",
        "eshop_id": "TEST",
        "dlv_block": "",
        "support_note": "",
        "client_note": "",
        "payId": "payIDGOGOGO",
        "distr_chan": "10",
        "ship_cond": "10",
        "conditions": [],
    }

    json_data = {"header": header}

    item = {
        "itm_number": "",
        "hg_lv_item": "",
        "free_item ": "",
        "material": "10000",
        "batch": "",
        "item_categ": "YDOZ",
        "short_text": "Doprava Kosik.cz",
        "long_text": "",
        "target_qty": 1,
        "target_qu": "LE",
        "altTargetQty": "",
        "altTargetQu": "",
        "dlv_group": "",
        "req_date_from": "20181003",
        "req_time_from": "210000",
        "req_date_to": "20181003",
        "req_time_to": "220000",
        "purch_no_c": "",
        "conditions": [],
    }

    # MONZNOST TVORIT ZAKAZKY DO BUDOUCNA

    today = date.today()
    if future_day is None or future_day < today.strftime("%d.%m.%Y"):
        expedition_date = date.today().strftime("%Y%m%d")
    else:
        expedition_date = datetime.strptime(future_day, "%d.%m.%Y").strftime("%Y%m%d")

    header["create_date"] = today.strftime("%Y%m%d")
    header["create_time"] = time.strftime("%H%M%S")
    item["req_date_from"] = expedition_date
    item["req_date_to"] = expedition_date

    time_from = sales_order_data.get("time_from")
    if time_from:
        if time_from > 225959:
            time_from = 225959

        item["req_time_from"] = str(time_from)
        item["req_time_to"] = str(time_from + 10000)

    json_data["items"] = [
        copy.deepcopy(item) for _ in range(len(sales_order_data.get("items")))
    ]

    for index, itm in enumerate(json_data["items"]):
        json_data["items"][index]["itm_number"] = str((index + 1) * 10)
        json_data["items"][index]["free_item "] = ""
        json_data["items"][index]["item_categ"] = ""
        json_data["items"][index]["short_text"] = ""
        json_data["items"][index]["material"] = str(
            sales_order_data.get("items")[index][0]
        )
        json_data["items"][index]["target_qty"] = sales_order_data.get("items")[index][
            1
        ]

        if isinstance(sales_order_data.get("items")[index][2], str):
            json_data["items"][index]["target_qu"] = sales_order_data.get("items")[
                index
            ][2]
        else:
            json_data["items"][index]["target_qu"] = "KG"
            json_data["items"][index]["altTargetQty"] = sales_order_data.get("items")[
                index
            ][2]
            json_data["items"][index]["altTargetQu"] = "PC"

        try:
            price = sales_order_data.get("items")[index][3]

        except IndexError:
            price = 100

        json_data["items"][index]["conditions"].append(dict())
        json_data["items"][index]["conditions"][0]["cond_type"] = "PR00"
        json_data["items"][index]["conditions"][0]["cond_value"] = price
        json_data["items"][index]["conditions"][0]["currency"] = "CZK"

    # doplneni dopravy a nastaveni cisla polozky dopravy
    json_data["items"].append(item)
    json_data["items"][-1]["itm_number"] = len(json_data["items"] * 10)

    # PAYMENT METHODS
    """
    G nebo H
    """
    pay_method = sales_order_data.get("payment_method")

    if not pay_method:
        header["pymt_meth"] = "H"
    else:
        header["pymt_meth"] = pay_method

    if pay_method == "G":

        total = 0

        for item in json_data["items"]:
            for condition in item["conditions"]:
                value_of_item = condition.get("cond_value")
                qty_of_item = item["target_qty"]
                total += value_of_item * qty_of_item

        header["conditions"].append(
            {"cond_type": "PR00", "cond_value": total, "currency": "CZK"}
        )

    customer = sales_order_data.get("customer")
    if B2B:
        json_data["header"]["distr_chan"] = "20"
        partner = {
            "partn_numb": outbound_b2b_customer_dict[system],
            "partn_role": "AG",
            "name1": "Banka",
            "name2": "SBERBANK CZ, a.s.",
            "city": "Praha 8 - Dáblice",
            "street": "Květnová",
            "house_number": "18",
            "post_code1": "180 00",
            "country": "CZ",
            "tel_number": "+420730194955",
            "mob_number": "+420730194955",
            "email": "petr.povysil@sabris.com",
            "tax_no_1": "",
            "tax_no_2": "",
            "vat_reg_no": "",
            "language": "cs",
            "latitude": "50.1454521",
            "longitude": "14.4800290",
            "transpzone": "TEST_2",
        }
    else:
        partner = {
            "partn_numb": customer,
            "partn_role": "AG",
            "name1": "Karel",
            "name2": "Černý",
            "city": "Praha",
            "street": "Písková",
            "house_number": "12",
            "post_code1": "170 00",
            "country": "CZ",
            "tel_number": "+420728212509",
            "email": "karelcerny@gmail.com",
            "tax_no_1": "",
            "tax_no_2": "",
            "vat_reg_no": "",
            "language": "cs",
            "longitude": "14.4105535315",
            "latitude": "50.0012306417",
            "transpzone": "TEST_2",
        }

        first_names = [
            "Ondřej",
            "Josef",
            "Marek",
            "Radim",
            "Petr",
            "Pavel",
            "Boleslav",
            "Jan",
            "Dmitriy",
            "Štěpán",
        ]
        last_names = [
            "Černý",
            "Červený",
            "Bílý",
            "Modrý",
            "Žlutý",
            "Zelený",
            "Fialový",
            "Bodrý",
            "Mokrý",
            "Suchý",
        ]

        partner["name1"] = random.choice(first_names)
        partner["name2"] = random.choice(last_names)

    json_data["partners"] = [copy.deepcopy(partner)]

    jsdata = json.dumps(json_data, indent=4, ensure_ascii=False)

    with codecs.open("json_outbound.txt", "w", encoding="UTF-8") as outfile:
        json.dump(json_data, outfile, indent=4, ensure_ascii=False)

    return jsdata


if __name__ == "__main__":
    so_data = {
        "items": [(1000456, 2, 2), (1000394, 2, "PC"), (102, 1, "JV")],
        "time_from": 205900,
        "customer": 1000022112,
        "payment_method": "H",
    }
    # item = (1000360, 1, "PC")
    # items = []
    # for _ in range(111):
    #     items.append(item)
    # material["items"] = items
    # print(material["items"])

    print(create_json_for_so(so_data, "K4T", False))
