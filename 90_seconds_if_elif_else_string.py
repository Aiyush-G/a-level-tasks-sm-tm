# If, elif, else
from random import randint 

subjectList = "Maths, Chemistry, Physics".split(", ")

print("Enter your favourite subject out of the following:")
print(*subjectList)

favouriteSubj = str(input(">>> ")).lower()

if favouriteSubj == "maths":
    print("You chose the best subject")
elif favouriteSubj == "physics":
    print("You chose the second best subject")
else:
    print("You chose a boring subject :( ")

