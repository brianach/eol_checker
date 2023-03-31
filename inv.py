"""
a simple demo to simulate the creation of a company hardware inventory with
options to replace hardware which has reached an EOL (end of life) cycle
"""

import os
from readchar import readkey, key
import random
from datetime import timedelta, datetime
import gspread
from google.oauth2.service_account import Credentials


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

USERS = 50  # both USERS and YEARS could be done by user input but
YEARS = 5  # due to google sheets limits I've capped at 50 and 5

SCRN, LAPT, DOCK, KEYB, MOUS, PHON, DATE = ([] for l_i in range(7))
INVENTORY = [SCRN, LAPT, DOCK, KEYB, MOUS, PHON, DATE]

SMEM, LMEM, DMEM, KMEM, MMEM, PMEM, DTMM = ([] for l_i in range(7))
INV_MEM = [SMEM, LMEM, DMEM, KMEM, MMEM, PMEM, DTMM]

SEOL, LEOL, DEOL, KEOL, MEOL, PEOL = ([] for l_i in range(6))
INV_EOL = [SEOL, LEOL, DEOL, KEOL, MEOL, PEOL]

EOL_VALUE = {
    "screen": 5,
    "laptop": 4,
    "dockst": 4,
    "keybrd": 3,
    "mouses": 3,
    "phones": 2
    }

TOT_EOL = 0
START_YR = 0
CURR_YR = 18  # this is the start year for ACME coders
ID_COUNT = 0
TOT_LINE = 60  # total available lines for the terminal


