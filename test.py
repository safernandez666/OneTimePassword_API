from datetime import datetime

time1 = "2021-10-05 19:45:13"
time2 = "2021-10-05 19:46:51"

d1 = datetime.strptime(time1, "%Y-%m-%d %H:%M:%S")
d2 = datetime.strptime(time2, "%Y-%m-%d %H:%M:%S")

print(d1)
print(d2)

print(d2-d1)