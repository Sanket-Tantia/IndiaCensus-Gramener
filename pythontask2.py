from datetime import date

startDate = date(1990, 1, 1)
endDate = date(2000, 1, 1)
diff = (endDate-startDate).days
day_of_week = startDate.weekday()
ans = (diff//7)
for i in range(diff%7):
    if day_of_week in [2]:
        ans += 1
    day_of_week = (day_of_week +1) %7
print (ans)
