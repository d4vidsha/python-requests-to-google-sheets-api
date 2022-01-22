from requests import request
import json

# config
CLIENT_ID = "794014765743-15nu01eqhjdpo4fh93lm404md8mic6ni.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REFRESH_TOKEN = "1//0go5ygZcgr82mCgYIARAAGBASNwF-L9IrBaWQIu4a-38XKInYWYr9Hx66vY_wvhNg0g5lq5hMG9vzysGwtSDAh666VXFbNeWlg4M"
SID = "1YUCXFilyFqR-C8LNGSm551GhT1Nh9G3q_5KjUqnjIds"

# constants
SPACE = " "

''' Given the refresh token, return the response which includes the access
    token and other bits of information.
'''
def refresh_access_token(refresh_tkn):
    url = "https://accounts.google.com/o/oauth2/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "refresh_token": refresh_tkn
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded"
    }

    r = request("POST", url, data=data, headers=headers)
    return r

''' Given a string message, row index and column index, return the payload of
    a cell.
'''
def a_cell(message, row, col):
    cell = {
        "updateCells": {
            "rows": [
                {
                    "values": [
                        {
                            "userEnteredValue": {
                                "stringValue": message
                            }
                        }
                    ]
                }
            ],
            "fields": "*",
            "start": {
                "sheetId": 0,
                "rowIndex": row,
                "columnIndex": col
            }
        }
    }
    return cell

''' Generate the request with the default intention of filling the entire row
    at `index` with the list of messages. If `row_fill` is set to `False`, 
    the column at `index` will be filled instead.
'''
def generate_request(messages, index, row_fill=True):
    requests = []
    if row_fill:
        for i in range(len(messages)):
            requests.append(a_cell(messages[i], index, i))
    # column fill
    else:
        for i in range(len(messages)):
            requests.append(a_cell(messages[i], i, index))
    return requests

class gsheets():

    def __init__(self, refresh_tkn):
        r = refresh_access_token(refresh_tkn)
        data = r.json()
        self.token = data["access_token"]
        self.token_type = data["token_type"]

    def update_cells(self, messages, spreadsheet_id):
        url = "https://sheets.googleapis.com/v4/spreadsheets/" \
            + f"{spreadsheet_id}:batchUpdate"
        
        body = {
            "requests": generate_request(messages, 0),
            "includeSpreadsheetInResponse": False,
            "responseRanges": [],
            "responseIncludeGridData": False
        }
        
        headers = {
            "Authorization": self.token_type + SPACE + self.token
        }

        r = request("POST", url, data=json.dumps(body), headers=headers)
        return r

def main():
    # post all important info to Google Sheets
    messages = ("cell1", "cell2", "cell3", "cell4")
    gs = gsheets(REFRESH_TOKEN)
    r = gs.update_cells(messages, SID)
    print(r)

if __name__ == "__main__":
    main()