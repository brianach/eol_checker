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

USERS = 25  # notional number of employees

USER, LAPT, SCRN, DOCK, KEYB, MOUS, PHON, HIRE = ([] for l_i in range(8))
INVENTORY = [USER, LAPT, SCRN, DOCK, KEYB, MOUS, PHON, HIRE]

UMEM, LMEM, SMEM, DMEM, KMEM, MMEM, PMEM, HMEM = ([] for l_i in range(8))
INV_MEM = [UMEM, LMEM, SMEM, DMEM, KMEM, MMEM, PMEM, HMEM]


def make_inv_list():
    """
    Function to generate inventory of data entered using random ordered dating
    """
    id_count = 1

    for year in reversed(range(4)):
  
        dthire = []

        for day in range(1, 1+USERS//5):
            rand_days = random.randrange(1, 365)  # create a random number
            # generate a random date
            sdate = datetime(2022, 12, 30) - timedelta((365*(year)+rand_days))
            dthire.append(sdate.strftime("%d%m%Y"))  # add random date
            HIRE = sorted(dthire, key=lambda hird: (hird[2:4], hird[0:2]))
        #print(HIRE)

        for dat in HIRE:
            i_list = 0
            for i_list in range(len(INVENTORY)-1):
                INVENTORY[i_list].append(inv_heads[i_list][0].capitalize()+str(id_count).zfill(3)+dat)
            id_count += 1
            
        for i_list in INVENTORY:
            print(i_list)
        
    for year in reversed(range(4)):

        i_list = 0
        for i_list in range(len(INVENTORY)-1):
            # this loop generates random items to simulate real world 
            # replacement of employees or hardware based on real world data
            rand_change = random.randrange(1, 3)  # select random number
            remove_items = random.sample(INVENTORY[i_list], rand_change)
            for r in remove_items:
                # add the removal values to a list for checking against the
                # associated inventory list eg: LAPT[] : LMEM[]
                INV_MEM[i_list].append(r)

        #for i_list in INV_MEM:
        #    print(i_list)   

        #simulate_changes()  # call the function for the given year

        simulate_eol_replacement(year)  # simulate replacement of aged hardware

        pos = 0  # position of item in list
        for u in USER:
            g_row = []
            for i_list in range(len(INVENTORY)-1):
                g_row.append(INVENTORY[i_list][pos])  # populate the inventory
            g_row.append(u[-8:])  # add the date field
            #print(f"This is year {year} and the data is {g_row}")
            #update_inventory(g_row)
            pos += 1

        # update_inventory(g_row)
            #print(f"This is year {year} and the data is {g_row}")


def update_inventory(g_row):
    """
    #Function to add data to google spreadsheet
    """
    inventory_worksheet = SHEET.worksheet("hardware")

    inventory_worksheet.append_row(g_row)



def simulate_changes():
    """
    This function simulates users leaving and hardware replacement due to failure.
    It removes the associated item from the list and appends the new replacements.
    """
    for year in reversed(range(4)):

        i_list = 0  # counter for inventory current list
        for i_list in range(len(INVENTORY)-1):
            list_i = 0  # counter for inventory current list current list item
            for i in INVENTORY[i_list]:
                r = 0  # counter for inventory memory if removal list item
                # this next loop checks the values in the random replacement lists
                # against the original list type. eg: LAPT[] : LMEM[]
                for r in range(len(INV_MEM[i_list])):
                    comp_string = INV_MEM[i_list][r][-8:]
                    inv_lst_item = i[-8:]

                    if comp_string == inv_lst_item:
                        # if a match is found the orignal item is removed from the list
                        # then the new item gets an incremented ID and the item is appended
                        del_date = datetime.strptime(comp_string, "%d%m%Y")
                        year_day = del_date.strftime("%j")
                        rand_days = random.randrange(1, int(year_day))
                        new_date_str = datetime(2022, 12, 30)-timedelta((365*(year)+rand_days))
                        new_date = new_date_str.strftime("%d%m%Y")
                        new_string = i[:1]+str((year + 1)*10+1+r).zfill(3)+new_date
                        INVENTORY[i_list].pop(list_i)
                        INVENTORY[i_list].append(new_string)
                    comp_string = ""  # reinitialise the string once used
            list_i += 1

        for i_list in INVENTORY:
            print(i_list)


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


make_inv_list()

