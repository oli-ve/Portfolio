from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from random import *
from os import listdir
from time import *

## THIS FILE CONTAINS ALL THE CUSTOM FUNCTIONS USED IN THE PARADIGM ##

#############################################
# Function that pulls values from widgets and returns a demographics dictionary
#############################################
def pullDemographics(window):  # function to pull demographic page inputs
    window.name = window.nameInput.text().strip()
    window.age = window.ageSpin.value()

    for radio in window.sexGroup.children():  # changing gender to whichever radioButton is ticked
        if radio.isChecked():
            window.gender = radio.text()

    window.educ = window.educCheck.isChecked()  # returns bool value from checkbox

    # returning dict containing demographics - allows easier access, overwriting, and CSV writing
    return {"name": window.name, "age": window.age, "gender": window.gender, "education": window.educ}


##############################################
# Function that checks a demographics dictionary and returns an error message if present
##############################################
def demogChecker(window, values, error):
    errorDisplay = error
    errorDisplay.show()  # allows it to update freely with different errors

    # using elif to create different error messages depending on missing value
    if values["name"] == "":
        errorDisplay.setText("Error - missing Name. Please amend to continue.")
    elif values["age"] == 0:
        errorDisplay.setText("Error - missing Age. Please amend to continue.")
    elif values["age"] != 0 and values["age"] < 18:
        errorDisplay.setText("Error - Age cannot be lower than 18. Please amend to continue.")
    elif values["gender"] == "":
        errorDisplay.setText("Error - missing Gender. Please amend to continue.")
    else:
        window.currStackIndex += 1
        window.mainStack.setCurrentIndex(window.currStackIndex)  # modifying stackwidget index

###############################
# Function that pulls self-report responses from radiobuttons
###############################
def pullSelfReport(window):
    #experimental, avoiding repetition
    for box in window.questionsCont.findChildren(QGroupBox): # cycling through boxes
        for radio in box.children():  # cycling through buttons
            if radio.isChecked():  # pulling selected responses
                window.responses.append(radio.text())
    return window.responses

##############################################
# function that computes route length (in accordance with game rules) for different routes
##############################################
def calculateSuccess(window, chosenRoute, container):  # container structured as journeySpeed and lossChance for each of the three routes
    container = container
    journeyLength = 0
    lossChance = 0  # the chance of getting lost on the route
    rand = float(random())  # a random float value between 0-1

    journeySpeed = 0 #
    lossChance = 0
    totalTime = 0  # the length their chosen journey takes

    #setting values for total time calculation based on choice
    if chosenRoute == "Rural Route":
        journeySpeed = container[0]
        lossChance = container[1]
    elif chosenRoute == "City Route":
        journeySpeed = container[2]
        lossChance = container[3]
    elif chosenRoute == "Motorway Route":
        journeySpeed = container[4]
        lossChance = container[5]


    #success calculation
    if rand < lossChance:
        totalTime = journeySpeed / 2  # half speed if lost = true
        window.lost = True
    else:
        totalTime += journeySpeed
        window.lost = False


    return totalTime

###############################
# function that replaces label elements
###############################
def modifyBriefLabel(window, label, oldStr="", newStr=""):
    label = label
    old = oldStr  # the string that needs replacing
    new = newStr  # the string we are replacing it with

    text = label.text()
    text = text.replace(oldStr, newStr)
    label.setText(text)





