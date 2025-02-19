import datetime

current_date = datetime.datetime.today().date()
newd = current_date - datetime.timedelta(days=5)

print(newd)