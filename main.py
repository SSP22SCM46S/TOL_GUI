import sys
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication
import pandas as pd
import openpyxl
import random
import math
from PyQt5.QtGui import QMovie
import time
import board
import busio
import adafruit_scd30

# SCD-30 has tempremental I2C with clock stretching, datasheet recommends
# starting at 50KHz
i2c = busio.I2C(board.SCL, board.SDA, frequency=50000)
scd = adafruit_scd30.SCD30(i2c)


#initialize starting tree list
df = pd.read_csv("PLANTS_Characteristics_Data.csv")

treeListFull = list(df.SCINAME)
treeList = list(df.SCINAME)
print(len(treeList))
tempTol = list(df.TEMP_TOLR_MIN_RNG)
phMin = list(df.SOIL_PH_TOLR_MIN_RNG)
phMax = list(df.SOIL_PH_TOLR_MAX_RNG)

#initialize zipcode to zone
df = pd.read_csv("zipcode_to_zone.csv")

zipCol = list(df.zipcode)
zoneCol = list(df.zone)

#initialize optimal tree list
df = pd.read_csv("optimalTrees.csv")

optimalTrees = list(df.Optimal_Trees)

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi("TOL.ui",self)
        self.pushButton.clicked.connect(self.gotoInstructions)

    def gotoInstructions(self):
        instructions = Instructions()
        widget.addWidget(instructions)
        widget.setCurrentIndex(widget.currentIndex()+1)

class Instructions(QDialog):
    def __init__(self):
        super(Instructions,self).__init__()
        loadUi("Instructions.ui",self)
        self.continue_button.clicked.connect(self.gotoZipcode)

    def gotoZipcode(self):
        zipcode = Zipcode()
        widget.addWidget(zipcode)
        widget.setCurrentIndex(widget.currentIndex()+1)

class Zipcode(QDialog):
    def __init__(self):
        super(Zipcode,self).__init__()
        loadUi("Zipcode.ui",self)
        self.enter_button.clicked.connect(self.updateZone)

    def updateZone(self):
        zipcodeVal = int(self.lineEdit.text())
        hardZone = zoneCol[zipCol.index(zipcodeVal)]
        
        #get rid of trees not in hardiness zone
        count = 0
        for i in treeList:
            if hardZone == "3a" and tempTol[count] < -40.0:
                treeList.remove(i)
            elif hardZone == "3b" and tempTol[count] < -35.0:
                treeList.remove(i)
            elif hardZone == "4a" and tempTol[count] < -30.0:
                treeList.remove(i)
            elif hardZone == "4b" and tempTol[count] < -25.0:
                treeList.remove(i)
            elif hardZone == "5a" and tempTol[count] < -20.0:
                treeList.remove(i)
            elif hardZone == "5b" and tempTol[count] < -15.0:
                treeList.remove(i)
            elif hardZone == "6a" and tempTol[count] < -10.0:
                treeList.remove(i)
            elif hardZone == "6b" and tempTol[count] < -5.0:
                treeList.remove(i)
            elif hardZone == "7a" and tempTol[count] < -0.0:
                treeList.remove(i)
            elif hardZone == "7b" and tempTol[count] < 5.0:
                treeList.remove(i)
            elif hardZone == "8a" and tempTol[count] < 10.0:
                treeList.remove(i)
            elif hardZone == "8b" and tempTol[count] < 15.0:
                treeList.remove(i)
            elif hardZone == "9a" and tempTol[count] < 20.0:
                treeList.remove(i)
            elif hardZone == "9b" and tempTol[count] < 25.0:
                treeList.remove(i)
            elif hardZone == "10a" and tempTol[count] < 30.0:
                treeList.remove(i)
            elif hardZone == "10b" and tempTol[count] < 35.0:
                treeList.remove(i)
            elif hardZone == "11a" and tempTol[count] < 40.0:
                treeList.remove(i)
            elif hardZone == "11b" and tempTol[count] < 45.0:
                treeList.remove(i)
            elif hardZone == "11a" and tempTol[count] < 50.0:
                treeList.remove(i)
            elif hardZone == "11b" and tempTol[count] < 55.0:
                treeList.remove(i)
            count+=1
        print(len(treeList))
        self.continue_button.clicked.connect(self.gotoFinalTree)
    def gotoFinalTree(self):
        finalTree = FinalTree()
        widget.addWidget(finalTree)
        widget.setCurrentIndex(widget.currentIndex()+1)

class FinalTree(QDialog):
    def __init__(self):
        super(FinalTree,self).__init__()
        loadUi("FinalTree.ui",self)

        self.results.setVisible(False)
        self.co2.setVisible(False)
        self.NPK.setVisible(False)
        self.PH.setVisible(False)
        self.camera.setVisible(False)

        # Loading the GIF
        self.movie = QMovie("loading.gif")
        self.loading1.setMovie(self.movie)
        self.loading2.setMovie(self.movie)
        self.loading3.setMovie(self.movie)
        self.loading4.setMovie(self.movie)
  
        self.movie.start()
        #self.movie.stop()

        #NPK
        #self.loading1.setVisible(False)
        #self.NPK.setVisible(True)

        #PH
        rngPH = round(random.uniform(3.0,11.0), 2)     
        count = 0
        for i in treeListFull:
            avgPH = (phMax[count] + phMin[count])/2.0
            if math.isclose(avgPH, rngPH, abs_tol = 0.01)==False:
                tempTree = treeListFull[phMax.index(phMax[count])]
                for j in treeList:
                    if j == tempTree:
                        treeList.remove(j)
            count+=1
        
        self.loading2.setVisible(False)
        self.PH.setVisible(True)

        #camera analyisis
        #self.loading3.setVisible(False)
        #self.camera.setVisible(True)

        #CO2
        co2ppm = 780
        if scd.data_available:
            co2ppm = round(scd.CO2, 2)
        self.loading3.setVisible(False)
        self.co2.setVisible(True)

        finalTreeList = []
        for i in range(len(treeList)):
            if treeList[i] in optimalTrees:
                finalTreeList.append(treeList[i])
        
        count = 0
        while len(finalTreeList) < 5:
            finalTreeList.append(treeList[count])
            count+=1

        n = 5
        topFive = random.choices(finalTreeList, k=n)

        self.analyzing.setVisible(False)
        self.results.setVisible(True)
        self.tree1.setText(topFive[0])
        self.tree2.setText(topFive[1])
        self.tree3.setText(topFive[2])
        self.tree4.setText(topFive[3])
        self.tree5.setText(topFive[4])

        self.co2.setText(str(co2ppm)+"ppm")
        self.PH.setText(str(rngPH))


        self.upload_button.clicked.connect(self.gotoLogin)
    def gotoLogin(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)


class Login(QDialog):
    def __init__(self):
        super(Login,self).__init__()
        loadUi("Login.ui",self)

        self.login_suc.setVisible(False)
        



# main
app = QApplication(sys.argv)
widget=QtWidgets.QStackedWidget()
mainwindow = MainWindow()

widget.addWidget(mainwindow)

widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")