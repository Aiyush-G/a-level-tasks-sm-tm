# If, else Statement 
import datetime as d

day = d.datetime.now()
weekday = day.strftime("%A")

userDay = str(input("Enter any day of the week. "))

if userDay == day:
    print(f"Hey, you chose {userDay} and it is {weekday} today!")
else:
    print("Hmm... that's a pretty cool day of the week!")