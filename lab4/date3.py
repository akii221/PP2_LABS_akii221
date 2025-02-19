import datetime 

today = datetime.datetime.today()
new_today = today.replace(microsecond=0)

print(new_today)