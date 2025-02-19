import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6 import QtGui
from model.model import Model
from view.view import View
from viewmodel.viewmodel import ViewModel

styles = '''
QPushButton#destructiveButton {
  background-color: red; 
  color: white; 
  border-radius: 5px; 
  padding-top: 1px; 
  padding-bottom: 3px; 
  padding-left: 12px; 
  padding-right: 12px; 
  margin-bottom: 1px;
} 
QPushButton#destructiveButton:pressed {
  background-color: darkRed; 
  color: grey;
}
QPushButton#destructiveButton:disabled {
  background-color: darkred; 
  color: grey; 
}
'''

if __name__ == '__main__':
  app = QApplication(sys.argv)
  app.setStyleSheet(styles)
  app.setWindowIcon(QtGui.QIcon('icon.icns'))
  model = Model()
  viewModel = ViewModel(model)
  view = View(viewModel)
  view.show()
  sys.exit(app.exec())