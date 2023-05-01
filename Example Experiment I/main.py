from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from random import *
from os import listdir


app = QApplication([])
window = uic.loadUi("paradigm.ui")
window.mainStack.setCurrentIndex(0)  # ensuring experiment begins on the first page
window.settingsBox.hide()  # hiding settings to be revealed upon button press
fileList = listdir()  # current directory files

#RESULTS FILE CREATION

#creating / opening the results CSV and writing column headings
if "results.csv" not in fileList: # creating the results file, if not present
    csv = open("results.csv", "w")
    csv.close()
else:
    None

csv = open("results.csv", "r")  # opening in readonly
aLineCSV = csv.readline()  # pulling the first line
if "Name, Age," not in aLineCSV or aLineCSV == "":  # writing header, if not present
    csv.close()
    csv = open("results.csv", "a")
    csv.write("Name, Age, Gender, Education, Current Condition,  Random Urn, Selected Urn, Drawn Marble \n")
else:
    csv.close()
    csv = open("results.csv", "a")


#STACKWIDGET INFORMATION / EXPERIMENT SETTINGS
window.currStackIndex = 0  # initialising stacked widget index

#conditions saved in a list - values can be added if >4 conditions necessary
window.conditionList = ["2", "10", "100"]

#MISC FUNCTIONS
def proceed():  # function to go to the next page of the experiment
    window.currStackIndex += 1
    window.mainStack.setCurrentIndex(window.currStackIndex)  # modifying stackwidget index

#SETTINGS BOX

password = "admin123" # password to access experimenter settings box
window.passwordIndex = 0
passwordError = QLabel(window.login)  # error label
passwordError.setGeometry(30, 180, 300, 40)

def login():  # function to check password, return error
    inputPW = window.pwBox.text()
    if inputPW == password:
        window.passwordIndex += 1
        window.settingsBox.setCurrentIndex(window.passwordIndex)
    else:
        passwordError.setText("Wrong password. Please try again.")
        passwordError.show()
window.logButton.clicked.connect(login)


window.cond4.hide()
window.cond4lab.hide()

def addCond():  # button allowing addition of a fourth condition
    window.cond4.show()
    window.cond4lab.show()
window.enableButton.clicked.connect(addCond)

def remCond():  # button removing the 4th condition
    window.cond4.hide()
    window.cond4.setValue(0)
    window.cond4lab.hide()
window.disableButton.clicked.connect(remCond)

def showSettings():
    window.settingsBox.show()
window.settingsButton.clicked.connect(showSettings)

def saveSettings(): # function to update condition values with inputs, then closes the settings page
    window.conditionList[0] = str(window.cond1.value())  # str adjustment matches default
    window.conditionList[1] = str(window.cond2.value())
    window.conditionList[2] = str(window.cond3.value())

    if window.cond4.value() != 0:  # adding condition4 value to list, if other than 0
        window.conditionList.append(str(window.cond4.value()))

    window.settingsBox.hide()
window.saveButton.clicked.connect(saveSettings)


#CONSENT FORM FUNCTIONALITY

def consentChecker():
    consentC = window.consentCheck.isChecked()  #isChecked returns bool
    dataC = window.dataCheck.isChecked()
    withdrawC = window.withdrawCheck.isChecked()
    ageC = window.ageCheck.isChecked()

    # error conditions - all at once, as they are all checkboxes
    if consentC is False or dataC is False or withdrawC is False or ageC is False:
        errorLabel = QLabel(window.consentForm)  # creating an error popup within the consentForm only
        errorLabel.setGeometry(90, 700, 850, 50)
        errorLabel.setText("A required field is empty. Please fill it to continue!")
        errorLabel.show()
    else:  # proceeding to the demographics page if all fields are ticked
        proceed()
window.continueButton.clicked.connect(consentChecker)

#DEMOGRAPHICS PAGE FUNCTIONALITY

#initializing variables to be written to csv later
window.name = ""
window.age = ""
window.gender = ""
window.educ = ""

def pullDemographics():  # function to pull demographic page inputs
    window.name = window.nameInput.text().strip()
    window.age = window.ageSpin.value()

    for radio in window.sexGroup.children():  # changing gender to whichever radioButton is ticked
        if radio.isChecked():
            window.gender = radio.text()

    window.educ = window.educCheck.isChecked()  # returns bool value from checkbox

    # returning dict containing demographics - allows easier access, overwriting, and CSV writing
    return {"name": window.name, "age": window.age, "gender": window.gender, "education": window.educ}


# creating an error popup within the consentForm only
errorLabel = QLabel(window.demographics)
errorLabel.setGeometry(90, 700, 850, 50)
errorLabel.hide()

def demogChecker(values):

    errorLabel.show()  # allows it to update freely with different errors

    # using elif to create different error messages depending on missing value
    if values["name"] == "":
        errorLabel.setText("Error - missing Name. Please amend to continue.")
    elif values["age"] == 0:
        errorLabel.setText("Error - missing Age. Please amend to continue.")
    elif values["age"] != 0 and values["age"] < 18:
        errorLabel.setText("Error - invalid Age. Please amend to continue.")
    elif values["gender"] == "":
        errorLabel.setText("Error - missing Gender. Please amend to continue.")
    else:
        proceed()  # moving to the next page when no errors are present


def demogPageButton():
    # pulling and checking demographics for errors
    window.demos = pullDemographics()  # saving demograhics dictionary
    demogChecker(window.demos)

    # assigning the "random" urn and the condition, at random
    # has to be tied to the demographic page button, otherwise it runs too soon and defaults are kept
    randomUrn()
    randomCondition()
window.verifyButton.clicked.connect(demogPageButton)


#EXPERIMENT PAGE FUNCTIONALITY

