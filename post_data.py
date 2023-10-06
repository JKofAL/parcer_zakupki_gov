from pprint import pprint

import httplib2
from apiclient import discovery as api_discovery
from oauth2client.service_account import ServiceAccountCredentials


CREDENTIALS_FILE = "creds.json"
SHEET_ID = "1NiVa_I7L80apgNk6fWWsSWEc3HPshvw62rRHaP3YKro"

# authorize
credentials = ServiceAccountCredentials.from_json_keyfile_name(
    CREDENTIALS_FILE,
    [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
)
httpAuth = credentials.authorize(httplib2.Http())
service = api_discovery.build('sheets', 'v4', http= httpAuth)

# get data
values = service.spreadsheets().values().get(
    spreadsheetId= SHEET_ID,
    range='A1:E10'
).execute()
pprint(values)

# post data
service.spreadsheets().values().batchUpdate(
    spreadsheetId= SHEET_ID,
    body = {
        "valueInputOption": "USER_ENTERED",
        "data": [
            {"range": "B3:C4",
            "values": [['b3','c3'],['b4','c4']]}
        ]
    }
).execute()