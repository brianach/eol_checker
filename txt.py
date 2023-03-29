"""
Test Print
"""

from datetime import datetime


def print_data():
    """
    Print some text to screen
    """
    prt = ''.join('\x1b[1;32;40m' + ' ' + '\x1b[0m' for i in range(120))
    print(prt)
    prt = ''.join('\x1b[4;32;40m' + ' ' + '\x1b[0m' for i in range(120))
    print(prt)
    for i in range(2):
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
    for i in range(2):
        prt = ''.join('\x1b[1;32;40m' + ' ' + '\x1b[0m' for i in range(120))
        print(prt)

    usr_object = "User Account......: "
    usr_locale = "User Context......: "
    usr_obj_name = " Administrator "
    usr_loc_name = " Inventory EOL "
    date_string = "Current Date...: "
    eoli_string = "Total EOL HW...: "
    current_date = datetime.now().strftime("%x")
    current_eoli = "   23   "

    line_sps = int((120 - (len(usr_object) + len(usr_obj_name)
                    + len(date_string) + len(current_date))) / 3)

    prt = ''.join('\x1b[1;32;40m' + ' ' + '\x1b[0m' for i in range(line_sps-5))
    print(prt, end='')
    t_line = ''.join('\x1b[4;32;40m' + usr_object + '\x1b[0m')
    print(t_line, end='')
    t_line = ''.join('\x1b[0;30;47m' + usr_obj_name + '\x1b[0m')
    print(t_line, end='')
    prt = ''.join('\x1b[1;32;40m' + ' ' + '\x1b[0m' for i in range(line_sps))
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
    prt = ''.join('\x1b[1;32;40m' + ' ' + '\x1b[0m' for i in range(line_sps))
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
    for i in range(2):
        prt = ''.join('\x1b[1;32;40m' + ' ' + '\x1b[0m' for i in range(120))
        print(prt)

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


print_data()
