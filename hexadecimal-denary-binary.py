###
# Program that converts numbers between hexadecimal, denary, binary
# 1. Figures out the input type based upon notation
# 2. Don't use any inbuilt modules
# 3. TUI / GUI
# 4. 16-bit, possibly 32-bit
errors = {"HEX FORMAT" : "INVALID HEX character",
}
#print(errors["HEX FORMAT"])

def _type(starting):

    if starting.isdigit():
        # Binary or Denary
        #starting = int(starting)
        
        numType = possibleTypes[0] # BIN
        for n in starting:
            if int(n)!= 0:
                numType = possibleTypes[1] # DEN
    else:
        numType = possibleTypes[2] # HEX
    
    return numType

def checkBinaryFormat(n):
    # Binary number has to have 8 full bits
    if len(list(n))%8 != 0:
        getStartInput(message="Binary number must be 8 bits")
    return True

def checkHexFormat(n):
    allowedChars = "0,1,2,3,4,5,6,7,8,9,A,B,C,D,E,F".split(",")
    #print(allowedChars)
    for char in str(n):
        if char.upper() not in allowedChars:
            # print(char)
            return "INVALID HEX"
            #return f"INVALID HEX: {char}"
    return True

def checkStarting(startingType, starting):
    try:
        if startingType == "BIN": checkBinaryFormat(starting)
        elif startingType == "HEX": 
            if checkHexFormat(starting) == "INVALID HEX":
                return False, "INVALID HEX"
                # getStartInput(message = "INVALID HEX")

        # ELIF DENARY
        return True, "Successful"
    except TypeError:
        return False, "Unsuccessful"

def getStartInput(message = None):
    startingType = "INVALID"
    if message:
        print(f"{message}")
    starting = input("Enter the input >>> ")

    #print(_type(starting))
    #print(starting)

    validatedSuccessfully, message = checkStarting(_type(starting), starting)

    if validatedSuccessfully:
        startingType = _type(starting)
    else:
        print(message)
        #startingType = "INVALID"

    # startingType = _type(starting) if checkStarting(_type(starting), starting) else "unknown"
    return startingType
           
possibleTypes = "BIN DEN HEX".split(" ")
print(getStartInput())

#run()
#starting = input("Enter the input")
#startingType = _type(starting) if checkStarting(_type(starting), starting) else "unknown"
