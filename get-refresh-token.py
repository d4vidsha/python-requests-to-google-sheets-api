''' This script has been prepared for obtaining the access token and 
    refresh token for Google services such as Google Sheets API. By following
    the steps below you can achieve the results in my video.
    Source: https://docs.informatica.com/integration-cloud/cloud-data-integration-connectors/current-version/google-sheets-connector/introduction-to-google-sheets-connector/administration-of-google-sheets-connector/generating-oauth-2-0-access-tokens.html
'''


from requests import request

# step 1: fill in the client credentials
CLIENT_ID = "794014765743-15nu01eqhjdpo4fh93lm404md8mic6ni.apps.googleusercontent.com"
CLIENT_SECRET = "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"

# step 2: get a temporary access code manually
# https://accounts.google.com/o/oauth2/auth?access_type=offline&approval_prompt=auto&client_id=794014765743-15nu01eqhjdpo4fh93lm404md8mic6ni.apps.googleusercontent.com&response_type=code&scope=https://www.googleapis.com/auth/spreadsheets&redirect_uri=http://localhost

ACCESS_CODE = "4/0AX4XfWiXLSF3gy1-yckuXNeMWfCM5XiJSvbxZluT3kh628dJTdgBWNlcHB4oU07elF2Obg"

# get refresh token/access token from access code
url = "https://accounts.google.com/o/oauth2/token"
data = {
    "grant_type": "authorization_code",
    "code": ACCESS_CODE,
    "client_id": CLIENT_ID,
    "client_secret": CLIENT_SECRET,
    "scope": "https://www.googleapis.com/auth/spreadsheets",
    "redirect_uri": "http://localhost"
}
headers = {
    "content-type": "application/x-www-form-urlencoded"
}

r = request("POST", url, data=data, headers=headers)
print(r.text)