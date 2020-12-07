import random
startHour = 7
startMinutes = 30

startAdd = random.randint(0, 135)
startAdd += startMinutes
while startAdd > 59:
    startHour += 1
    startAdd -= 60
smallerThenTenPadding = ""
if startAdd < 10:
    smallerThenTenPadding = "0"
print("Start Hour: " + str(startHour) + ":" +
      smallerThenTenPadding + str(startAdd))
workingHours = random.randint(560, 660)
# workingHours = random.randint(290, 390) # half day
workingHours += startAdd
while workingHours > 59:
    startHour += 1
    workingHours -= 60
smallerThenTenPadding = ""
if workingHours < 10:
    smallerThenTenPadding = "0"
print("Worked Until: " + str(startHour) + ":" +
      smallerThenTenPadding + str(workingHours))
