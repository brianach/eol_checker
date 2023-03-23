import gspread
import random
import time
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
inv_heads = SHEET.worksheet("hardware").row_values(1)

USERS = 50  # notional number of employees

USER, LAPT, SCRN, DOCK, KEYB, MOUS, PHON, HIRE = ([] for l_i in range(8))
INVENTORY = [USER, LAPT, SCRN, DOCK, KEYB, MOUS, PHON, HIRE]

UMEM, LMEM, SMEM, DMEM, KMEM, MMEM, PMEM, HMEM = ([] for l_i in range(8))
INV_MEM = [UMEM, LMEM, SMEM, DMEM, KMEM, MMEM, PMEM, HMEM]

c_year = 0
id_count = 0


def make_inv_list(year):
    """
    Function to generate inventory of data using random ordered dating
    """
    global id_count

    # SECTION TO GENERATE RANDOM DATES WITHIN CURRENTLY SELECTED c_year
    # ---------------------------------------------------------------
    dthire = []
    for day in range(1, 1+USERS//5):
        rand_days = random.randrange(1, 365)  # create a random number
        # generate a random date
        sdate = datetime(2022, 12, 30) - timedelta((365*(year)+rand_days))
        dthire.append(sdate.strftime("%d%m%Y"))  # add random date
        # the next line of code rearranges and sorts the dates by ddmmyyy
        HIRE = sorted(dthire, key=lambda hird: (hird[2:4], hird[0:2]))

    # SECTION TO GENERATE INITIAL INVENTORY USING THE RANDOM DATES
    # ------------------------------------------------------------
    for dat in HIRE:
        for i_list in INVENTORY[:-1]:
            list_len = len(i_list)
            if list_len >= USERS//5:  # if 1st yr done increment id from last
                id_count = int(i_list[-1][1:4])
                i_list.append(inv_heads[INVENTORY.index(i_list)][0].capitalize \
                    ()+str(id_count + 1).zfill(3)+dat)
            else:
                i_list.append(inv_heads[INVENTORY.index(i_list)][0].capitalize \
                    ()+str(id_count + 1).zfill(3)+dat)                   
        id_count += 1


def generate_change_list():
    """
    This function generates random selection from the original inventory
    based on industry stats on employee and hardware replacements
    """
    global c_year

    for i_list in INVENTORY[:-1]:
        curr_list = INVENTORY.index(i_list)
        rand_change = random.randrange(1, 3)  # select random number

        # SAMPLE FOR THE CURRENT YEAR ONLY USING THE LIST RANGE METHOD
        # ------------------------------------------------------------
        remove_items = random.sample(i_list[c_year * USERS//5 : c_year \
            * USERS//5 + USERS//5], rand_change)
        for r_m in remove_items:
            # add the removal values to a list for checking against the
            # associated inventory list eg: LAPT[] : LMEM[]
            INV_MEM[curr_list].append(r_m)

    c_year += 1


def simulate_changes(year):
    """
    This function takes the generate_change_list() results and removes
    the matching items from the existing lists
    """
    for id_n, s_list_2 in enumerate(INV_MEM[:-1]):

        for i_1, item_2 in enumerate(s_list_2):
            s_list_1 = INVENTORY[id_n]
            for i_2, item_1 in enumerate(s_list_1):
                if item_2 == item_1:
                    pos = i_2
                    comp_string = item_1[-8:]
                    del_date = datetime.strptime(comp_string, "%d%m%Y")
                    year_day = del_date.strftime("%j")
                    rand_days = random.randrange(1, int(year_day))
                    new_date_str = datetime(2022, 12, 30)-timedelta((365*(year)+rand_days))
                    new_date = new_date_str.strftime("%d%m%Y")
                    new_string = item_1[:1]+str(len(s_list_1)+1+i_1).zfill(3)+new_date
                    s_list_1.pop(pos)
                    s_list_1.append(new_string)


def simulate_eol_replacement(year):
    """
    This function checks the type of hardware against an eol factor as follows:
    5(years) for screens, 4(y) for laptops & docks, 3(y) for keyboard
     & mouse and 2(y) for phones starting with the shortest eol factor
    """
    if year > 0:
        if year % 2 == 0:
            print(f"Year {year} is an even year")
        else:
            print(f"Year {year} is an odd year")


def generate_new_inventory():
    """
    This takes the updated lists after all the simulated changes
    and sends it to the google sheets 
    """
    pos = 0  # position of item in list
    with open("data.txt", mode = "a") as file:
        for u in USER:
            g_row = []
            for i_list in INVENTORY[:-1]:
                g_row.append(i_list[pos])  # populate the inventory
            g_row.append(u[-8:])  # add the date field

            pos += 1
            file.write(f"{g_row}\n")
            #print(g_row)  # write to file to test output
            #update_inventory(g_row)


def update_inventory(g_row):
    """
    Function to write data to google spreadsheet
    """
    HARDWARE.append_row(g_row)


def main():
    """
    Run all program functions.
    """
    for year in reversed(range(5)):
        make_inv_list(year)
        generate_change_list()
        simulate_changes(year)
    generate_new_inventory()


main()
