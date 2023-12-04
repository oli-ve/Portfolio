import pandas as pd
import numpy as np
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from random import *
from os import listdir
from returnHome import *
from re import *
from addBook import *

# opening window, loading UI file
app = QApplication([])
window = uic.loadUi("library.ui")
fileList = listdir()
window.libStack.setCurrentIndex(0)

def resetBoxes(container):
    c = container
    for textbox in c.children():
        textbox.setText("")

# creating dataframe to store books if not already present

if "books.csv" in fileList:
    bookdf = pd.read_csv("books.csv") #reading in file if present
else: #creating the dataframe file if not present / adding default values for testing
    bookdf = pd.DataFrame([{
                        "Title": "David Fincher Interviews",
                        "Author": "Laurence Knapp",
                        "Year of Release": "2014",
                        "Library ID Code": "1"},
        {"Title": "Stella Maris",
                        "Author": "Cormac McCarthy",
                        "Year of Release": "2022",
                        "Library ID Code": "2"}]) # input - list of dictionaries

    #saving
    bookdf.to_csv("books.csv", sep=",", index=False)


#main page UI buttons

window.goHomeButton = navigationButton(window)
window.goHomeButton.setText("Return Home")
window.goHomeButton.linkToStack(window.libStack)
window.goHomeButton.setGeometry(730, 720, 91, 24)

window.searchPageButton = navigationButton(window.homePage)
window.searchPageButton.setText("Search for a book")
window.searchPageButton.linkToStack(window.libStack)
window.searchPageButton.setGeometry(670, 270, 221, 71)

window.addBookButton = navigationButton(window.homePage)
window.addBookButton.setText("Add a new book")
window.addBookButton.linkToStack(window.libStack)
window.addBookButton.setGeometry(670, 360, 221, 71)

#viewing a book functionality

def bookSearch():
    toSearch = window.enterID.text() #pulling the content of the lineEdit
    a=""
    y=""
    l=""

    if toSearch == None or toSearch == "":
        a = "Please enter a valid ID or title."
    elif toSearch.isdigit() == False: #searching based on title
        a = bookdf.where(bookdf['Title'] == toSearch)["Author"].dropna().to_string()
        y = bookdf.where(bookdf['Title'] == toSearch)["Year of Release"].dropna().to_string()
        l = bookdf.where(bookdf['Title'] == toSearch)["Library ID Code"].dropna().to_string()
    elif toSearch.isdigit() == True: #alternatively searching based on ID number
        a = bookdf.where(bookdf['Library ID Code'] == toSearch)["Title"].dropna().to_string()
        y = bookdf.where(bookdf['Library ID Code'] == toSearch)["Year of Release"].dropna().to_string()
        l = bookdf.where(bookdf['Library ID Code'] == toSearch)["Author"].dropna().to_string()

    window.outputLabel.setText(a)
    window.outputLabel_2.setText(y)
    window.outputLabel_3.setText(l)


window.searchButton.clicked.connect(bookSearch)


#"add a book" functionality

def addABook():
    toAdd = {"Title": "", #initialising new dictionary to add to df, blank values
    "Author": "",
    "Year of Release": 0,
    "Library ID Code": ""}
    outputTxt = ""

    t = window.nameEntry.text() #can probably optimise this! check old projects for examples
    y = window.yearEntry.text()
    a = window.authorEntry.text()

    lst = [t, a, y]
    #creating new id code - pulling previous entry and adding 1
    newid = int(bookdf["Library ID Code"][len(bookdf)-1]) + 1

    #adding inputs to new row dictionary
    if None in lst or "" in lst:
        outputTxt = "Please ensure all of the entered details are accurate."
    else:
        toAdd["Title"] = t
        toAdd["Author"] = a
        toAdd["Year of Release"] = y 
        toAdd["Library ID Code"] = str(newid)
        outputTxt = "Entry successfully added!"

    #appending the new row/setting output label
    bookdf.loc[len(bookdf)] = toAdd
    window.hiddenLab.setText(outputTxt)

    #resetting text boxes/saving csv
    resetBoxes(window.addInputGroup)
    bookdf.to_csv("books.csv", sep=",", index=False)
    

window.addButton.clicked.connect(addABook)

# showing window, executing the program
window.show()
app.exec_()