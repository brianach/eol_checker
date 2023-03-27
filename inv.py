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

USERS = 50  # both this and the company age could be done by input but due
            # to google sheets limits i've capped at 50 and 5 years

USER, LAPT, SCRN, DOCK, KEYB, MOUS, PHON, HIRE = ([] for l_i in range(8))
INVENTORY = [USER, LAPT, SCRN, DOCK, KEYB, MOUS, PHON, HIRE]

UMEM, LMEM, SMEM, DMEM, KMEM, MMEM, PMEM, HMEM = ([] for l_i in range(8))
INV_MEM = [UMEM, LMEM, SMEM, DMEM, KMEM, MMEM, PMEM, HMEM]

EOL_VALUE = {
    "screen": 5,
    "laptop": 4,
    "dockst": 4,
    "keybrd": 3,
    "mouses": 3,
    "phones": 2
    }

start_year = 0
curr_year = 18
id_count = 0


def generate_dates(year):
    """
    Function to generate inventory of data using random ordered dating
    """
    date_hire = []
    for day in range(1, 1+USERS//5):
        rand_days = random.randrange(1, 365)
        sdate = datetime(2022, 12, 30) - timedelta((365*(year)+rand_days))
        date_hire.append(sdate.strftime("%d%m%Y"))
        hire_date = sorted(date_hire, key=lambda hird: (hird[2:4], hird[0:2]))
    generate_inventory(hire_date)


def generate_inventory(hire_date):
    """
    Function to generate the initial inventory
    """
    global id_count
    for h_date in hire_date:
        for hw_list in INVENTORY[:-1]:
            list_len = len(hw_list)
            if list_len >= USERS//5:  # if the first year  inventory is initiated
                id_count = int(hw_list[-1][1:4])   # increment the hw id from last item
                hw_list.append(inv_heads[INVENTORY.index(hw_list)][0].capitalize \
                    ()+str(id_count + 1).zfill(3)+h_date)
            else:
                hw_list.append(inv_heads[INVENTORY.index(hw_list)][0].capitalize \
                    ()+str(id_count + 1).zfill(3)+h_date)                   
        id_count += 1


def generate_churn_list():
    """
    This function generates selections from the initial inventory
    based on a random value not greater than 20% to simulate wear
    and tear, hardware failures and average employee churn rate
    """
    global start_year

    for hw_list in INVENTORY[:-1]:
        curr_list_id = INVENTORY.index(hw_list)
        rand_change = random.randrange(1, 3)

        remove_items = random.sample(hw_list[start_year * USERS// \
            5 : start_year * USERS//5 + USERS//5], rand_change)
        for r_m in remove_items:
            INV_MEM[curr_list_id].append(r_m)

    start_year += 1


def simulate_churn(year):
    """
    This function takes the generate_churn_list() results and
    removes any matching items in that list from the old lists
    then replacement items are appended to the old list
    """
    for index_n, s_list_2 in enumerate(INV_MEM[:-1]):

        for index_1, item_2 in enumerate(s_list_2):
            s_list_1 = INVENTORY[index_n]
            for index_2, item_1 in enumerate(s_list_1):
                if item_2 == item_1:
                    pos = index_2
                    comp_string = item_1[-8:]
                    del_date = datetime.strptime(comp_string, "%d%m%Y")

                    year_day = del_date.strftime("%j")
                    rand_days = random.randrange(1, int(year_day) + 1 )
                    new_date_str = datetime(2022, 12, 30)-timedelta((365*(year)+rand_days))
                    new_date = new_date_str.strftime("%d%m%Y")
                    new_string = item_1[:1]+str(len(s_list_1)+1+index_1).zfill(3)+new_date
                    s_list_1.pop(pos)
                    s_list_1.append(new_string)


def simulate_eol_replacement(year):
    """
    Each hardware type has an eol value. When this is reached the
    hardware should be replaced. This function checks the hardware
    against its eol value and initiates the replacement function
    """
    #eol_time = int(datetime.now().strftime("%y"))
    hw_type = []
    if start_year > 1:  # eol check (2 years)

        for hw_list in INVENTORY[1:-1]:
            curr_list_id = INVENTORY.index(hw_list)
            hw_type = inv_heads[curr_list_id]
            hw_item = hw_list[0]  # get the hw list
            check_val = curr_year - int(hw_item[-2:])
            for key, eol_value in EOL_VALUE.items():
                if key == hw_type and check_val == eol_value:
                    remove_eol_hardware(hw_type, eol_value, year)


def generate_new_inventory():
    """
    This takes the updated lists after all the simulated changes
    and sends it to the google sheets 
    """
    pos = 0  # position of item in list
    for u in USER:
        g_row = []
        for hw_list in INVENTORY[:-1]:
            g_row.append(hw_list[pos])  # populate the inventory
        g_row.append(u[-8:])  # add the date field
        pos += 1
        update_inventory(g_row)


def remove_eol_hardware(hw_type, eol_value, year):
    """
    This function replaces the eol hardware items
    """
    #print(f"replace {hw_type}")

    inv_list_index = inv_heads.index(hw_type)
    hw_list = INVENTORY[inv_list_index]
    eol_year = int(hw_list[-1][-2:]) - eol_value
    for i in range(USERS//5):
        list_item = hw_list[0]
        if int(list_item[-2:]) == eol_year:
            get_hw_date = list_item[-8:]
            old_date = datetime.strptime(get_hw_date, "%d%m%Y")
            delta = datetime.today() - old_date
            if delta.days > eol_value * 365:
                print(f"{list_item} purchased over {start_year} year's ago")
                hw_list.pop(0)
                replace_eol_hardware(hw_list, eol_value, year)


def replace_eol_hardware(hw_list, eol_value, year):
    """
    This function replaces the removed eol hardware with new
    """
    rand_days = random.randrange(1, 365)
    eol_time = int(datetime.now().strftime("%y")) - (year+1)
    new_date_str = datetime(2022, 12, 30)-timedelta((365*(eol_value)+rand_days))
    new_date = new_date_str.strftime("%d%m%Y")
    new_date = new_date[:-2] + str(eol_time)
    id_count = int(hw_list[-1][1:4])  # increment the hw id from last item
    hw_list.append(inv_heads[INVENTORY.index(hw_list)][0].capitalize \
        ()+str(id_count + 1).zfill(3)+new_date)


def update_inventory(g_row):
    """
    Function to write data to google spreadsheet
    """
    HARDWARE.append_row(g_row)


def main():
    """
    Run all program functions.
    """
    global curr_year
    for year in reversed(range(5)):
        generate_dates(year)
        simulate_eol_replacement(year)        
        generate_churn_list()
        simulate_churn(year)
        curr_year += 1
    generate_new_inventory()


main()
