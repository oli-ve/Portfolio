from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from random import *
from os import listdir
from time import *
from classes import *
from functions import *

app = QApplication([])
window = uic.loadUi("mazeparadigm.ui")
window.mainStack.setCurrentIndex(0)  # ensuring experiment begins on the first page
fileList = listdir()
imageList = listdir("images")

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
    csv.write("Name, Age, Gender, Education, Walk Comfort, Walk Frequency, Walk Fear, P1, P2, P3, P4, P5, Number of Trials, Rural Rate, Rural Loss Chance, City Rate, City Loss Chance, Motorway Rate, Motorway Loss Chance, N1, N2, N3, N4, Total Score  \n")
else:
    csv.close()
    csv = open("results.csv", "a")

#MISC
window.currStackIndex = 0  # initialising stacked widget index
def proceed():
    window.currStackIndex += 1
    window.mainStack.setCurrentIndex(window.currStackIndex)  # modifying stackwidget index

# SETTINGS BOX / LABEL CHANGING
window.password = "admin123"  # password to access experimenter settings box
window.passwordIndex = 0
window.passwordError = QLabel(window.login)  # error label
window.passwordError.setGeometry(30, 180, 300, 40)
window.settingsBox.hide()

#initialising navigation game variables
window.rates = [75, 0.4, 40, 0.15, 125, 0.75]  # speed and losschance by default
window.numberOfTrials = str(window.trialSpin.value())  # saving default number of trials

#funciton that shows settings box
def showSettings():
    window.settingsBox.show()

#try adding window and widget as arguments
def settingsBoxLogin():  # function to check password, return error
    inputPW = window.pwBox.text()
    if inputPW == window.password:
        window.passwordIndex += 1
        window.settingsBox.setCurrentIndex(window.passwordIndex)
    else:
        window.passwordError.setText("Wrong password. Please try again.")
        window.passwordError.show()


def saveSettings():  # function updating values with inputs, then closes the settings page
    labelList = window.mazePage.findChildren(QLabel)
    for label in labelList:
        label.setAlignment(Qt.AlignCenter)

    #saving rate values in the container
    window.rates[0] = window.ruralSpeed.value()
    window.rates[1] = window.ruralLoss.value()
    window.rates[2] = window.citySpeed.value()
    window.rates[3] = window.cityLoss.value()
    window.rates[4] = window.motorwaySpeed.value()
    window.rates[5] = window.motorwayLoss.value()

    #saving number of trials
    window.numberOfTrials = window.trialSpin.value()

    #modifying navigation brief label
    modifyBriefLabel(window, window.brief, "1", str(window.numberOfTrials))

    #modifying other information labels on the navigation game page
    window.ruralLabel.setText(f"Rural Route: \n"
                              f"\n"
                              f"Journey Speed = {window.rates[0]} \n"
                              f"Loss chance = {window.rates[1]*100}%")  # *100 necessary to display
                                                                        # percentages
    window.cityLabel.setText(f"City Route: \n"
                             f"\n"
                              f"Journey Speed = {window.rates[2]} \n"
                              f"Loss chance = {window.rates[3]*100}%")

    window.motorwayLabel.setText(f"Motorway Route: \n"
                                 f"\n"
                              f"Journey Speed = {window.rates[4]} \n"
                              f"Loss chance = {window.rates[5]*100}%")


    window.settingsBox.hide()


window.settingsButton.clicked.connect(showSettings)
window.logButton.clicked.connect(settingsBoxLogin)
window.saveButton.clicked.connect(saveSettings)

#CONSENT FORM

def consentPageButton():
    states = []
    for checkbox in window.consentForm.findChildren(QCheckBox):  # searching through all boxes
        states.append(checkbox.isChecked()) # returns bool - false if unchecked

    if False in states:
        errorLabel = QLabel(window.consentForm)  # creating an error popup within the consentForm only
        errorLabel.setGeometry(90, 700, 850, 50)
        errorLabel.setText("A required field is empty. Please fill it to continue!")
        errorLabel.show()
    else:
        proceed()
window.continueButton.clicked.connect(consentPageButton)
window.continueButton.clicked.connect(saveSettings) # needs to save settings to ensure at least defaults
                                                    # are saved


#DEMOGRAPHICS PAGE / SELF-REPORT

#initializing variables to be written to csv later
window.name = ""
window.age = ""
window.gender = ""
window.educ = ""

window.responses = []  # the self-report responses are saved to this container

# creating an error popup within the consentForm only
errorLabel = QLabel(window.demographics)
errorLabel.setGeometry(90, 700, 850, 50)
errorLabel.hide()

def demogPageButton():
    # pulling and checking demographics for errors
    window.demos = pullDemographics(window)  # saving demograhics dictionary
    demogChecker(window, window.demos, errorLabel)
window.verifyButton.clicked.connect(demogPageButton)

window.moveOnTimer = QTimer()  # creating a timer to automatically move on from instructions
window.moveOnTimer.timeout.connect(proceed)
window.moveOnTimer.setSingleShot(True)

