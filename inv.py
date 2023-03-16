import gspread
import random
from google.oauth2.service_account import Credentials
from datetime import timedelta, date, datetime

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('credentials.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("hw_inventory")

inv_heads = SHEET.worksheet("hardware").row_values(1)

for y in range(4, -1, -1):

    rdates = []
    for d in range(1,10):
        rand_days = random.randrange(1,365)
        sdate = datetime(2022, 12, 30) - timedelta((365*(y)+rand_days))
        rdates.append(sdate.strftime("%d%m%Y"))
    print(rdates)

    #edate = datetime(2022, 12, 30) - timedelta(365*y)
    #print(sdate.strftime("%d%m%Y"), edate.strftime("%d%m%Y"))

