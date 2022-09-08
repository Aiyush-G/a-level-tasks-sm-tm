###
# Program that converts numbers between hexadecimal, denary, binary
# 1. Figures out the input type based upon notation
# 2. Don't use any inbuilt modules
# 3. TUI / GUI
# 4. 16-bit, possibly 32-bit

possibleTypes = "BIN DEN HEX".split(" ")
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
    if n%8 != 0:
        return False
    return True

def checkHexFormat(n):
    allowedChars = "0,1,2,3,4,5,6,7,8,9,A,B,C,D,E,F".split(",")
    print(allowedChars)
    for char in str(n):
        if char.upper() not in allowedChars:
            print(char)
            return False
    return True

def checkStarting(_type):
    pass

# print(checkHexFormat("ede345"))
            

starting = input("Enter the input")
startingType = _type(starting)