window.randomUrn = ""  # initializing random urn

#function setting whether urn A or B is the urn with a random distribution of marbles
def randomUrn():
    promptText = window.briefLabel.text()  # pulling the base brief text from designer

    selector = randint(1, 2)
    if selector == 1:  # adjusting specific default substrings for randomUrn=A
        promptText = promptText.replace("Urn A contains 50 red marbles and 50 blue marbles", "Urn B contains 50 red marbles and 50 blue marbles")
        promptText = promptText.replace("Urn B contains marbles in an unknown color ratio", "Urn A contains marbles in an unknown color ratio")
        promptText = promptText.replace("Urn B has been decided", "Urn A has been decided")
        promptText = promptText.replace("to be put into Urn B", "to be put into Urn A")
        promptText = promptText.replace("in Urn B is equally likely", "in urn A is equally likely")

        window.randomUrn = "1"  # randomUrn = A
    else:
        None  # keeping default (randomUrn = B)
        window.randomUrn = "0"

    window.promptText = promptText  # updating label text with urn info


#function allocating condition at random
def randomCondition():
    window.currCondition = ""  # initialising current condition, making it "global"
    conditionAllocation = randint(1, len(window.conditionList))   # randomisation

    #setting current condition based on randomisation
    window.currCondition = window.conditionList[conditionAllocation-1]

    #changing text based on condition
    window.promptText = window.promptText.replace("100", window.currCondition)  # changing total figure
    window.promptText = window.promptText.replace("50", str(round(int(window.currCondition)/2)))  # changing half
                                                                                                  # figure and rounding

    #setting final label text to be viewed by participant
    window.briefLabel.setText(window.promptText)

#creating a label that emits a signal when clicked
class clickableUrn(QLabel):
    clicked = pyqtSignal()
    def mousePressEvent(self, mouseEvent): # customising pressEvent to emit a signal
        self.clicked.emit()

urn = QPixmap("urn.png") # creating a pixmap with the picture of the urn

urnList = ["Urn A", "Urn B"]

#creating clickable urns without function - they are just "A" and "B"
window.urnA = clickableUrn(window.briefPage)  # adding the left urn
window.urnA.setGeometry(235, 375, 400, 400)
window.urnA.setPixmap(urn)  # adding the urn image itself
window.urnA.setObjectName("Urn A")
window.urnA.setScaledContents(True)  # scaling


window.urnB = clickableUrn(window.briefPage)  # adding the right urn - same as above
window.urnB.setGeometry(835, 375, 400, 400)
window.urnB.setPixmap(urn)
window.urnB.setObjectName("Urn B")
window.urnB.setScaledContents(True)


# loading marble images as Pixmap
blueMarble = QPixmap("bluemarble.png")
redMarble = QPixmap("redmarble.png")

window.marblePic = QLabel(window.briefPage)  # creating the marble label, but blank for now
window.marblePic.setGeometry(640, 450, 200, 200)
window.marblePic.setScaledContents(True)


window.selectionLabel = QLabel(window.briefPage)
window.selectionLabel.setGeometry(640, 650, 300, 30)
window.selectionLabel.setText("Please click an urn.")

window.drawnMarble = ""  # initializing drawnMarble and selectedUrn window variables
window.selectedUrn = ""


def urnClick():  # function to select an urn and save the selection
    clickedObject = window.sender()
    clickedUrnName = clickedObject.objectName()  # pulling clicked urn name
    window.selectionLabel.setText(f"You have selected {clickedUrnName}.")  # changing label

    # adjusting global selected urn value based on urn assignment/selection
    if window.randomUrn == "1" and clickedUrnName == "Urn A":
        window.selectedUrn = "0"
    else:
        window.selectedUrn = "1"


for urn in window.findChildren(clickableUrn):  # assigning the above to urns
    urn.clicked.connect(urnClick)

aTimer = QTimer()  # initializing a timer

# function to actually draw the marble
def drawButtonFunc():
    if window.selectedUrn == "1":  # known distribution urn
        randomizer = randint(0, int(window.currCondition))  # "drawing" a marble
        if randomizer <= int(window.currCondition) / 2:  # halfway point, as .5 probability for both
            window.drawnMarble = "blue"  # adjusting global drawnMarble value
        else:
            window.drawnMarble = "red"

    else: # replicating Pulford paper method to decide random marble distribution
        blueMarbles = randint(0, int(window.currCondition))  # setting the number of blue marbles
        randomizer = randint(0, int(window.currCondition))  # pulling a marble at random
        if randomizer < blueMarbles:  # if the marble is within the blue marble range
            window.drawnMarble = "blue"
        else:  # if above that number (i.e., not within blue marble range), marble = RED
            window.drawnMarble = "red"

    # attaching relevant marble image depending on draw result
    if window.drawnMarble == "blue":
        window.marblePic.setPixmap(blueMarble)
    else:
        window.marblePic.setPixmap(redMarble)

    window.drawButton.hide()  # hiding button afterwards, so it can only be pressed once

    aTimer.timeout.connect(proceed)
    aTimer.setSingleShot(True)  # proceed() only runs once
    aTimer.start(4000)  # moving to the debrief page after 4 seconds

    #disabling clickable urns - "locking in" participant choice once a marble is drawn
    for urn in window.findChildren(clickableUrn):
        urn.setEnabled(False)

    #writing results to CSV
    csv.write(f"{window.name}, {window.age}, {window.gender}, {window.educ}, {window.currCondition}, {window.randomUrn}, {window.selectedUrn}, {window.drawnMarble} \n")
    csv.close()

window.drawButton.clicked.connect(drawButtonFunc)


#showing window, executing the program
window.show()
app.exec_()