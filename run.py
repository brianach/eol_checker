import gspread
from google.oauth2.service_account import Credentials
from datetime import timedelta, date

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('credentials.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("hw_inventory")

def test_write():
    """
    Test opening the sheet and writing some data in
    """

    while True:
        print("Add some test data. ")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")
        data_str = input("Enter your data here: \n")

        test_data = list(data_str.split(","))

        if validate_data(test_data):
            break

    return test_data
    

def validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """

    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values are required, you provided {len(values)}")

    except ValueError as e:
        print(f"Invalid data: {e}, please try again\n")
        return False

    return True


def update_worksheet(new_row, worksheet):
    """
    Update the specified worksheet,
    adding a new row with the list data provided.
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)

    # adds new row to the end of the current data
    worksheet_to_update.append_row(new_row)

    print(f"{worksheet} worksheet updated successfully\n")


def get_values():
    """
    Get the data from the inventory
    """
    
    headings = SHEET.worksheet("hardware").row_values(1)
    hwvalues = SHEET.worksheet("hardware").row_values(2)

    hw_values = []

    for head, value in zip(headings, hwvalues):
        hw_values.append((head[:1]).capitalize() + str(1).zfill(3) + str(int(value) * 365).zfill(5))

    print(f"These are the current hw data values: {hw_values} \n")

    return hw_values


def main():
    """
    Run all program functions.
    """
    data = test_write()
    test_data = [int(num) for num in data]
    update_worksheet(test_data, "hardware")
    get_values()


main()

