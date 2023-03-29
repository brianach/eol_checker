"""
Print ANSO color tables
"""


def print_format_table():
    """
    prints table of formatted text format options
    """
    for style in range(8):
        for f_g in range(30, 38):
            s_1 = ''
            for b_g in range(40, 48):
                fromat = ';'.join([str(style), str(f_g), str(b_g)])
                s_1 += '\x1b[%sm %s \x1b[0m' % (fromat, fromat)
            print(s_1)
        print('\n')


print_format_table()
