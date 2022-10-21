import sys
from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi("TOL.ui",self)
        self.button.clicked.connect(self.gotoInstructions)

    def gotoInstructions(self):
        instructions = Instructions()
        widget.addWidget(instructions)
        widget.setCurrentIndex(widget.currentIndex()+1)

class Instructions(QDialog):
    def __init__(self):
        super(Instructions,self).__init__()
        loadUi("Instructions.ui",self)
        self.button.clicked.connect(self.gotoMainWindow)

    def gotoMainWindow(self):
        mainwindow = MainWindow()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)

# main
app = QApplication(sys.argv)
widget=QtWidgets.QStackedWidget()
widget.setFixedHeight(480)
widget.setFixedWidth(800)
widget.show()

try:
    sys.exit(app.exec_())
except:
    print("Exiting")
    

#PH
        rngPH = random.uniform(2.0,12.0)
        print(rngPH)
        count = 0
        for i in treeListFull:
            if rngPH > phMax[count]:
                tempTree = treeListFull[phMax.index(phMax[count])]
                for j in treeList:
                    if j == tempTree:
                        treeList.remove(j)
            if rngPH < phMin[count]:
                tempTree = treeListFull[phMin.index(phMin[count])]
                for j in treeList:
                    if j == tempTree:
                        treeList.remove(j)           
            count+=1
        print(len(treeList))