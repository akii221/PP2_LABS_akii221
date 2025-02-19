import datetime
# # YYYY, MM, DD, HH, MM, SS format dati

date1 = datetime.datetime(2025, 8, 8, 12, 10, 40)
date2 = datetime.datetime(2025, 8, 8, 12, 5, 15 )
difference = date1 - date2


seconds = difference.total_seconds()
print(seconds)

