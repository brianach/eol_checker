def print_data():
    """
    Print some text to screen
    """
    print('\x1b[1;32;40m' + '                                                                                                    ' + '\x1b[0m')
    print('\x1b[1;32;40m' + ' -------------------------------------------------------------------------------------------------- ' + '\x1b[0m')
    print('\x1b[1;32;40m' + '                                                                                                    ' + '\x1b[0m')
    print('\x1b[1;32;40m' + '                          ' + '\x1b[4;32;40m' + 'ACME Coders' + '\x1b[0m' + '\x1b[1;32;40m' + '               ' + '\x1b[4;32;40m' + 'HARDWARE INVENTORY' + '\x1b[0m' + '\x1b[1;32;40m' + '                              ' + '\x1b[0m')
    print('\x1b[1;32;40m' + '                                                                                                    ' + '\x1b[0m')
    print('\x1b[1;32;40m' + ' -------------------------------------------------------------------------------------------------- ' + '\x1b[0m')
    print('\x1b[1;32;40m' + '                                                                                                    ' + '\x1b[0m')
    print('\x1b[1;32;40m' + '        User Account......: ' + '\x1b[2;30;40m' + ' Administrator ' + '\x1b[0m' + '\x1b[1;32;40m' + '                                                         '+ '\x1b[0m')
    print('\x1b[1;32;40m' + '        User Context......: ' + '\x1b[2;30;40m' + ' Inventory EOL ' + '\x1b[0m' + '\x1b[1;32;40m' + '                                                         '+ '\x1b[0m')
    print('\x1b[1;32;40m' + '                                                                                                    ' + '\x1b[0m')
    print('\x1b[1;32;40m' + '                                                                                                    ' + '\x1b[0m')
    print('\x1b[1;32;40m' + ' -------------------------------------------------------------------------------------------------- ' + '\x1b[0m')
    print('\x1b[1;32;40m' + '                                                                                                    ' + '\x1b[0m')
    print('\x1b[1;32;40m' + '                                                                                                    ' + '\x1b[0m')
    print('\x1b[6;30;42m' + 'Success!' + '\x1b[0m')


print_data()

def print_format_table():
    """
    prints table of formatted text format options
    """
    for style in range(8):
        for fg in range(20,38):
            s1 = ''
            for bg in range(30,48):
                format = ';'.join([str(style), str(fg), str(bg)])
                s1 += '\x1b[%sm %s \x1b[0m' % (format, format)
            print(s1)
        print('\n')

#print_format_table()