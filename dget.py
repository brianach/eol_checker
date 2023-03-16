from datetime import timedelta, date, datetime


def days_ago(n):
    # return date.today() - timedelta(n)
    ddate = datetime(2023, 1, 1) - timedelta(n)
    return ddate
    

for y in range( 1 , 6 ):
    # get the bumber of days before Jan 01 2003 for the last 5 years
    print(days_ago(365*y).strftime("%d%m%Y"))
