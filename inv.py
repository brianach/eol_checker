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
USERS = 50  # notional number of employees
inventory = []


def make_inv_list():
    """
    Function to generate inventory of data entered using random ordered dating
    """

    for y_r in range(4, -1, -1):

        dhr, usr, lap, scrn, dok, key, mou, phn, hir = ([] for l_i in range(9))

        for d_n in range(1, 1+USERS//5):
            rand_days = random.randrange(1, 365)
            sdate = datetime(2022, 12, 30) - timedelta((365*(y_r)+rand_days))
            dhr.append(sdate.strftime("%d%m%Y"))
            hir = sorted(dhr, key=lambda hird: (hird[2:4], hird[0:2]))
        d_n = 0

        for hird in hir:

            d_n += 1
            usr.append(inv_heads[0][0].capitalize()+str(d_n).zfill(3)+hird)
            lap.append(inv_heads[1][0].capitalize()+str(d_n).zfill(3)+hird)
            scrn.append(inv_heads[2][0].capitalize()+str(d_n).zfill(3)+hird)
            dok.append(inv_heads[3][0].capitalize()+str(d_n).zfill(3)+hird)
            key.append(inv_heads[4][0].capitalize()+str(d_n).zfill(3)+hird)
            mou.append(inv_heads[5][0].capitalize()+str(d_n).zfill(3)+hird)
            phn.append(inv_heads[6][0].capitalize()+str(d_n).zfill(3)+hird)

        print(f"{usr}\n{lap}\n{scrn}\n{dok}")
        print(f"{key}\n{mou}\n{phn}\n{hir}")


make_inv_list()
