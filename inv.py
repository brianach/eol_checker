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

    for y_r in range(0, -1, -1):

        dh, usr, lap, scr, dok, key, mou, phn, hir = ([] for l_i in range(9))

        for d in range(1, 1+USERS//5):
            rand_days = random.randrange(1, 365)
            sdate = datetime(2022, 12, 30) - timedelta((365*(y_r)+rand_days))
            dh.append(sdate.strftime("%d%m%Y"))
            hir = sorted(dh, key=lambda hird: (hird[2:4], hird[0:2]))
        p = 0

        for h in hir:   
            g_row = []

            usr.append(inv_heads[0][0].capitalize()+str(p).zfill(3)+h)
            lap.append(inv_heads[1][0].capitalize()+str(p).zfill(3)+h)
            scr.append(inv_heads[2][0].capitalize()+str(p).zfill(3)+h)
            dok.append(inv_heads[3][0].capitalize()+str(p).zfill(3)+h)
            key.append(inv_heads[4][0].capitalize()+str(p).zfill(3)+h)
            mou.append(inv_heads[5][0].capitalize()+str(p).zfill(3)+h)
            phn.append(inv_heads[6][0].capitalize()+str(p).zfill(3)+h)

            g_row = usr[p], lap[p], scr[p], dok[p], key[p], mou[p], phn[p], hir[p]
            update_inventory(g_row)
            p += 1

        print(f"{usr}\n{lap}\n{scr}\n{dok}\n{key}\n{mou}\n{phn}\n{hir}")  # test output to console


def update_inventory(g_row):
    """
    Function to add data to google spreadsheet
    """
    inventory_worksheet = SHEET.worksheet("hardware")

    inventory_worksheet.append_row(g_row)


make_inv_list()
