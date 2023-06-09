"""
a simple demo to simulate the creation of a company hardware inventory with
options to replace hardware which has reached an EOL (end of life) cycle
"""

import os
import random
from datetime import timedelta, datetime, date
from readchar import readkey, key
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("ci-project-3")
HARDWARE = SHEET.worksheet("hardware")

HARDWARE.batch_clear(["A2:E51"])  # clear the worksheet to run simulation
inv_heads = SHEET.worksheet("hardware").row_values(1)

USERS = 50  # both USERS and YEARS could be done by user input but
YEARS = 5  # due to google sheets limits I've capped at 50 and 5

SCRN, LAPT, KEYB, MOUS, DATE = ([] for l_i in range(5))
INVENTORY = [SCRN, LAPT, KEYB, MOUS, DATE]

SMEM, LMEM, KMEM, MMEM, DMEM = ([] for l_i in range(5))
INV_MEM = [SMEM, LMEM, KMEM, MMEM, DMEM]

SEOL, LEOL, KEOL, MEOL = ([] for l_i in range(4))
INV_EOL = [SEOL, LEOL, KEOL, MEOL]

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


def initialize_display():
    """
    Set up display while innventory is simulated
    """
    print_header()

    sel_choices_ = "Please wait while the hardware inventory loads"
    choices_len = len(sel_choices_)
    spaces = int((78 - choices_len) / 2) * ' '

    print('\x1b[1;32;40m' + spaces + '\x1b[0m', end='')
    print('\x1b[1;32;40m' + sel_choices_ + '\x1b[0m', end='')
    print('\x1b[1;32;40m' + spaces + '\x1b[0m')

    print_blank_line()
    print_uscore_line()

    for _l in range(13):
        print_blank_line()
    print_footer()


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
            for _key, eol_value in EOL_VALUE.items():
                if _key == hw_type and check_val == eol_value:
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
        try:
            update_inventory(g_row)
        except Exception as _e:
            print(_e)
            err_str = "Google API Error. Please wait 1 minute to retry."
            display_alert(err_str)


def update_inventory(g_row):
    """
    Function to write data to google spreadsheet
    """
    HARDWARE.append_row(g_row)
    return g_row


def get_eol_hardware():
    """
    Get the total value for all EOL hardware
    """
    hw_type = []
    global TOT_EOL
    for hw_list, _eol_list in zip(INVENTORY[:-1], INV_EOL):
        curr_list_id = INVENTORY.index(hw_list)
        hw_type = inv_heads[curr_list_id]
        hw_item = hw_list[0]
        check_val = CURR_YR - int(hw_item[-2:])
        for hw_item in hw_list:
            for _key, eol_value in EOL_VALUE.items():
                if _key == hw_type and check_val == eol_value:
                    then = datetime.strptime(hw_item[-8:], "%d%m%Y")
                    if (datetime.now() - then) >= timedelta(365*eol_value):
                        TOT_EOL += 1
                        INV_EOL[curr_list_id].append(hw_item)
                    break
    balance_eolhw_inventory()


def balance_eolhw_inventory():
    """
    If there are any empty items in EOL_INV then this function
    will fill them with an empty string of 12 characters
    """
    max_len = max(len(sublist) for sublist in INV_EOL)
    for sublist in INV_EOL:
        while len(sublist) < max_len:
            sublist.append(' ' * 12)


def print_uscore_line():
    """
    Refactor print funtions using this function for underscore lines
    """
    print('\x1b[4;32;40m' + ' ' * 78 + '\x1b[0m')


def print_blank_line():
    """
    Refactor print funtions using this function for blank lines
    """
    print('\x1b[1;32;40m' + ' ' * 78 + '\x1b[0m')


