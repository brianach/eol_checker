import gspread
import random
from google.oauth2.service_account import Credentials
from datetime import timedelta, datetime

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('credentials.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("ci-project-3")
HARDWARE = SHEET.worksheet("hardware")

HARDWARE.batch_clear(["A2:H60"])  # clear the worksheet to run simulation

g_row = 'U05009122022', 'L05009122022', 'S05009122022', 'D05009122022', 'K05009122022', 'M05009122022', 'P05009122022'
HARDWARE.append_row(g_row)
