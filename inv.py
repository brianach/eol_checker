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
SHEET = GSPREAD_CLIENT.open("hw_inventory")

inv_heads = SHEET.worksheet("hardware").row_values(1)
USERS = 50 # notional number of employees
inventory = []




def make_inv_list():

    for y in range(0, -1, -1):

        datehr = []
        userid = []
        laptop = []
        screen = []
        dockst = []
        keybrd = []
        mouses = []
        phones = []
        hiredt = []

        for d in range(1,1+USERS//5):
            rand_days = random.randrange(1,365)
            sdate = datetime(2022, 12, 30) - timedelta((365*(y)+rand_days))
            datehr.append(sdate.strftime("%d%m%Y"))
            hiredt = sorted(datehr, key=lambda hired: (hired[2:4],hired[0:2]))
        d = 0

        for hired in hiredt:

            d += 1        
            userid.append(inv_heads[0][0].capitalize() + str(d).zfill(3) + hired)
            laptop.append(inv_heads[1][0].capitalize() + str(d).zfill(3) + hired)
            screen.append(inv_heads[2][0].capitalize() + str(d).zfill(3) + hired)
            dockst.append(inv_heads[3][0].capitalize() + str(d).zfill(3) + hired)
            keybrd.append(inv_heads[4][0].capitalize() + str(d).zfill(3) + hired)
            mouses.append(inv_heads[5][0].capitalize() + str(d).zfill(3) + hired)
            phones.append(inv_heads[6][0].capitalize() + str(d).zfill(3) + hired)
        
        print(f"{userid}\n{laptop}\n{screen}\n{dockst}\n{keybrd}\n{mouses}\n{phones}\n{hiredt}")


make_inv_list()