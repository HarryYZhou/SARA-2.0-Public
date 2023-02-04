import datetime
today = datetime.datetime.utcnow()
ten_hours_from_utc = today + datetime.timedelta(hours=11)
weekday = today.weekday()
weekday2 = ten_hours_from_utc.weekday()

print(weekday)
print(today)
print(ten_hours_from_utc)
print(weekday2)