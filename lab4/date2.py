import datetime

today = datetime.datetime.today().date()
yesterday = today - datetime.timedelta(days=1)
tomorrow = today + datetime.timedelta(days=1)

print(f'Today: {today}')
print(f'Yestarday: {yesterday}')
print(f'Tomorrow: {tomorrow}')