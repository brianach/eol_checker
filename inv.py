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
HARDWARE = SHEET.worksheet("hardware")

HARDWARE.batch_clear(["A2:H60"])  # clear the worksheet to run simulation
inv_heads = SHEET.worksheet("hardware").row_values(1)

USERS = 50  # notional number of employees


def make_inv_list():
    """
    Function to generate inventory of data entered using random ordered dating
    """

    for year in range(0, -1, -1):

        userid, laptop, screen, dockst, keybrd, mouses, phones, \
            hiredt = ([] for l_i in range(8))  # initialize lists for each variable
        inventory = [userid, laptop, screen, dockst, keybrd, \
            mouses, phones, hiredt]
        dthire = []

        for day in range(1, 1+USERS//5):
            rand_days = random.randrange(1, 365)  # create a random number from the days in a year
            sdate = datetime(2022, 12, 30) - timedelta((365*(year)+rand_days))  # generate a random date
            dthire.append(sdate.strftime("%d%m%Y"))  # add the random date to the dthire list
            hiredt = sorted(dthire, key=lambda hird: (hird[2:4], hird[0:2]))  # oder the dthire list and copy to hiredt

        pos = 0  # position of item in list

        for dat in hiredt:
            g_row = []

            userid.append(inv_heads[0][0].capitalize()+str(pos).zfill(3)+dat)
            laptop.append(inv_heads[1][0].capitalize()+str(pos).zfill(3)+dat)
            screen.append(inv_heads[2][0].capitalize()+str(pos).zfill(3)+dat)
            dockst.append(inv_heads[3][0].capitalize()+str(pos).zfill(3)+dat)
            keybrd.append(inv_heads[4][0].capitalize()+str(pos).zfill(3)+dat)
            mouses.append(inv_heads[5][0].capitalize()+str(pos).zfill(3)+dat)
            phones.append(inv_heads[6][0].capitalize()+str(pos).zfill(3)+dat)
        
            g_row = userid[pos], laptop[pos], screen[pos], dockst[pos], \
                keybrd[pos], mouses[pos], phones[pos], hiredt[pos]
            update_inventory(g_row)
            pos += 1

        #print(f"{userid}\n{laptop}\n{screen}\n{dockst}\n{keybrd}\n{mouses}\n{phones}\n{hiredt}")  # test output to console
        count = 0
        for count in range(len(inventory)-1):
            rand_change = random.randrange(1, 3)  # select random 20% of elements from list
            print(f"Count is : {count} {random.sample(inventory[count], rand_change)}")


def update_inventory(g_row):
    """
    Function to add data to google spreadsheet
    """
    inventory_worksheet = SHEET.worksheet("hardware")

    inventory_worksheet.append_row(g_row)


make_inv_list()
