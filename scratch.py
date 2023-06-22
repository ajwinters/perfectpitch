import sys
from PyQt5.QtCore import *
from PyQt5.QtGui  import *
from PyQt5.QtWidgets import *

class mainb(QPushButton):
    def __init__(self, Text, parent = None):
        super(mainb, self).__init__()
        self.setupbt(Text)

    def setupbt(self, Text):
        self.setText(Text)
        self.setGeometry(200,100, 60, 35)
        self.move(300,300)
        print('chegu aqui')
        self.setToolTip('Isso muito maneiro <b>Artur</b>')
        self.show()


class mainwindow(QWidget):
    def __init__(self , parent = None):
        super(mainwindow, self).__init__()    
        self.setupgui()
    def setupgui(self):
        self.setToolTip('Oi <i>QWidget</i> widget')       
        self.resize(800,600)
        self.setWindowTitle('Janela do Artur')
        newLayout = QHBoxLayout()
        af = mainb("Bom dia",self)
        newLayout.addWidget(af)
        self.setLayout(newLayout)
        self.show()


def main():

    app = QApplication(sys.argv)
    ex = mainwindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()