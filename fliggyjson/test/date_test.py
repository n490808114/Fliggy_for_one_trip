import datetime

start_date = datetime.datetime.strptime(input("please input scrapy start date"),'%Y-%m-%d')
print(type(start_date))

times = int(input("how many days you want search?"))
print(type(times))

for i in range(times):
    date = start_date + datetime.timedelta(days=i)
    print(type(date))
    print(date)
    d = date.strftime('%Y-%m-%d')
    print(type(d))
    print(d)