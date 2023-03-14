import frappe
import requests
import base64
import json


@frappe.whitelist()
def make_api_call(datetime, invoice_id, issued_date, currency, customer, customer_address, items, item_count):
    encoded_string = "ewoic2VsbGVyRGV0YWlscyI6IHsKInRpbiI6ICIxMDAxNTI0MDk5IiwKIm5pbkJybiI6ICIiLAoibGVnYWxOYW1lIjogIlRSVUUgTk9SVEggQ09OU1VMVCBMVEQiLAoiYnVzaW5lc3NOYW1lIjogIlRSVUUgTk9SVEggQ09OU1VMVCBMVEQiLAoiYWRkcmVzcyI6ICJQbG90IDc3IFl1c3VmIEx1bGUgUm9hZCIsCiJtb2JpbGVQaG9uZSI6ICIiLAoibGluZVBob25lIjogIiIsCiJlbWFpbEFkZHJlc3MiOiAibWFpbHRvOmluZm9AdHJ1ZW5vcnRoYWZyaWNhLmNvbSIsCiJwbGFjZU9mQnVzaW5lc3MiOiAiIiwKInJlZmVyZW5jZU5vIjogIlJFRjY5Njc2NyIsCiJicmFuY2hJZCI6ICIiCgp9LAoiYmFzaWNJbmZvcm1hdGlvbiI6IHsKImludm9pY2VObyI6ICIiLAoiYW50aWZha2VDb2RlIjogIiIsCiJkZXZpY2VObyI6ICJUQ1MyM2Y5Y2YyNjE1ODcyMjM4IiwKImlzc3VlZERhdGUiOiAiMjAyMi0xMi0wMSAxMjowODowNyIsCiJvcGVyYXRvciI6ICJQYXVsIFNzZXJ1YmlyaSIsCiJjdXJyZW5jeSI6ICJVR1giLAoib3JpSW52b2ljZUlkIjogIiIsCiJpbnZvaWNlVHlwZSI6ICIxIiwKImludm9pY2VLaW5kIjogIjEiLAoiZGF0YVNvdXJjZSI6ICIxMDEiLAoiaW52b2ljZUluZHVzdHJ5Q29kZSI6ICIxMDEiLAoiaXNCYXRjaCI6ICIwIgp9LAoiYnV5ZXJEZXRhaWxzIjogewoiYnV5ZXJUaW4iOiAiMTAwMDE3MTI4NCIsCiJidXllck5pbkJybiI6ICIiLAoiYnV5ZXJQYXNzcG9ydE51bSI6ICIiLAoiYnV5ZXJMZWdhbE5hbWUiOiAiVEVQVSIsCiJidXllckJ1c2luZXNzTmFtZSI6ICJURVBVIiwKImJ1eWVyQWRkcmVzcyI6ICIyMSBZVVNVRiBMVUxFIFJPQUQgQ09VUlNFIFZJRVcgVE9XRVJTIiwKImJ1eWVyRW1haWwiOiAiIiwKImJ1eWVyTW9iaWxlUGhvbmUiOiAiIiwKImJ1eWVyTGluZVBob25lIjogIjAxMC0iLAoiYnV5ZXJQbGFjZU9mQnVzaSI6ICIiLAoiYnV5ZXJUeXBlIjogIjAiLAoiYnV5ZXJSZWZlcmVuY2VObyI6ICIiCn0sCiJnb29kc0RldGFpbHMiOiBbCnsKICAgICAgICAgICAgICAgICAgICAiaXRlbSI6ICJNYW5hZ2VtZW50IEZlZXMgKERlZW1lZCkiLAoiaXRlbUNvZGUiOiAiMDEwIiwKInF0eSI6ICIyMi4wMCIsCiJ1bml0T2ZNZWFzdXJlIjogIjExNyIsCiJ1bml0UHJpY2UiOiAiODY3NTAuMDAiLAoidG90YWwiOiAiMTkwODUwMC4wMCIsCiJ0YXhSYXRlIjogIjAuMTgiLAoidGF4IjogIjI5MTEyNy4xMSIsCiJkaXNjb3VudFRvdGFsIjogIiIsCiJkaXNjb3VudFRheFJhdGUiOiAiIiwKIm9yZGVyTnVtYmVyIjogIjAiLAoiZGlzY291bnRGbGFnIjogIjIiLAoiZGVlbWVkRmxhZyI6ICIxIiwKImV4Y2lzZUZsYWciOiAiMiIsCiJjYXRlZ29yeUlkIjogIiIsCiJjYXRlZ29yeU5hbWUiOiAiIiwKImdvb2RzQ2F0ZWdvcnlJZCI6ICI4MDExMTcwMSIsCiJnb29kc0NhdGVnb3J5TmFtZSI6ICIiLAoiZXhjaXNlUmF0ZSI6ICIiLAoiZXhjaXNlUnVsZSI6ICIiLAoiZXhjaXNlVGF4IjogIiIsCiJwYWNrIjogIiIsCiJzdGljayI6ICIiLAoiZXhjaXNlVW5pdCI6ICIiLAoiZXhjaXNlQ3VycmVuY3kiOiAiIiwKImV4Y2lzZVJhdGVOYW1lIjogIiIKfQpdLAoidGF4RGV0YWlscyI6IFsKewoKICAgICAgICAgICAgInRheENhdGVnb3J5Q29kZSI6ICIwNCIsCiAgICAgICAgICAgIm5ldEFtb3VudCI6ICIxNjE3MzcyLjg5IiwKICAgICAgICAgICAidGF4UmF0ZSI6ICIwLjE4IiwKICAgICAgICAgICAidGF4QW1vdW50IjogIjI5MTEyNy4xMSIsCiAgICAgICAgICAgImdyb3NzQW1vdW50IjogIjE5MDg1MDAuMDAiLAogICAgICAgICAgICJleGNpc2VVbml0IjogIiIsCiAgICAgICAgICAgImV4Y2lzZUN1cnJlbmN5IjogIiIsCiAgICAgICAgICAgInRheFJhdGVOYW1lIjogIiIKICAgICAgICAgICAgfQpdLAoic3VtbWFyeSI6IHsKIm5ldEFtb3VudCI6ICIxNjE3MzcyLjg5IiwKInRheEFtb3VudCI6ICIwIiwKImdyb3NzQW1vdW50IjogIjE2MTczNzIuODkiLAoiaXRlbUNvdW50IjogIjEiLAoibW9kZUNvZGUiOiAiMCIsCiJyZW1hcmtzIjogIk1hbnBvd2VyIFByb3Zpc2lvbiBIZWFkIG9mIEFjY291bnRpbmcgZm9yIE5vdiAyMDIyLSBMYXdyZW5jZSBTYWt1IiwKInFyQ29kZSI6ICIiCn0sCiJwYXlXYXkiOiBbewoicGF5bWVudE1vZGUiOiAiMTA3IiwKInBheW1lbnRBbW91bnQiOiAiMTkwODUwMC4wMCIsCiJvcmRlck51bWJlciI6ICIxMDAwNzYyODA1Igp9XSwKImV4dGVuZCI6IHt9Cgp9"
    decoded_bytes = base64.b64decode(encoded_string)
    decoded_string = decoded_bytes.decode("utf-8")
    decoded_dict = json.loads(decoded_string)

    user = frappe.session.user
    user_doc = frappe.get_doc("User", user)
    full_name = user_doc.full_name

    customer_doc = frappe.get_doc("Customer", f"{customer}")
    customer_email = customer_doc.email_id

    buyer_type = 0
    if customer_doc == "Individual":
        buyer_type = 1

    items_dict = json.loads(items)

    items_details = []
    for item in items_dict:
        item_details = {
            "item": f"{item['item_name']}",
            "itemCode": f"{item['item_code']}",
            "qty": f"{item['qty']}",
            "unitOfMeasure": "117", #item uom
            "unitPrice": "86750.00", #item unit price
            "total": "1908500.00", #invoice total amount
            "taxRate": "0.18", #item 
            "tax": "291127.11",
            "discountTotal": "",
            "discountTaxRate": "",
            "orderNumber": "0",
            "discountFlag": "2",
            "deemedFlag": "1",
            "exciseFlag": "2",
            "categoryId": "",
            "categoryName": "",
            "goodsCategoryId": "80111701",
            "goodsCategoryName": "",
            "exciseRate": "",
            "exciseRule": "",
            "exciseTax": "",
            "pack": "",
            "stick": "",
            "exciseUnit": "",
            "exciseCurrency": "",
            "exciseRateName": ""
        }

        items_details.append(item_details)

    # Data dict
    data_dict = {
        "sellerDetails": {
            "tin": "1001524099",  # static
            "ninBrn": "",
            "legalName": "TRUE NORTH CONSULT LTD",  # static
            "businessName": "TRUE NORTH CONSULT LTD",  # static
            "address": "Plot 77 Yusuf Lule Road",  # static
            "mobilePhone": "",
            "linePhone": "",
            "emailAddress": "mailto:info@truenorthafrica.com",  # static
            "placeOfBusiness": "",
            "referenceNo": f"{invoice_id}",  # Invoice number(Dynamic)
            "branchId": ""
        },
        "basicInformation": {
            "invoiceNo": "",
            "antifakeCode": "",
            "deviceNo": "TCS23f9cf2615872238",  # static
            "issuedDate": f"{issued_date}",  # Date invoice was created
            "operator": f"{full_name}",  # Invoice creator
            "currency": f"{currency}",  # Invoice currency
            "oriInvoiceId": "",
            "invoiceType": "1",  # static
            "invoiceKind": "1",  # static
            "dataSource": "101",  # static
            "invoiceIndustryCode": "101",  # static
            "isBatch": "0"
        },
        "buyerDetails": {
            "buyerTin": "1000171284",  # Customer tax id
            "buyerNinBrn": "",
            "buyerPassportNum": "",
            "buyerLegalName": f"{customer}",  # Invoice customer name
            "buyerBusinessName": f"{customer}",  # Invoice customer name
            "buyerAddress": f"{customer_address}",  # Invoice customer address
            "buyerEmail": f"{customer_email}",  # Invoice customer email
            "buyerMobilePhone": "",
            "buyerLinePhone": "010-",
            "buyerPlaceOfBusi": "",
            "buyerType": f"{buyer_type}",  # Individual(1) or Company(0)
            "buyerReferenceNo": ""
        },
        "goodsDetails": items_details,
        "taxDetails": [
            {
                "taxCategoryCode": "04",  # Custom field
                "netAmount": "1617372.89",
                "taxRate": "0.18",
                "taxAmount": "291127.11",
                "grossAmount": "1908500.00",
                "exciseUnit": "",
                "exciseCurrency": "",
                "taxRateName": ""
            }
        ],
        "summary": {
            "netAmount": "1617372.89",
            "taxAmount": "0",
            "grossAmount": "1617372.89",
            "itemCount": f"{item_count}",  # Number of items on invoice
            "modeCode": "0",
            "remarks": "Manpower Provision Head of Accounting for Nov 2022- Lawrence Saku",
            "qrCode": ""
        },
        "payWay": [{
            "paymentMode": "107",
            "paymentAmount": "1908500.00",
            "orderNumber": "1000762805"
        }],
        "extend": {}
    }
    
    data_dict_json = json.dumps(data_dict)
    data_dict_encoded = base64.b64encode(data_dict_json.encode('utf-8')).decode('utf-8')

    ##

    """
    [
            {
                "item": "Management Fees (Deemed)",  # invoice Item name
                "itemCode": "010",  # invoice item code
                "qty": "22.00",  # invoice quantity
                "unitOfMeasure": "117",
                "unitPrice": "86750.00",
                "total": "1908500.00",
                "taxRate": "0.18",
                "tax": "291127.11",
                "discountTotal": "",
                "discountTaxRate": "",
                "orderNumber": "0",
                "discountFlag": "2",
                "deemedFlag": "1",
                "exciseFlag": "2",
                "categoryId": "",
                "categoryName": "",
                "goodsCategoryId": "80111701",
                "goodsCategoryName": "",
                "exciseRate": "",
                "exciseRule": "",
                "exciseTax": "",
                "pack": "",
                "stick": "",
                "exciseUnit": "",
                "exciseCurrency": "",
                "exciseRateName": ""
            }
        ]
    """

    endpoint = "http://192.168.0.31:9880/efristcs/ws/tcsapp/getInformation"
    payload = {
        "data": {
            "content": f"{data_dict_encoded}", #"ewoic2VsbGVyRGV0YWlscyI6IHsKInRpbiI6ICIxMDAxNTI0MDk5IiwKIm5pbkJybiI6ICIiLAoibGVnYWxOYW1lIjogIlRSVUUgTk9SVEggQ09OU1VMVCBMVEQiLAoiYnVzaW5lc3NOYW1lIjogIlRSVUUgTk9SVEggQ09OU1VMVCBMVEQiLAoiYWRkcmVzcyI6ICJQbG90IDc3IFl1c3VmIEx1bGUgUm9hZCIsCiJtb2JpbGVQaG9uZSI6ICIiLAoibGluZVBob25lIjogIiIsCiJlbWFpbEFkZHJlc3MiOiAibWFpbHRvOmluZm9AdHJ1ZW5vcnRoYWZyaWNhLmNvbSIsCiJwbGFjZU9mQnVzaW5lc3MiOiAiIiwKInJlZmVyZW5jZU5vIjogIlJFRjY5Njc2NzkwIiwKImJyYW5jaElkIjogIiIKCn0sCiJiYXNpY0luZm9ybWF0aW9uIjogewoiaW52b2ljZU5vIjogIiIsCiJhbnRpZmFrZUNvZGUiOiAiIiwKImRldmljZU5vIjogIlRDUzIzZjljZjI2MTU4NzIyMzgiLAoiaXNzdWVkRGF0ZSI6ICIyMDIyLTEyLTAxIDEyOjA4OjA3IiwKIm9wZXJhdG9yIjogIlBhdWwgU3NlcnViaXJpIiwKImN1cnJlbmN5IjogIlVHWCIsCiJvcmlJbnZvaWNlSWQiOiAiIiwKImludm9pY2VUeXBlIjogIjEiLAoiaW52b2ljZUtpbmQiOiAiMSIsCiJkYXRhU291cmNlIjogIjEwMSIsCiJpbnZvaWNlSW5kdXN0cnlDb2RlIjogIjEwMSIsCiJpc0JhdGNoIjogIjAiCn0sCiJidXllckRldGFpbHMiOiB7CiJidXllclRpbiI6ICIxMDAwMTcxMjg0IiwKImJ1eWVyTmluQnJuIjogIiIsCiJidXllclBhc3Nwb3J0TnVtIjogIiIsCiJidXllckxlZ2FsTmFtZSI6ICJURVBVIiwKImJ1eWVyQnVzaW5lc3NOYW1lIjogIlRFUFUiLAoiYnV5ZXJBZGRyZXNzIjogIjIxIFlVU1VGIExVTEUgUk9BRCBDT1VSU0UgVklFVyBUT1dFUlMiLAoiYnV5ZXJFbWFpbCI6ICIiLAoiYnV5ZXJNb2JpbGVQaG9uZSI6ICIiLAoiYnV5ZXJMaW5lUGhvbmUiOiAiMDEwLSIsCiJidXllclBsYWNlT2ZCdXNpIjogIiIsCiJidXllclR5cGUiOiAiMCIsCiJidXllclJlZmVyZW5jZU5vIjogIiIKfSwKImdvb2RzRGV0YWlscyI6IFsKewogICAgICAgICAgICAgICAgICAgICJpdGVtIjogIk1hbmFnZW1lbnQgRmVlcyAoRGVlbWVkKSIsCiJpdGVtQ29kZSI6ICIwMTAiLAoicXR5IjogIjIyLjAwIiwKInVuaXRPZk1lYXN1cmUiOiAiMTE3IiwKInVuaXRQcmljZSI6ICI4Njc1MC4wMCIsCiJ0b3RhbCI6ICIxOTA4NTAwLjAwIiwKInRheFJhdGUiOiAiMC4xOCIsCiJ0YXgiOiAiMjkxMTI3LjExIiwKImRpc2NvdW50VG90YWwiOiAiIiwKImRpc2NvdW50VGF4UmF0ZSI6ICIiLAoib3JkZXJOdW1iZXIiOiAiMCIsCiJkaXNjb3VudEZsYWciOiAiMiIsCiJkZWVtZWRGbGFnIjogIjEiLAoiZXhjaXNlRmxhZyI6ICIyIiwKImNhdGVnb3J5SWQiOiAiIiwKImNhdGVnb3J5TmFtZSI6ICIiLAoiZ29vZHNDYXRlZ29yeUlkIjogIjgwMTExNzAxIiwKImdvb2RzQ2F0ZWdvcnlOYW1lIjogIiIsCiJleGNpc2VSYXRlIjogIiIsCiJleGNpc2VSdWxlIjogIiIsCiJleGNpc2VUYXgiOiAiIiwKInBhY2siOiAiIiwKInN0aWNrIjogIiIsCiJleGNpc2VVbml0IjogIiIsCiJleGNpc2VDdXJyZW5jeSI6ICIiLAoiZXhjaXNlUmF0ZU5hbWUiOiAiIgp9Cl0sCiJ0YXhEZXRhaWxzIjogWwp7CgogICAgICAgICAgICAidGF4Q2F0ZWdvcnlDb2RlIjogIjA0IiwKICAgICAgICAgICAibmV0QW1vdW50IjogIjE2MTczNzIuODkiLAogICAgICAgICAgICJ0YXhSYXRlIjogIjAuMTgiLAogICAgICAgICAgICJ0YXhBbW91bnQiOiAiMjkxMTI3LjExIiwKICAgICAgICAgICAiZ3Jvc3NBbW91bnQiOiAiMTkwODUwMC4wMCIsCiAgICAgICAgICAgImV4Y2lzZVVuaXQiOiAiIiwKICAgICAgICAgICAiZXhjaXNlQ3VycmVuY3kiOiAiIiwKICAgICAgICAgICAidGF4UmF0ZU5hbWUiOiAiIgogICAgICAgICAgICB9Cl0sCiJzdW1tYXJ5IjogewoibmV0QW1vdW50IjogIjE2MTczNzIuODkiLAoidGF4QW1vdW50IjogIjAiLAoiZ3Jvc3NBbW91bnQiOiAiMTYxNzM3Mi44OSIsCiJpdGVtQ291bnQiOiAiMSIsCiJtb2RlQ29kZSI6ICIwIiwKInJlbWFya3MiOiAiTWFucG93ZXIgUHJvdmlzaW9uIEhlYWQgb2YgQWNjb3VudGluZyBmb3IgTm92IDIwMjItIExhd3JlbmNlIFNha3UiLAoicXJDb2RlIjogIiIKfSwKInBheVdheSI6IFt7CiJwYXltZW50TW9kZSI6ICIxMDciLAoicGF5bWVudEFtb3VudCI6ICIxOTA4NTAwLjAwIiwKIm9yZGVyTnVtYmVyIjogIjEwMDA3NjI4MDUiCn1dLAoiZXh0ZW5kIjoge30KCn0=",
            "dataDescription": {
                "codeType": "0",
                "encryptCode": "1",
                "zipCode": "0"
            }
        },
        "globalInfo": {
            "appId": "AP01",
            "version": "1.1.20191201",
            "dataExchangeId": "9230489223014123",
            "interfaceCode": "T109",
            "requestCode": "TP",
            "requestTime": f"{datetime}",
            "responseCode": "TA",
            "userName": "admin",
            "deviceMAC": "FFFFFFFFFFFF",
            "deviceNo": "TCS23f9cf2615872238",
            "tin": "1001524099",
            "brn": "",
            "taxpayerID": "1",
            "longitude": "116.397128",
            "latitude": "39.916527",
            "extendField": {
                "responseDateFormat": "dd/MM/yyyy",
                "responseTimeFormat": "dd/MM/yyyy HH:mm:ss",
                "referenceNo": "21PL010020807"
            }
        },
        "returnStateInfo": {
            "returnCode": "",
            "returnMessage": ""
        }
    }

    response = requests.post(endpoint, json=payload)

    response_data = response.json()
    encoded_data_string = response_data["data"]["content"]
    decoded_data_bytes = base64.b64decode(encoded_data_string)
    decoded_data_string = decoded_data_bytes.decode("utf-8")
    decoded_data_dict = json.loads(decoded_data_string)

    # return response_data["data"]
    # frappe.errprint(response)
    # frappe.errprint("Printing response")
    return {
        "from_api": response.json(),
        "from_decoded": decoded_dict,
        "to_send": data_dict,
        "encoded": data_dict_encoded,
        "decoded_data_dict": decoded_data_dict
    }
    # return response.json().globalInfo.appId
