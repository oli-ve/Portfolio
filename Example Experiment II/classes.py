from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from random import *
from os import listdir
from time import *

## THIS FILE CONTAINS ALL CUSTOM CLASSES USED IN THE PARADIGM ##


##########################################################
# a custom class to fulfil image response needs.
# functionality includes randomising image with keypress and altering UI elements
#########################################################
class imageDisplayWidget(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)  # calling superclass constructor
        self.allResponses = []  # list of all responses
        self.recentResponse = None  # most recent participant response
        self.imageDir = listdir("images")  # pulling list of images - add additional images to this file
        self.reactionTimes = []


    def linkObjects(self, labelToLink, aTimer, posLabel, negLabel):  # method that allows relevant widgets and
        self.timer = aTimer                                          # variables to be linked to the class
        self.label = labelToLink
        self.posL = posLabel
        self.negL = negLabel


    def setImage(self):  # method to set image until there are no more unique images to use

        if len(self.imageDir) == 0:  # disabling further response/moving on when all images viewed
            self.setEnabled(False)
            self.label.setGeometry(350, 10, 1000, 100)
            self.label.setFont(QFont("Arial", 10))
            self.label.setText("Thank you for responding to all of the images. The next part of the experiment will begin in 5 seconds.")
            self.timer.start(5000)


        else:
            randPic = choice(self.imageDir)  # randomly selecting image
            aPix = QPixmap(f"images\{randPic}")
            self.setPixmap(aPix)
            self.imageDir.remove(randPic)  # removing "used" pictures



    def keyPressEvent(self, keyEvent): # events both emit signal and record response
        if keyEvent.text() == "j":
            self.recentResponse = "positive"
        elif keyEvent.text() == "f":
            self.recentResponse = "negative"
        else:
            None # other key presses do nothing

        if keyEvent.text() == "j" or keyEvent.text() == "f":
            self.label.show()
            self.label.setText(self.recentResponse)  # updating label text
            self.setImage()  # updating image on keypress
            self.labColourChange()  # updating label colours
            self.allResponses.append(self.recentResponse)  # saving response
        else:
            None  # necessary so that other, possibly accidental, key presses don't trigger the next
                  # image too early

    def labColourChange(self): # method changing the instruction label colour
        if self.recentResponse == "positive":
            self.negL.setStyleSheet("color: black;")
            self.posL.setStyleSheet("color: red;")
        elif self.recentResponse == "negative":
            self.negL.setStyleSheet("color: red;")
            self.posL.setStyleSheet("color: black;")

#####################################
# a simple clickable label
####################################
class clickableLabel(QLabel):
    clicked = pyqtSignal()
    def mousePressEvent(self, mouseEvent): # customising pressEvent to emit a signal
        self.clicked.emit()

#########################
# a label with adjustable pixmap capable of animation
#########################
class animatedLabel(QLabel):
    def __init__(self, image, parent=None):
        super().__init__(image, parent)

        self.setPixmap(QPixmap(image))  # setting pixmap to the image called in constructor
        self.setScaledContents(True)   # setting scaled contents

        self.destination = 0

        #establishing how large we want each step to be
        self.stepSizeX = 0

        self.timer = QTimer()
        self.timer.timeout.connect(self.animationFunc)  # timer loops the movement repeatedly
        self.timer.start(27)  # timer begins internally, meaning that any external call will need to
                              # change step size to make the animation "start"

    def linkButton(self, button):
        self.aButton = button

    def animationFunc(self):
        self.parentGeom = self.parent().geometry()
        self.currentGeom = self.geometry()
        nextX = self.currentGeom.x()
        nextY = self.currentGeom.y()

        if self.stepSizeX != 0:
            nextX += self.stepSizeX

        self.setGeometry(nextX, nextY, self.currentGeom.width(), self.currentGeom.height())

        # returning label to original position if exceeding window
        if nextX > self.parentGeom.width():
            self.setGeometry(860, 750, 100, 50)
            self.stepSizeX = 0

        if self.currentGeom.x() != 860:
            self.aButton.setEnabled(False)
        elif self.currentGeom.x() == 860:
            self.aButton.setEnabled(True)

    #method to start animation at a certain speed
    def startAnimation(self, speed):
        self.stepSizeX = speed

