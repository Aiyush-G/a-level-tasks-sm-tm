# If Statement
import datetime as d

day = d.datetime.now().strftime("%A")
userDay = str(input("Enter any day of the week. "))

if userDay == day:
    print(f"Hey, you chose {userDay} and it is {day} today!")