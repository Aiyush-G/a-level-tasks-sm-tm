import hbd_gui_ui as gui # pyuic6 -x -o hbd_gui_ui.py hdb_gui.ui

from PySide6 import QtCore, QtWidgets

class ConversionWindow(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs): # Passing over any parameters
        super().__init__(*args, **kwargs)

        self.errors = {
            "HEX FORMAT" : "INVALID (HEX) AND/OR INPUT NOT ACCEPTED",
            "BINARY FORMAT" : "BINARY NUMBER MUST BE 8 BITS",
            "DENARY FORMAT": "DENARY CONTAINS DISALLOWED CHAR"
        }

        self.possibleTypes = "BIN DEN HEX AUTO INVALID".split(" ")
        self.inputType = None
        self.validInput = False

        # From QT Designer
        self.ui = gui.Ui_Form()
        self.ui.setupUi(self) # Builds the design onto the widget
        

        self.ui.convert_pushButton.clicked.connect(self.handleInput)
        self.ui.credits.setHtml("""
        <h1>Aiyush Gupta - 12PT - 2022</h1>
        <p>Hexadecimal to binary to denary converter with automatic detection for input. 
        Written in Python using PyQT graphics library for GUI.</p>
        """)
        #self.ui.console.insertPlainText("text")
    
    
    #### CONVERSION

    def binToDen(self, n):
        total = 0
        bList = [(2**x) for x in range(len(n) - 1, -1, -1)]
        
        for index in range(0, len(n)):
            if int(n[index]) == 1:
                total += bList[index]
    
        return total
    
    def denToBin(self, n):
        n = int(n)
        bList = [(2**x) for x in range(n.bit_length() - 1, -1, -1)]
        b = ""
        for num in bList:
            if (n - num) > -1:
                n -= num
                b+= str(1)
            else: b+= str(0)
        return b

    def hexToBinary(self, n):
        hexValues = {0:0, 1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, "A":10, "B":11, "C":12, "D":13, "E":14, "F":15}
        b = ""
        for hexDigit in list(n):
            for digit in self.denToBin(hexValues[hexDigit.upper()]): b+= str(digit)
        return b

    def binaryToHex(self, n):
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
            hex+= str(hexValues[self.binToDen(_4bit)])
        
        return hex

    def hexToDenary(self, n):
        return self.binToDen(self.hexToBinary(n))

    def denaryToHex(self, n):
        return self.binaryToHex(self.denToBin(n))

    #### HANDLE UI
    def handleInput(self):
        _input = self.ui.input_lineEdit.text()

        if _input == "":
            self.addToConsole(f"No Input Detected \n")
            print("No Input Detected")

        elif self.ui.autoType_radioButton.isChecked():
            self.inputType = self._type(_input)
            self._typeCheckValidated(_input)

        elif self.ui.hexadecimalType_radioButton.isChecked():
            #if self.checkHexFormat(self, _input):
            self.inputType = self.possibleTypes[2]
            self._typeCheckValidated(_input)
            # else err

        elif self.ui.denaryType_radioButton.isChecked():
            #if self.checkDenaryFormat(self, _input):
            self.inputType = self.possibleTypes[1]
            self._typeCheckValidated(_input)
            

        elif self.ui.binaryType_radioButton.isChecked():
            #if self.checkBinaryFormat(self, _input):
            self.inputType = self.possibleTypes[0]
            self._typeCheckValidated(_input)
        
        if self.validInput:
            if self.inputType == self.possibleTypes[0]: # BIN
                # BIN TO HEX, BIN TO DENARY
                hex = self.binToDen(_input)
                den = self.binaryToHex(_input)
                self.addToConsoleAndCalculation(f"{_input} to hexadecimal is {hex} ")
                self.addToConsoleAndCalculation(f"{_input} to denary is {den} ")

            elif self.inputType == self.possibleTypes[1]: # DEN 
                hex = self.denaryToHex(_input)
                bin = self.denToBin(_input)
                self.addToConsoleAndCalculation(f"{_input} to hexadecimal is {hex} ")
                self.addToConsoleAndCalculation(f"{_input} to binary is {bin} ")

            elif self.inputType == self.possibleTypes[2]: # HEX
                bin = self.hexToBinary(_input)
                den = self.hexToDenary(_input)
                self.addToConsoleAndCalculation(f"{_input} to binary is {bin} ")
                self.addToConsoleAndCalculation(f"{_input} to denary is {den} ")

            
        self.addToConsole(f"Valid input: {self.validInput} \n")
        self.addToConsole(f"Valid input: {self.inputType} \n")
        print(f"Valid input: {self.validInput}")
        print(f"Input type: {self.inputType}")

    def addToConsole(self, text):
        self.ui.console.insertPlainText(text + "\n")
    
    def addToConsoleAndCalculation(self, text):
        self.ui.calculation.insertPlainText(text + "\n")
        self.addToConsole(text)

    def _type(self, starting):
        # Binary or Denary    
        if starting.isdigit():
            numType = self.possibleTypes[0] # BIN
            for n in starting:
                if int(n)!= 0:
                    numType = self.possibleTypes[1] # DEN
        else:
            numType = self.possibleTypes[2] # HEX
        
        return numType
    
    def _typeCheckValidated(self, _input):
        validatedMsg = self._typeCheckFormat(_input)
            
        if validatedMsg == True:
            self.validInput = True
        else:
            self.addToConsole(f"Validated Message: {validatedMsg} \n")
            print(validatedMsg)
    
    def _typeCheckFormat(self, _input):
        def errCheck(validated):
            if validated == True: 
                self.validInput = True
                return True
            else:
                self.validInput = False
                return validated
            
        if self.inputType == self.possibleTypes[0]: # BINARY
            validated = errCheck(self.checkBinaryFormat(_input))
            
            
        elif self.inputType == self.possibleTypes[1]: # DENARY
            validated =  errCheck(self.checkDenaryFormat(_input))
            

        elif self.inputType == self.possibleTypes[2]: # HEX
            validated =  errCheck(self.checkHexFormat(_input))
        
        else:
            self.addToConsole(f"Input Type: {self.inputType} \n")
            print(f"Input Type: {self.inputType}")
        return validated
                
    
    def checkHexFormat(self, n):
        allowedChars = "0,1,2,3,4,5,6,7,8,9,A,B,C,D,E,F".split(",")

        for char in str(n):
            if char.upper() not in allowedChars:
                return self.errors["HEX FORMAT"]
                
        return True
    
    def checkBinaryFormat(self, n):
        if len(list(n))%8 != 0:
            return self.errors["BINARY FORMAT"]
            
        return True
    
    def checkDenaryFormat(self, n):
        if str(n).isdigit():
            return True
        else:
            return self.errors["DENARY FORMAT"]
    

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    widget = ConversionWindow()
    widget.show()

    app.exec()