def print_header():
    """
    Print terminal header text to screen
    """
    co_title = "ACME  Coders"
    app_name = "HARDWARE INVENTORY"

    usr_object = "User Account...: "
    usr_locale = "User Context...: "
    usr_obj_name = " Administrator "
    usr_loc_name = " Inventory EOL "
    date_string = "Current Date...: "
    eoli_string = "Total EOL HW...: "

    print_blank_line()

    spaces = int((78 - (len(co_title) + len(app_name))) / 3) * ' '

    print('\x1b[1;32;40m' + spaces + '\x1b[0m', end='')
    t_line = ''.join('\x1b[4;32;40m' + co_title + '\x1b[0m')
    print(t_line, end='')
    print('\x1b[1;32;40m' + spaces + '\x1b[0m', end='')
    t_line = ''.join('\x1b[4;32;40m' + app_name + '\x1b[0m')
    print(t_line, end='')
    print('\x1b[1;32;40m' + spaces + '\x1b[0m')

    print_uscore_line()
    print_blank_line()

    current_date = "  " + datetime.now().strftime("%x") + " "
    current_eoli = "     " + str(TOT_EOL).zfill(2) + "    "

    spaces = int((78 - (len(usr_object) + len(usr_obj_name)
                        + len(date_string) + len(current_date))) / 3) * ' '

    print('\x1b[1;32;40m' + spaces + '\x1b[0m', end='')
    t_line = ''.join('\x1b[4;32;40m' + usr_object + '\x1b[0m')
    print(t_line, end='')
    t_line = ''.join('\x1b[3;30;47m' + usr_obj_name + '\x1b[0m')
    print(t_line, end='')
    print('\x1b[1;32;40m' + spaces + '\x1b[0m', end='')
    t_line = ''.join('\x1b[4;32;40m' + date_string + '\x1b[0m')
    print(t_line, end='')
    t_line = ''.join('\x1b[3;30;47m' + current_date + '\x1b[0m')
    print(t_line, end='')
    print('\x1b[1;32;40m' + spaces + '\x1b[0m')

    print('\x1b[1;32;40m' + spaces + '\x1b[0m', end='')
    t_line = ''.join('\x1b[4;32;40m' + usr_locale + '\x1b[0m')
    print(t_line, end='')
    t_line = ''.join('\x1b[3;30;47m' + usr_loc_name + '\x1b[0m')
    print(t_line, end='')
    print('\x1b[1;32;40m' + spaces + '\x1b[0m', end='')
    t_line = ''.join('\x1b[4;32;40m' + eoli_string + '\x1b[0m')
    print(t_line, end='')
    t_line = ''.join('\x1b[3;30;47m' + current_eoli + '\x1b[0m')
    print(t_line, end='')
    print('\x1b[1;32;40m' + spaces + '\x1b[0m')

    print_blank_line()


def print_main_menu():
    """
    Display main menu
    """
    heading_1 = "  Select one of the options presented below by"
    heading_2 = " pressing the number indicated  "

    sel_choice_1 = "1: Show Inventory"
    sel_choice_2 = "2: Show EOL Items"
    sel_choice_3 = "3: Exit Inventory "

    spaces = int((78 - (len(sel_choice_1) + len(sel_choice_2)
                        + len(sel_choice_3))) / 4) * ' '

    print('\x1b[1;32;40m' + heading_1 + heading_2 + '\x1b[0m')

    print_blank_line()

    print('\x1b[1;32;40m' + spaces + '\x1b[0m', end='')
    print('\x1b[4;32;40m' + sel_choice_1 + '\x1b[0m', end='')
    print('\x1b[1;32;40m' + spaces + '\x1b[0m', end='')
    print('\x1b[4;32;40m' + sel_choice_2 + '\x1b[0m', end='')
    print('\x1b[1;32;40m' + spaces + '\x1b[0m', end='')
    print('\x1b[4;32;40m' + sel_choice_3 + '\x1b[0m', end='')
    print('\x1b[1;32;40m' + spaces + '  ' + '\x1b[0m')

    print_uscore_line()
    print_blank_line()


