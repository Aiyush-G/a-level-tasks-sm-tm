# 90 Seconds if, else nested two inputs


def evalNumber(favNumber):
    if favNumber > 100:
        if favNumber % 2 == 0:
            print("You chose a large number that is even")
        else:
            print("You chose a larger number that is odd")
    else:
        print("Your number is quite low :( ")
        again = str(input("Would you like to choose another number? Y/N"))
        if again.upper() == "Y":
            favNumber = int(input("Enter your favourite number >>> "))
            evalNumber(favNumber)

favNumber = int(input("Enter your favourite number >>> "))
evalNumber(favNumber)