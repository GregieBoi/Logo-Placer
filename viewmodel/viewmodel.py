from PyQt6.QtCore import QObject, pyqtSignal
from model.model import Model

class ViewModel(QObject):
    doSomething = pyqtSignal(str)
    
    def __init__(self, model: Model):
        super().__init__()
        self.model = model
        self.name = "ViewModel"

    def doSomethingFoo(self):
        self.doSomething.emit(self.model.name)