def print_inventory_menu():
    """
    Menu which appears when display inventory is selected
    """
    sel_choices_ = " Use the up and down arrows to navigate inventory"
    sel_choice_1 = "1: Show EOL Items"
    sel_choice_2 = "2: Exit Inventory "

    choices_len = len(sel_choices_)
    spaces = int((78 - choices_len) / 2) * ' '

    print('\x1b[1;32;40m' + ' ' + spaces + '\x1b[0m', end='')
    print('\x1b[1;32;40m' + sel_choices_ + '\x1b[0m', end='')
    print('\x1b[1;32;40m' + spaces + '\x1b[0m')

    print_blank_line()

    spaces = int((78 - (len(sel_choice_1) + len(sel_choice_2))) / 3) * ' '

    print('\x1b[1;32;40m' + ' ' + spaces + '\x1b[0m', end='')
    print('\x1b[4;32;40m' + sel_choice_1 + '\x1b[0m', end='')
    print('\x1b[1;32;40m' + spaces + '\x1b[0m', end='')
    print('\x1b[4;32;40m' + sel_choice_2 + '\x1b[0m', end='')
    print('\x1b[1;32;40m' + spaces + '\x1b[0m')

    print_uscore_line()
    print_headings()


def print_headings():
    """
    Display the hardware column headings
    """
    my_list = ['Screen', 'Laptop', 'Keyboard', 'Mouse']
    num_items = len(my_list)
    width = 78

    item_width = int(width / num_items)

    format_str = "{:^" + str(item_width) + "}"

    output_str = "".join([format_str.format(item) for item in my_list])
    headings = ''.join('\x1b[4;32;40m' + '  ' + output_str + '\x1b[0m')

    print(headings)

    print_blank_line()


def print_footer():
    """
    This prints out the bottom lines on the screen
    """
    app_n_str = "  EOL Inventory Checker "
    app_v_str = " CI-PP3  Version 1.0  "
    spaces = int(78 - (len(app_n_str) + len(app_v_str))) * ' '

    print_uscore_line()

    print('\x1b[1;32;40m' + app_n_str + '\x1b[0m', end='')
    print('\x1b[1;32;40m' + spaces + '\x1b[0m', end='')
    print('\x1b[1;32;40m' + app_v_str + '\x1b[0m')


def main_menu_interaction():
    """
    This function offers the user the ability to display information
    and interact with the terminal
    """
    os.system('clear')
    print_header()
    print_main_menu()
    for _l in range(11):
        print_blank_line()
    print_footer()

    while True:
        _k = readkey()
        if _k == "1":
            inventory_menu_interaction()
        if _k == "2":
            eol_menu_interaction()
        if _k == "3":
            break


def inventory_menu_interaction():
    """
    This function loads the inventory into a transposed array in order
    to correctly display and then checks for input from user while in
    the inventory display screen context
    """
    inventory_row = [list(sublist) for sublist in zip(*INVENTORY[:-1])]

    direction = 0
    display_inventory(direction, inventory_row)

    while True:
        _k = readkey()

        if _k == key.DOWN:
            direction += 10
            display_inventory(direction, inventory_row)

        if _k == key.UP:
            direction -= 10
            display_inventory(direction, inventory_row)

        if _k == "1":
            eol_menu_interaction()

        if _k == "2":
            main_menu_interaction()


def eol_menu_interaction():
    """
    This function checks for input from user while in
    the eol inventory display screen context
    """

    display_eol_hardware()

    while True:
        _k = readkey()
        if _k == "1":
            user_replace_eol_hw()
        if _k == "2":
            main_menu_interaction()


def user_replace_eol_hw():
    """
    Function for replacement of eol hardware by user
    """
    for hw_list1, hw_list2 in zip(INV_EOL, INVENTORY[:-1]):

        hw_items = [hw_item for hw_item in hw_list1 if hw_item in hw_list2]

        for _i, hw_item in enumerate(hw_list2):
            ID_COUNT = int(hw_list2[-1][1:4])
            hw_type = hw_list2[0][0]
            if hw_item in hw_items:
                hw_item_idx1 = hw_list1.index(hw_item)
                hw_item_idx2 = hw_list2.index(hw_item)
                hw_list1.pop(hw_item_idx1)
                hw_list2.pop(hw_item_idx2)
                today_date = date.today().strftime("%d%m%Y")
                new_hardware = hw_type+str(ID_COUNT + 1).zfill(3)+today_date
                hw_list2.append(new_hardware)

    eol_menu_interaction()


