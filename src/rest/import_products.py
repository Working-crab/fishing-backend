import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def sheet_id_from_url(url):
    return url.lstrip('https://').lstrip('http://').lstrip('docs.google.com/spreadsheets/d/').split('/', 1)[0]

def import_products_from_google_sheet(sheet_id):
    API_KEY = 'AIzaSyBE_kByUf5VcW8i7L6SJjrsnER-cFfVPLE'

    try:
        service = build('sheets', 'v4', developerKey=API_KEY)

        # Call the Sheets API
        spreadsheets = service.spreadsheets()
        document = spreadsheets.get(spreadsheetId=sheet_id).execute()
        sheet = document['sheets'][0]['properties']['title']
        result = spreadsheets.values().get(spreadsheetId=sheet_id,
                                    range=sheet).execute()
        values = result.get('values', [])

        if not values:
            print('No data found.')
            return

        print('Name, Major:')
        for row in values:
            # Print columns A and E, which correspond to indices 0 and 4.
            print('%s, %s' % (row[0], row[4]))
    except HttpError as err:
        print(err)