def selfReportChecker():
    responses = pullSelfReport(window)
    if len(responses) != 3:
        window.demErrorLab.setText("Please respond to all of the questions.")
    else:
        proceed() # moving TO the instructions page
        window.moveOnTimer.start(15000)  # starting the timer to move on FROM instructions page

window.continueButton2.clicked.connect(selfReportChecker)

#IMAGE DISPLAY PAGE
#see "classes" for display functionality

window.feedBackLabel = QLabel(window.imagePage)  # a label for instructions/feedback
window.feedBackLabel.setGeometry(715, 15, 150, 40)
window.feedBackLabel.setFont(QFont("Arial", 18))

window.imageDisplay = imageDisplayWidget(window.imagePage)  # image display
window.imageDisplay.setGeometry(400, 85, 800, 600)
window.imageDisplay.setScaledContents(True)
window.imageDisplay.setImage() # setting initial image at random
window.imageDisplay.setFocus()  # setting focus so that keypresses register
window.imageDisplay.linkObjects(window.feedBackLabel, window.moveOnTimer, window.JLabel, window.FLabel)

#NAVIGATION GAME PAGE

window.navGameResults = []  # list of game results
window.routeChoices = []  # list of routes chosen
window.clickedObjName = ""  # the most recent object clicked
window.totalScore = 0  # running tally of speeds, forming score


#adding the three route labels, naming, setting geom, and setting pixmap
window.ruralRoute = clickableLabel(window.mazePage)
window.ruralRoute.setObjectName("Rural Route")
window.ruralRoute.setGeometry(350,190,200,200)
window.ruralRoute.setPixmap(QPixmap("gameImages/ruralroad.jpg"))

window.cityRoute = clickableLabel(window.mazePage)
window.cityRoute.setGeometry(650,190,200,200)
window.cityRoute.setObjectName("City Route")
window.cityRoute.setPixmap(QPixmap("gameImages/cityroad.jpg"))

window.motorwayRoute = clickableLabel(window.mazePage)
window.motorwayRoute.setGeometry(950,190,200,200)
window.motorwayRoute.setObjectName("Motorway Route")
window.motorwayRoute.setPixmap(QPixmap("gameImages/motorway.jpg"))

def routeChoose():  # function allowing participants to choose the route

    #route choose
    clickedObject = window.sender()
    window.clickedObjName = clickedObject.objectName()  #saving name of clicked object

    window.feedback.setText(f"You have selected the {window.clickedObjName}")

for routeLabel in window.findChildren(clickableLabel):
    routeLabel.show()
    routeLabel.setScaledContents(True)
    routeLabel.clicked.connect(routeChoose)

#adding the car avatar to the window, off-screen
window.carAvatar = animatedLabel("car.png", window.mazePage)
window.carAvatar.setGeometry(860, 750, 100, 50)  # car begins moving from off-screen
window.carGeom = window.carAvatar.geometry()
window.carAvatar.linkButton(window.beginJourneyButton)
window.carAvatar.show()

def verifyChoice():  # function operating the button for the navigation game
    successfulness = calculateSuccess(window, window.clickedObjName, window.rates)
    window.totalScore += successfulness
    propSpeed = int(successfulness / 10)  # a proportional step size for animations
    window.carAvatar.startAnimation(propSpeed)

    window.navGameResults.append(successfulness)  # adding successfulness to a list
    window.routeChoices.append(window.clickedObjName)  # adding choice to a list

    #updating label based on calculateSuccess output
    if window.lost == True:
        window.pointsFig.setText("You got lost!")
    elif window.lost == False:
        window.pointsFig.setText("You made it!")

    #moving on when trialNo has been reached and animation has finished
    if len(window.navGameResults) == window.numberOfTrials:
        proceed()
        modifyBriefLabel(window, window.finalLabel, "xxx", str(window.totalScore))  # modifying final page label

window.beginJourneyButton.clicked.connect(verifyChoice)


#WRITING TO CSV
def writeFinalResults():
    csv.write(f"{window.name}, {window.age}, {window.gender}, {window.educ}, {window.responses[0]}, {window.responses[1]}, {window.responses[2]}, {window.imageDisplay.allResponses[0]}, {window.imageDisplay.allResponses[1]}, {window.imageDisplay.allResponses[2]}, {window.imageDisplay.allResponses[3]}, {window.imageDisplay.allResponses[4]}, {window.numberOfTrials}, {window.rates[0]}, {window.rates[1]}, {window.rates[2]}, {window.rates[3]}, {window.rates[4]}, {window.rates[5]}, {window.routeChoices[0]}, {window.routeChoices[1]}, {window.routeChoices[2]}, {window.routeChoices[3]}, {window.totalScore} \n")
    csv.close()
    window.close() # closing the window on button press
window.closeButton.clicked.connect(writeFinalResults)

#showing window, executing the program
window.show()
app.exec_()