from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from viewmodel.viewmodel import ViewModel

class View(QWidget):
    def __init__(self, viewModel: ViewModel):
        super().__init__()
        self._viewModel = viewModel
        self._viewModel.doSomething.connect(self.doSomething)
        self.InitUi()

    def InitUi(self):
        self.setWindowTitle("Logo Placer")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.label = QLabel("Hellow World")
        self.layout.addWidget(self.label)
        self.QPushButton = QPushButton("Do Something")
        self.QPushButton.clicked.connect(self._viewModel.doSomethingFoo)
        self.layout.addWidget(self.QPushButton)

    def doSomething(self, text):
        self.label.setText(text)