def generate_dates(year):
    """
    Function to generate inventory of data using random ordered dating
    """
    date_start = []
    for _i in range(1, 1 + USERS // YEARS):
        rand_days = random.randrange(1, 365)
        sdate = datetime(2022, 12, 30) - timedelta((365*(year)+rand_days))
        date_start.append(sdate.strftime("%d%m%Y"))
        start_date = sorted(date_start, key=lambda start_d:
                            (start_d[2:4], start_d[0:2]))
    generate_inventory(start_date)


def generate_inventory(start_date):
    """
    Function to generate the initial inventory
    """
    global ID_COUNT
    for s_date in start_date:
        for hw_list in INVENTORY[:-1]:
            list_len = len(hw_list)
            if list_len >= USERS // YEARS:  # if year one completed
                ID_COUNT = int(hw_list[-1][1:4])  # increment id from last
                hw_list.append(inv_heads[INVENTORY.index(hw_list)][0].
                               capitalize()+str(ID_COUNT + 1).zfill(3)+s_date)
            else:
                hw_list.append(inv_heads[INVENTORY.index(hw_list)][0].
                               capitalize()+str(ID_COUNT + 1).zfill(3)+s_date)
        ID_COUNT += 1
        INVENTORY[len(INVENTORY)-1].append(s_date)


def generate_churn_list():
    """
    This function generates selections from the initial inventory
    based on a random value not greater than 20% to simulate wear
    and tear, hardware failures and average employee churn rate
    """
    global START_YR

    for hw_list in INVENTORY[:-1]:
        curr_list_id = INVENTORY.index(hw_list)
        rand_change = random.randrange(1, 3)

        remove_items = random.sample(hw_list[START_YR * USERS //
                                             YEARS: START_YR * USERS // 5 +
                                             USERS // YEARS], rand_change)
        for r_m in remove_items:
            INV_MEM[curr_list_id].append(r_m)

    START_YR += 1


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
                    rand_days = random.randrange(1, int(year_day) + 1)
                    new_date_str = datetime(2022, 12, 30)-timedelta(
                            (365*(year) + rand_days))
                    new_date = new_date_str.strftime("%d%m%Y")
                    new_string = item_1[:1]+str(len(s_list_1) + 1 +
                                                index_1).zfill(3)+new_date
                    s_list_1.pop(pos)
                    s_list_1.append(new_string)


def simulate_eol_replacement(year):
    """
    Each hardware type has an eol value. When this is reached the
    hardware should be replaced. This function checks the hardware
    against its eol value and initiates the replacement function
    """
    hw_type = []
    if START_YR > 1:  # eol check (2 years)

        for hw_list in INVENTORY[1:-1]:
            curr_list_id = INVENTORY.index(hw_list)
            hw_type = inv_heads[curr_list_id]
            hw_item = hw_list[0]
            check_val = CURR_YR - int(hw_item[-2:])
            for key, eol_value in EOL_VALUE.items():
                if key == hw_type and check_val == eol_value:
                    remove_eol_hardware(hw_type, eol_value, year)


def remove_eol_hardware(hw_type, eol_value, year):
    """
    This function replaces the eol hardware items
    """
    inv_list_index = inv_heads.index(hw_type)
    hw_list = INVENTORY[inv_list_index]
    eol_year = int(hw_list[-1][-2:]) - eol_value
    for _i in range(USERS // YEARS):
        list_item = hw_list[0]
        if int(list_item[-2:]) == eol_year:
            get_hw_date = list_item[-8:]
            old_date = datetime.strptime(get_hw_date, "%d%m%Y")
            delta = datetime.today() - old_date
            if delta.days > eol_value * 365:
                hw_list.pop(0)
                replace_eol_hardware(hw_list, eol_value, year)


def replace_eol_hardware(hw_list, eol_value, year):
    """
    This function replaces the removed eol hardware with new
    """
    rand_days = random.randrange(1, 365)
    eol_time = int(datetime.now().strftime("%y")) - (year+1)
    new_d_str = datetime(2022, 12, 30)-timedelta((365*(eol_value)+rand_days))
    new_date = new_d_str.strftime("%d%m%Y")
    new_date = new_date[:-2] + str(eol_time)
    ID_COUNT = int(hw_list[-1][1:4])  # increment the hw id from last item
    hw_list.append(inv_heads[INVENTORY.index(hw_list)][0].capitalize()
                   + str(ID_COUNT + 1).zfill(3)+new_date)


def generate_new_inventory():
    """
    This takes the updated lists after all the simulated changes
    and sends it to the google sheets
    """

    pos = 0  # position of item in list
    for _d in DATE:
        g_row = []
        for hw_list in INVENTORY[:-1]:
            g_row.append(hw_list[pos])  # populate the inventory
        g_row.append(_d[-8:])  # add the date field
        pos += 1
        update_inventory(g_row)


def update_inventory(g_row):
    """
    Function to write data to google spreadsheet
    """
    # HARDWARE.append_row(g_row)

    with open("data.txt", mode="a") as file:
        file.write(f"{g_row}\n")
    return g_row


def get_eol_hardware():
    """
    Get the total value for all EOL hardware
    """
    hw_type = []
    global TOT_EOL
    for hw_list, hw_eol_list in zip(INVENTORY[:-1], INV_EOL):
        curr_list_id = INVENTORY.index(hw_list)
        hw_type = inv_heads[curr_list_id]
        hw_item = hw_list[0]
        check_val = CURR_YR - int(hw_item[-2:])
        for hw_item in hw_list:
            for key, eol_value in EOL_VALUE.items():
                if key == hw_type and check_val == eol_value:
                    then = datetime.strptime(hw_item[-8:], "%d%m%Y")
                    if (datetime.now() - then) >= timedelta(365*eol_value):
                        TOT_EOL += 1
                        # print(hw_type, hw_item[-8:], "Total EOL", TOT_EOL)
                        INV_EOL[curr_list_id].append(hw_item)
                    break


def print_header():
    """
    Print terminal header text to screen
    """

    prt = ''.join('\x1b[4;32;40m' + ' ' + '\x1b[0m' for i in range(120))
    print(prt)
    prt = ''.join('\x1b[1;32;40m' + ' ' + '\x1b[0m' for i in range(120))
    print(prt)

    co_title = "ACME  Coders"
    app_name = "HARDWARE INVENTORY"
    line_sps = int((120 - (len(co_title) + len(app_name))) / 3)

    prt = ''.join('\x1b[1;32;40m' + ' ' + '\x1b[0m' for i in range(line_sps))
    print(prt, end='')
    t_line = ''.join('\x1b[4;32;40m' + co_title + '\x1b[0m')
    print(t_line, end='')
    prt = ''.join('\x1b[1;32;40m' + ' ' + '\x1b[0m' for i in range(line_sps))
    print(prt, end='')
    t_line = ''.join('\x1b[4;32;40m' + app_name + '\x1b[0m')
    print(t_line, end='')
    prt = ''.join('\x1b[1;32;40m' + ' ' + '\x1b[0m' for i in range(line_sps))
    print(prt)

    prt = ''.join('\x1b[4;32;40m' + ' ' + '\x1b[0m' for i in range(120))
    print(prt)
    prt = ''.join('\x1b[1;32;40m' + ' ' + '\x1b[0m' for i in range(120))
    print(prt)

    usr_object = "User Account......: "
    usr_locale = "User Context......: "
    usr_obj_name = " Administrator "
    usr_loc_name = " Inventory EOL "
    date_string = "Current Date...: "
    eoli_string = "Total EOL HW...: "
    current_date = " " + datetime.now().strftime("%x") + " "
    current_eoli = "    " + str(TOT_EOL).zfill(2) + "    "

    line_sps = int((120 - (len(usr_object) + len(usr_obj_name)
                    + len(date_string) + len(current_date))) / 3)

    prt = ''.join('\x1b[1;32;40m' + ' ' + '\x1b[0m' for i in range(line_sps-5))
    print(prt, end='')
    t_line = ''.join('\x1b[4;32;40m' + usr_object + '\x1b[0m')
    print(t_line, end='')
    t_line = ''.join('\x1b[0;30;47m' + usr_obj_name + '\x1b[0m')
    print(t_line, end='')
    prt = ''.join('\x1b[1;32;40m' + ' ' + '\x1b[0m' for i in range(line_sps+1))
    print(prt, end='')
    t_line = ''.join('\x1b[4;32;40m' + date_string + '\x1b[0m')
    print(t_line, end='')
    t_line = ''.join('\x1b[0;30;47m' + current_date + '\x1b[0m')
    print(t_line, end='')
    prt = ''.join('\x1b[1;32;40m' + ' ' + '\x1b[0m' for i in range(line_sps+5))
    print(prt)
    prt = ''.join('\x1b[1;32;40m' + ' ' + '\x1b[0m' for i in range(line_sps-5))
    print(prt, end='')
    t_line = ''.join('\x1b[4;32;40m' + usr_locale + '\x1b[0m')
    print(t_line, end='')
    t_line = ''.join('\x1b[0;30;47m' + usr_loc_name + '\x1b[0m')
    print(t_line, end='')
    prt = ''.join('\x1b[1;32;40m' + ' ' + '\x1b[0m' for i in range(line_sps+1))
    print(prt, end='')
    t_line = ''.join('\x1b[4;32;40m' + eoli_string + '\x1b[0m')
    print(t_line, end='')
    t_line = ''.join('\x1b[0;30;47m' + current_eoli + '\x1b[0m')
    print(t_line, end='')
    prt = ''.join('\x1b[1;32;40m' + ' ' + '\x1b[0m' for i in range(line_sps+5))
    print(prt)

    prt = ''.join('\x1b[1;32;40m' + ' ' + '\x1b[0m' for i in range(120))
    print(prt)
    prt = ''.join('\x1b[4;32;40m' + ' ' + '\x1b[0m' for i in range(120))
    print(prt)
    prt = ''.join('\x1b[1;32;40m' + ' ' + '\x1b[0m' for i in range(120))
    print(prt)


def print_main_menu():
    """
    Display main menu
    """
    sel_choices_ = "Select one of the options presented below by pressing the\
 number indicated"
    sel_choice_1 = " 1 : Display Inventory  "
    sel_choice_2 = " 2 : Display EOL Items  "
    sel_choice_3 = " 3 : Exit EOL Inventory "

    choices_len = len(sel_choices_)
    line_sps = int((120 - choices_len) / 2)

    prt = ''.join('\x1b[1;32;40m' + ' ' + '\x1b[0m' for i in range(line_sps))
    print(prt, end='')
    prt = ''.join('\x1b[1;32;40m' + sel_choices_ + '\x1b[0m')
    print(prt, end='')
    prt = ''.join('\x1b[1;32;40m' + ' ' + '\x1b[0m' for i in range(line_sps))
    print(prt)
    prt = ''.join('\x1b[1;32;40m' + ' ' + '\x1b[0m' for i in range(120))
    print(prt)
    prt = ''.join('\x1b[1;32;40m' + ' ' + '\x1b[0m' for i in range(12))
    print(prt, end='')
    t_line = ''.join('\x1b[4;32;40m' + sel_choice_1 + '\x1b[0m')
    print(t_line, end='')
    prt = ''.join('\x1b[1;32;40m' + ' ' + '\x1b[0m' for i in range(12))
    print(prt, end='')
    t_line = ''.join('\x1b[4;32;40m' + sel_choice_2 + '\x1b[0m')
    print(t_line, end='')
    prt = ''.join('\x1b[1;32;40m' + ' ' + '\x1b[0m' for i in range(12))
    print(prt, end='')
    t_line = ''.join('\x1b[4;32;40m' + sel_choice_3 + '\x1b[0m')
    print(t_line, end='')
    prt = ''.join('\x1b[1;32;40m' + ' ' + '\x1b[0m' for i in range(12))
    print(prt)
    prt = ''.join('\x1b[1;32;40m' + ' ' + '\x1b[0m' for i in range(120))
    print(prt)
    prt = ''.join('\x1b[4;32;40m' + ' ' + '\x1b[0m' for i in range(120))
    print(prt)


def print_inventory_menu():
    """
    Menu which appears when display inventory is selected
    """
    sel_choices_ = "  Use the up and down arrows to navigate inventory  "
    sel_choice_4 = " 4 : Display EOL Items  "
    sel_choice_5 = " 5 : Exit Inventory "

    choices_len = len(sel_choices_)
    line_sps = int((120 - choices_len) / 2)

    prt = ''.join('\x1b[1;32;40m' + ' ' + '\x1b[0m' for i in range(line_sps))
    print(prt, end='')
    prt = ''.join('\x1b[1;32;40m' + sel_choices_ + '\x1b[0m')
    print(prt, end='')
    prt = ''.join('\x1b[1;32;40m' + ' ' + '\x1b[0m' for i in range(line_sps))
    print(prt)
    prt = ''.join('\x1b[1;32;40m' + ' ' + '\x1b[0m' for i in range(120))
    print(prt)

    prt = ''.join('\x1b[1;32;40m' + ' ' + '\x1b[0m' for i in range(20))
    print(prt, end='')
    t_line = ''.join('\x1b[4;32;40m' + sel_choice_4 + '\x1b[0m')
    print(t_line, end='')
    prt = ''.join('\x1b[1;32;40m' + ' ' + '\x1b[0m' for i in range(36))
    print(prt, end='')
    t_line = ''.join('\x1b[4;32;40m' + sel_choice_5 + '\x1b[0m')
    print(t_line, end='')
    prt = ''.join('\x1b[1;32;40m' + ' ' + '\x1b[0m' for i in range(20))
    print(prt)

    prt = ''.join('\x1b[4;32;40m' + ' ' + '\x1b[0m' for i in range(120))
    print(prt)

    my_list = ['Screen', 'Laptop', 'Dock Stn', 'Keyboard', 'Mouse', 'Phone']
    num_items = len(my_list)
    width = 120

    item_width = int(width / num_items)

    format_str = "{:^" + str(item_width) + "}"

    output_str = "".join([format_str.format(item) for item in my_list])
    headings = ''.join('\x1b[4;32;40m' + output_str + '\x1b[0m')

    print(headings)

    prt = ''.join('\x1b[1;32;40m' + ' ' + '\x1b[0m' for i in range(120))
    print(prt)


def print_footer():
    """
    This prints out the bottom lines on the screen
    """
    app_n_str = "  EOL Inventory Checker  "
    app_v_str = "  CI-PP330  Version 1.0  "
    line_sps = 120 - (len(app_n_str) + len(app_v_str))

    prt = ''.join('\x1b[4;32;40m' + ' ' + '\x1b[0m' for i in range(120))
    print(prt)
    t_line = ''.join('\x1b[1;32;40m' + app_n_str + '\x1b[0m')
    print(t_line, end='')
    prt = ''.join('\x1b[1;32;40m' + ' ' + '\x1b[0m' for i in range(line_sps))
    print(prt, end='')
    t_line = ''.join('\x1b[1;32;40m' + app_v_str + '\x1b[0m')
    print(t_line)


def get_user_interaction():
    """
    This fucntion offers the user the ability to display information
    and interact with the terminal
    """
    print_header()
    print_main_menu()
    for _l in range(20):
        prt = ''.join('\x1b[1;32;40m' + ' ' + '\x1b[0m' for i in range(120))
        print(prt)
    print_footer()

    while True:
        _k = readkey()
        if _k == "1":
            display_inventory()
        if _k == "2":
            print("Wahoo too")
        if _k == "3":
            break


def inventory_input():
    """
    This checks for input from user while in the inventory display screen
    """
    i_row = [list(sublist) for sublist in zip(*INVENTORY[:-1])]

    direction = 0
    display_inventory(direction, i_row)

    while True:
        _k = readkey()

        if _k == key.DOWN:
            direction += 20
            display_inventory(direction, i_row)

        if _k == key.UP:
            direction -= 20
            display_inventory(direction, i_row)

        if _k == "3":
            break


def display_inventory(direction, i_row):
    """
    Display the contents of the hardware inventory 20 rows a time 
    """
    os.system('clear')
    print_header()
    print_inventory_menu()

    for i in range(direction, direction + 20):
        if i > len(i_row) - 1:
            for i in range(10):  # there are 10 available lines left on screen
                prt = ''.join('\x1b[1;32;40m' + ' ' + '\x1b[0m' for i in range(120))
                print(prt)
            direction = 0 
            break
        elif direction < 0:
            direction = 0
            break
        else:
            print('\x1b[1;32;40m' + '      ', '       '.join('\x1b[1;32;40m' + str(i)for i in i_row[i]) + '      ' + '\x1b[0m')
    print_footer()


def main():
    """
    Run all program functions.
    """
    global CURR_YR
    for year in reversed(range(5)):
        generate_dates(year)
        generate_churn_list()
        simulate_churn(year)
        simulate_eol_replacement(year)
        CURR_YR += 1
    get_eol_hardware()
    generate_new_inventory()
    #get_user_interaction()
    inventory_input()


main()
