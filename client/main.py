import sys
import math
import time
from PyQt5 import QtGui, QtWidgets, QtCore#, QPainter

w = 0
z = 0
app = 0

def zzfunc():
  global z
  z = 0

class Qww(QtWidgets.QWidget):
  def __init__(self):
    super().__init__()
    self.resize(600, 800)
    self.initUI()
    self.setMouseTracking(True)

  def initUI(self):
    lb1 = QtWidgets.QLabel('zzz', self)
    lb1.move(10, 10)

    b1 = QtWidgets.QPushButton('Btn', self)
    global app
    b1.clicked.connect(lambda : app.quit())
    b1.setToolTip('This is <b> zzz </b>')
    b1.resize(b1.sizeHint())
    b1.move(100, 100)

    self.c1 = QtWidgets.QGraphicsView(self)
    self.c1.setGeometry(0, 0, 400, 400)
    sc = QtWidgets.QGraphicsScene()
    sc.setSceneRect(0, 0, 300, 300)
    self.c1.setScene(sc)
    sc.addLine(0, 0, 300, 500)

    self.c1.mouseMoveEvent = lambda e: sc.addLine(0, 0, e.x()-50, e.y()-50)

  def paintEvent(self, event):
    self.c1 = QtGui.QPainter()
    self.c1.begin(self)
    self.c1.drawLine(0, 0, 100, 100)
    self.c1.end()

    self.show()
    self.mousePressEvent = lambda e: self.c1.drawLine(-50, -50, e.x(), e.y())
    #self.mouseMoveEvent = lambda e: print(e.x(), e.y())


  def wow(self, e):
    self.setToolTip('wooowooowoo')
    print('WoooWoooWooooo')

#class myCanvas(QPainter):
  #pass

def func():
  a, r = 600, 200
  global z
  w.resize(a + r * math.sin(z*math.pi/100)
         , a + r * math.cos(z*math.pi/100))
  time.sleep(0.001)
  z += 1

def main():
  global app
  app = QtWidgets.QApplication(sys.argv)
  global w
  w = Qww()
  w.show()

  tm = QtCore.QTimer()
  tm.timeout.connect(func)
  tm.start(1)
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()
