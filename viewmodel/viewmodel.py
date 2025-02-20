from PyQt6.QtCore import QObject, pyqtSignal
from model.model import Model
from PIL import Image

class ViewModel(QObject):
    logoLoaded = pyqtSignal(object)
    fetchedLogoNames = pyqtSignal(list)
    savedLogo = pyqtSignal(list)
    deletedLogo = pyqtSignal(list)
    testedLogo = pyqtSignal(Image.Image)
    logoized = pyqtSignal(bool)
    
    def __init__(self, model: Model):
        super().__init__()
        self.model = model
        self.name = "ViewModel"

    def fetchLogoNames(self):
        self.fetchedLogoNames.emit(self.model.fetchLogoNames())

    def loadLogo(self, name: str):
        self.logoLoaded.emit(self.model.loadLogo(name))

    def saveLogo(self, name: str, path: str, position: str, padding: list[int], scale: float, resolution: list[int]):
        self.savedLogo.emit(self.model.saveLogo(name, path, position, padding, scale, resolution))

    def deleteLogo(self, name: str):
        self.deletedLogo.emit(self.model.deleteLogo(name))

    def handleTestLogoization(self, testPath: str, testPosition: str, testPadding: list[int], testScale: float, testResolution: list[int]):
        self.testedLogo.emit(self.model.handleTestLogoization(testPath, testPosition, testPadding, testScale, testResolution))

    def handleLogoization(self, logoName: str, images: list[str], saveDesination: str):
        self.logoized.emit(self.model.handleLogoization(logoName, images, saveDesination))