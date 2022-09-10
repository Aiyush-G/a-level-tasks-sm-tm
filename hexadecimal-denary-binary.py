###
# Program that converts numbers between hexadecimal, denary, binary
# 1. Figures out the input type based upon notation
# 2. Don't use any inbuilt modules
# 3. TUI / GUI
# 4. 16-bit, possibly 32-bit

# Determines type of input
import re


def _type(starting):
    
    # Binary or Denary    
    if starting.isdigit():
        numType = possibleTypes[0] # BIN
        for n in starting:
            if int(n)!= 0:
                numType = possibleTypes[1] # DEN
    else:
        numType = possibleTypes[2] # HEX
    
    return numType

# Validates Binary Format to ensure it is multiple of 8 bits
def checkBinaryFormat(n):
    if len(list(n))%8 != 0:
        return errors["BINARY FORMAT"]
        
    return True

# Validates Hex Format to contain allowed characters
def checkHexFormat(n):
    allowedChars = "0,1,2,3,4,5,6,7,8,9,A,B,C,D,E,F".split(",")

    for char in str(n):
        if char.upper() not in allowedChars:
            return errors["HEX FORMAT"]
            
    return True

# Helper Function To auto-validate function
def checkStarting(startingType, starting):
    try:
        if startingType == "BIN": 
            if checkBinaryFormat(starting) == errors["BINARY FORMAT"]:
                return False, errors["BINARY FORMAT"]
        elif startingType == "HEX": 
            if checkHexFormat(starting) == errors["HEX FORMAT"]:
                return False, errors["HEX FORMAT"]
                

        # ELIF DENARY
        return True, "Successful"
    except TypeError:
        return False, "Unsuccessful"

# ENTRY, will return error message to console provided by helper functions
def getStartInput(message = None):
    startingType = "INVALID"
    if message:
        print(f"{message}")
    starting = input("Enter the input >>> ")

    validatedSuccessfully, message = checkStarting(_type(starting), starting)

    if validatedSuccessfully:
        startingType = _type(starting)
    else:
        print(message)
        
    return startingType

errors = {
    "HEX FORMAT" : "INVALID HEX AND/OR INPUT NOT ACCEPTED",
    "BINARY FORMAT" : "BINARY NUMBER MUST BE 8 BITS",
}

'''
possibleTypes = "BIN DEN HEX".split(" ")
getStartInput()
'''

#run()
#starting = input("Enter the input")
#startingType = _type(starting) if checkStarting(_type(starting), starting) else "unknown"



def binToDen(n):
    # 10101101
    total = 0
    bList = [(2**x) for x in range(len(n) - 1, -1, -1)]
    
    for index in range(0, len(n)):
        if int(n[index]) == 1:
            total += bList[index]
    
    return total

def denToBin(n):
    n = int(n)
    bList = [(2**x) for x in range(n.bit_length() - 1, -1, -1)]
    b = ""
    for num in bList:
        if (n - num) > -1:
            n -= num
            b+= str(1)
        else: b+= str(0)
    return b

def hexToBinary(n):
    hexValues = {0:0, 1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, "A":10, "B":11, "C":12, "D":13, "E":14, "F":15}
    b = ""
    for hexDigit in list(n):
        for digit in denToBin(hexValues[hexDigit]): b+= str(digit)
    return b

def binaryToHex(n):
    # 0101 0101 -> denary -> hex
    left = int(len(n))%8
    # print(f"LEFT: {left}")
    if left != 0:
        toAdd = ""
        for _ in range(0, 8-left): toAdd += "0"
        n = toAdd + n
    
        
    hexValues = {0:0, 1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:"A", 11:"B", 12:"C", 13:"D", 14:"E", 15:"F"}
    split = []
    hex = ""
    while n:
        split.append(n[:4])  
        n = n[4:]
    for _4bit in split:
        hex+= str(hexValues[binToDen(_4bit)])
    
    return hex

def hexToDenary(n):
    return binToDen(hexToBinary(n))

def denaryToHex(n):
    return binaryToHex(denToBin(n))

#print(denToBin(999))
print(denaryToHex("511"))
#print(binaryToHex("0000000111111111"))

#print(hexToDenary("BCD"))
#binToDen(hexToBinary("AA"))
#binToDen("10101101")
#denToBin(255)