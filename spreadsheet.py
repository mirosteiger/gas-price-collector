import auth

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

SHEET_ID = "1v7GV04QOVO_X3pS91gBHi3k9isdd-vudV5zAOEyFEuU"
RANGE_NAME = "Daten!A1:C1000"


def add(date, time, price):

    global service
    # Call the Sheets API
    service = auth.spreadsheet_service
    append_data(date, time, price)


def read_range():
    print("READING")
    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=SHEET_ID, range=RANGE_NAME)
        .execute()
    )
    rows = result.get("values", [])
    # print(rows)
    # print("{0} rows retrieved.".format(len(rows)))
    # print("{0} rows retrieved.".format(rows))
    return rows


def append_data(date, time, price):
    
    data = {"range": "Daten!A1:C1000", "values": [[date, time, price]]}
    body = {"body": data}

    result = (
        service.spreadsheets()
        .values()
        .append(
            spreadsheetId=SHEET_ID,
            range=RANGE_NAME,
            body=data,
            valueInputOption="USER_ENTERED",
        )
        .execute()
    )
