import datetime
today1 = datetime.date.today()
today2 = "{0:%Y/%m/%d}".format(today1)
print(today1)
print(today2)

print(type(today2))
