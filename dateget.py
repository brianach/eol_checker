from datetime import timedelta, date

def days_ago(n):
  return date.today() - timedelta(n)
  
print(days_ago(985).strftime("%d%m%Y"))

