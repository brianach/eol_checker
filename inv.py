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

USER, LAPT, SCRN, DOCK, KEYB, MOUS, PHON, HIRE = ([] for l_i in range(8))  
INVENTORY = [USER, LAPT, SCRN, DOCK, KEYB, MOUS, PHON, HIRE]

UMEM, LMEM, SMEM, DMEM, KMEM, MMEM, PMEM, HMEM = ([] for l_i in range(8))
INV_MEM = [UMEM, LMEM, SMEM, DMEM, KMEM, MMEM, PMEM, HMEM]

def make_inv_list():
    """
    Function to generate inventory of data entered using random ordered dating
    """

    for year in range(0, -1, -1):

        dthire = []

        for day in range(1, 1+USERS//5):
            rand_days = random.randrange(1, 365)  # create a random number 
            sdate = datetime(2022, 12, 30) - timedelta((365*(year)+rand_days))  # generate a random date
            dthire.append(sdate.strftime("%d%m%Y"))  # add random date to dthire list
            HIRE = sorted(dthire, key=lambda hird: (hird[2:4], hird[0:2])) 

        pos = 0  # position of item in list

        for dat in HIRE:
            i_list = 0
            g_row = []
            for i_list in range(len(INVENTORY)-1):
                INVENTORY[i_list].append(inv_heads[i_list][0].capitalize()+str(pos).zfill(3)+dat)
                g_row.append(INVENTORY[i_list][pos])  # populate the inventory 
            g_row.append(dat)  # add the date field
            update_inventory(g_row)
            pos += 1

        count = 0
        for count in range(len(INVENTORY)-1):
            rand_change = random.randrange(1, 3)  # select random elements < 3 from list
            remove_items =  random.sample(INVENTORY[count], rand_change)
            INV_MEM[count].append(remove_items)  # add the removal values to a list 
            INVENTORY[count] = [ r for r in INVENTORY[count] if r not in remove_items]  
            print(INVENTORY[count])


def update_inventory(g_row):
    """
    Function to add data to google spreadsheet
    """
    inventory_worksheet = SHEET.worksheet("hardware")

    inventory_worksheet.append_row(g_row)


make_inv_list()
