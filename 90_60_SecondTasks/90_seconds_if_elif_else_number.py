# If, elif, else in 90 seconds

import datetime as d

dayNumber = d.datetime.now().strftime("%w")
selectedNumber = int(input("Choose any number between 1 and 5 >>>"))

if selectedNumber == 1:
    print(f"Your number {selectedNumber} timed by the current day of the week (where Monday is 1) is {selectedNumber * (int(dayNumber) + 1)}")
elif selectedNumber == 2:
    print(f"2 x 2 is 4")
else:
    print("Your number is not equal to one or two! ")