def display_alert(err_str):
    """
    Display and alert message on main screen
    """
    if err_str.startswith("Google"):
        os.system('clear')
        print_header()
        for _i in range(3):
            print_blank_line()
        print_uscore_line()

    continue_str = "Please press the spacebar to continue "
    spaces = int((78 - len(err_str)) / 2) * ' '

    for _i in range(5):
        print_blank_line()

    print('\x1b[1;32;40m' + spaces + '\x1b[0m', end='')
    print('\x1b[1;32;40m' + err_str + '\x1b[0m', end='')
    print('\x1b[1;32;40m' + spaces + '\x1b[0m')

    spaces = int((78 - len(continue_str)) / 2) * ' '

    print('\x1b[1;32;40m' + spaces + '\x1b[0m', end='')
    print('\x1b[1;32;40m' + continue_str + '\x1b[0m', end='')
    print('\x1b[1;32;40m' + spaces + '\x1b[0m')

    for _i in range(4):
        print_blank_line()

    print_footer()

    while True:
        _k = readkey()
        if _k == key.SPACE:
            break


def display_inventory(direction, inventory_row):
    """
    Display the contents of the hardware inventory 9 rows a time
    """
    os.system('clear')
    print_header()
    print_inventory_menu()

    for i in range(direction, direction + 10):
        if i < 0:
            err_str = "Already at the top of the inventory "
            display_alert(err_str)
            inventory_menu_interaction()
        elif i >= len(inventory_row):
            err_str = "You reached the end of the inventory"
            display_alert(err_str)
            inventory_menu_interaction()
        else:
            sps = ' ' * 5
            print('\x1b[1;32;40m' + sps + '  ', sps.join('\x1b[1;32;40m' +
                                                         str(i)for i in
                                                         inventory_row[i])
                  + sps + '  ' + '\x1b[0m')

    print_footer()


def display_eol_hardware():
    """
    This function loads the eol inventory into a transposed array in order
    to correctly display and then applies changes based on input from the user
    """
    os.system('clear')
    blank_rows = 10 - len(INV_EOL)
    print_header()
    print_eolhw_menu()

    eol_inventory = [list(sublist) for sublist in zip(*INV_EOL)]

    for i, eol_row in enumerate(eol_inventory):
        if i >= len(eol_row):
            err_str = " There are more EOL items remaining "
            display_alert(err_str)
            inventory_menu_interaction()
        else:
            sps = ' ' * 5
            print('\x1b[1;32;40m' + sps + '  ', sps.join('\x1b[1;32;40m' +
                                                         str(i) for i in
                                                         eol_row) + sps +
                  '  ' + '\x1b[0m')

    for _i in range(blank_rows):
        print_blank_line()

    print_footer()


def print_eolhw_menu():
    """
    Menu which appears when display inventory is selected
    """
    sel_choices_ = "  Select from one of the options presented below  "
    sel_choice_1 = "1: Replace EOL Hardware"
    sel_choice_2 = "2: Exit EOL Inventory "

    choices_len = len(sel_choices_)
    spaces = int((78 - choices_len) / 2) * ' '

    print('\x1b[1;32;40m' + spaces + '\x1b[0m', end='')
    print('\x1b[1;32;40m' + sel_choices_ + '\x1b[0m', end='')
    print('\x1b[1;32;40m' + spaces + '\x1b[0m')

    spaces = int((80 - (len(sel_choice_1) + len(sel_choice_2))) / 3) * ' '

    print_blank_line()

    print('\x1b[1;32;40m' + spaces + '\x1b[0m', end='')
    print('\x1b[4;32;40m' + sel_choice_1 + '\x1b[0m', end='')
    print('\x1b[1;32;40m' + spaces + '\x1b[0m', end='')
    print('\x1b[4;32;40m' + sel_choice_2 + '\x1b[0m', end='')
    print('\x1b[1;32;40m' + spaces + '\x1b[0m')

    print_uscore_line()
    print_headings()


def main():
    """
    Run all program functions.
    """
    global CURR_YR
    initialize_display()
    for year in reversed(range(5)):
        generate_dates(year)
        generate_churn_list()
        simulate_churn(year)
        simulate_eol_replacement(year)
        CURR_YR += 1
    get_eol_hardware()
    generate_new_inventory()
    main_menu_interaction()


main()
