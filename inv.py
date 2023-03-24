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

HARDWARE.batch_clear(["A2:H120"])  # clear the worksheet to run simulation
inv_heads = SHEET.worksheet("hardware").row_values(1)

USERS = 50  # number of employees

USER, LAPT, SCRN, DOCK, KEYB, MOUS, PHON, HIRE = ([] for l_i in range(8))
INVENTORY = [USER, LAPT, SCRN, DOCK, KEYB, MOUS, PHON, HIRE]

UMEM, LMEM, SMEM, DMEM, KMEM, MMEM, PMEM, HMEM = ([] for l_i in range(8))
INV_MEM = [UMEM, LMEM, SMEM, DMEM, KMEM, MMEM, PMEM, HMEM]

curr_year = 0
id_count = 0


def make_inv_list(year):
    """
    Function to generate inventory of data using random ordered dating
    """
    global id_count

    # SECTION TO GENERATE RANDOM DATES WITHIN CURRENT SELECTED YEAR
    # -------------------------------------------------------------
    date_hire = []
    for day in range(1, 1+USERS//5):
        rand_days = random.randrange(1, 365)
        sdate = datetime(2022, 12, 30) - timedelta((365*(year)+rand_days))
        date_hire.append(sdate.strftime("%d%m%Y"))
        HIRE = sorted(date_hire, key=lambda hird: (hird[2:4], hird[0:2]))

    # SECTION TO GENERATE INITIAL INVENTORY USING RANDOM DATES
    # --------------------------------------------------------
    for dat in HIRE:
        for inv_list in INVENTORY[:-1]:
            list_len = len(inv_list)
            if list_len >= USERS//5:  # if 1st yr done increment id from last id
                id_count = int(inv_list[-1][1:4])
                inv_list.append(inv_heads[INVENTORY.index(inv_list)][0].capitalize \
                    ()+str(id_count + 1).zfill(3)+dat)
            else:
                inv_list.append(inv_heads[INVENTORY.index(inv_list)][0].capitalize \
                    ()+str(id_count + 1).zfill(3)+dat)                   
        id_count += 1


def generate_change_list():
    """
    This function generates random selection from the original inventory
    based on industry stats on employee and hardware replacements
    """
    global curr_year

    for inv_list in INVENTORY[:-1]:
        curr_list = INVENTORY.index(inv_list)
        rand_change = random.randrange(1, 3)  # select random number

        # SAMPLE FOR THE CURRENT YEAR ONLY USING THE LIST RANGE
        # -----------------------------------------------------
        remove_items = random.sample(inv_list[curr_year * USERS//5 : curr_year \
            * USERS//5 + USERS//5], rand_change)
        for r_m in remove_items:
            INV_MEM[curr_list].append(r_m)

    curr_year += 1


def simulate_changes(year):
    """
    This function takes the generate_change_list() results and 
    removes any matching items in that list from the old lists
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
    Each hardware type has an eol value. When this is reached the 
    hardware is replaced'
    """
    eol_time = int(datetime.now().strftime("%y"))
    hw_type = []
    if curr_year > 1:
        if curr_year % 2 == 1:
            hw_type.clear()
            hw_type.append("phones")
            hw_purch_yr = eol_time - (year + 3)
            replace_eol_hardware(hw_type, hw_purch_yr, year)

        if curr_year % 3 == 1:
            hw_type.clear()
            hw_type.extend(["keybrd", "mouses"])
            hw_purch_yr = eol_time - (year + 4)
            replace_eol_hardware(hw_type, hw_purch_yr, year)

        if curr_year % 4 == 1:
            hw_type.clear()
            hw_type.extend(["laptop", "dockst"])
            hw_purch_yr = eol_time - (year + 5)
            replace_eol_hardware(hw_type, hw_purch_yr, year)
           
        if curr_year % 5 == 0:
            hw_type.clear()
            hw_type.extend(["screen"])
            hw_purch_yr = eol_time - (year + 6)
            replace_eol_hardware(hw_type, hw_purch_yr, year)


def generate_new_inventory():
    """
    This takes the updated lists after all the simulated changes
    and sends it to the google sheets 
    """
    pos = 0  # position of item in list
    with open("data.txt", mode = "a") as file:
        for u in USER:
            g_row = []
            for inv_list in INVENTORY[:-1]:
                g_row.append(inv_list[pos])  # populate the inventory
            g_row.append(u[-8:])  # add the date field

            pos += 1
            file.write(f"{g_row}\n")
            #print(g_row)  # write to file to test output
            #update_inventory(g_row)


def replace_eol_hardware(hw_type, hw_purch_yr, year):
    """
    This function replaces the eol hardware items
    """
    print(f"replace {hw_type}")

    eol_matches = [hw_item for hw_item in inv_heads if hw_item in hw_type]

    for match in eol_matches:
        inv_list_index = inv_heads.index(match)
        hw_list = INVENTORY[inv_list_index]
        for list_item in hw_list:
            if int(list_item[-2:]) == hw_purch_yr:
                get_hw_date = list_item[-8:]
                old_date = datetime.strptime(get_hw_date, "%d%m%Y")
                delta = datetime.today() - old_date
                if delta.days > year * 365:
                    print(f"{list_item} purchased over {curr_year -1 } year's ago")
    #print(eol_matches)


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
        simulate_eol_replacement(year)
    generate_new_inventory()


main()
