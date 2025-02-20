from PyQt6.QtWidgets import QSizePolicy,QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

class ImageModal(QDialog):
  def __init__(self, logo_name: str, image : QPixmap , parent=None):
    super().__init__()
    self.logo_name = logo_name
    self.image = image
    self.initUI()

  def initUI(self):
    self.setWindowTitle('Test ' + self.logo_name)
    self.setWindowModality(Qt.WindowModality.ApplicationModal)
    self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

    self.layout = QVBoxLayout()
    self.layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
    
    self.imageLabel = QLabel()
    self.imageLabel.setPixmap(self.image)

    self.layout.addWidget(self.imageLabel, stretch=100)

    self.setLayout(self.layout)