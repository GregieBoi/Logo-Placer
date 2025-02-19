from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTabWidget
from PyQt6.QtCore import Qt
from viewmodel.viewmodel import ViewModel
from _widgets.labeled_button import LabeledButton
from _widgets.labeled_textedit import LabeledTextEdit
from _widgets.labeled_dropdown import LabeledDropdown
from _widgets.labeled_line_edit import LabeledLineEdit

class View(QWidget):
    def __init__(self, viewModel: ViewModel):
        super().__init__()
        self._viewModel = viewModel
        self._viewModel.doSomething.connect(self.doSomething)
        self.InitUi()

    def InitUi(self):
        self.setWindowTitle("Logo Placer")
        self.layout = QVBoxLayout()
        self.tabs = QTabWidget()
        self.tabs.addTab(self.InitLogoTab(), "Logos")
        self.tabs.addTab(self.InitGenerateTab(), "Generate")
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


    def InitLogoTab(self) -> QWidget:

        # initalize logo tab and its layout 
        self.LogoTab = QWidget()
        layout = QVBoxLayout()

        # layout the logo name and selection
        logoLayout = QHBoxLayout()
        self.logoName = LabeledLineEdit("Logo Name:", "Enter Logo Name")
        logoLayout.addWidget(self.logoName)
        self.selectedLogo = LabeledDropdown("Logo Select:", ["New Logo"] + sorted(self._viewModel.model.fetchLogoNames()))
        logoLayout.addWidget(self.selectedLogo)
        layout.addLayout(logoLayout)

        # layout the upload and position section
        pathLayout = QHBoxLayout()
        self.uploadLogo = LabeledButton("Logo:", "Upload")
        pathLayout.addWidget(self.uploadLogo)
        self.positionLogo = LabeledDropdown("Position:", ["Top Left", "Top Right", "Bottom Left", "Bottom Right"])
        pathLayout.addWidget(self.positionLogo)
        layout.addLayout(pathLayout)

        # layout the details sections
        detailsLayout = QHBoxLayout()
        detailsLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # layout the padding section
        paddingLayout = QVBoxLayout()
        self.paddingLabel = QLabel("Padding:")
        self.Xpadding = QLineEdit()
        self.Ypadding = QLineEdit()
        self.Xpadding.setPlaceholderText("0")
        self.Ypadding.setPlaceholderText("0")
        paddingLayout.addWidget(self.paddingLabel)
        paddingLayout.addWidget(self.Xpadding)
        paddingLayout.addWidget(self.Ypadding)
        detailsLayout.addLayout(paddingLayout)

        # layout the scale section
        scaleLayout = QVBoxLayout()
        scaleLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scaleLabel = QLabel("Scale:")
        self.scale = QLineEdit()
        self.scale.setPlaceholderText("1.0")
        scaleLayout.addWidget(self.scaleLabel)
        scaleLayout.addWidget(self.scale)
        detailsLayout.addLayout(scaleLayout)

        # layout the image resoultion section
        resolutionLayout = QVBoxLayout()
        self.resolutionLabel = QLabel("Resolution:")
        self.Xresolution = QLineEdit()
        self.Yresolution = QLineEdit()
        self.Xresolution.setPlaceholderText("1280")
        self.Yresolution.setPlaceholderText("720")
        resolutionLayout.addWidget(self.resolutionLabel)
        resolutionLayout.addWidget(self.Xresolution)
        resolutionLayout.addWidget(self.Yresolution)
        detailsLayout.addLayout(resolutionLayout)

        # add the details section to the layout
        layout.addLayout(detailsLayout)

        # layout the button section
        buttonLayout = QHBoxLayout()
        self.testLogoButton = QPushButton("Test Configuration")
        self.testLogoButton.clicked.connect(self.testLogoButtonClicked)
        buttonLayout.addWidget(self.testLogoButton)
        self.saveLogoButton = QPushButton("Save Logo")
        self.saveLogoButton.clicked.connect(self.saveLogoButtonClicked)
        buttonLayout.addWidget(self.saveLogoButton)
        self.deleteLogoButton = QPushButton("Delete Logo")
        self.deleteLogoButton.setObjectName("destructiveButton")
        self.deleteLogoButton.clicked.connect(self.deleteLogoButtonClicked)
        buttonLayout.addWidget(self.deleteLogoButton)
        layout.addLayout(buttonLayout)

        # set the final layout
        self.LogoTab.setLayout(layout)

        return self.LogoTab

    def InitGenerateTab(self) -> QWidget:
        self.GenerateTab = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # add the layout for the image upload and logo selection
        logoLayout = QHBoxLayout()
        self.imagesUpload = LabeledButton("Image(s):", "Upload")
        self.imagesUpload.clicked.connect(self.uploadImagesButtonClicked)
        self.logoSelection = LabeledDropdown("Logo:", sorted(self._viewModel.model.fetchLogoNames()))
        logoLayout.addWidget(self.imagesUpload)
        logoLayout.addWidget(self.logoSelection)
        layout.addLayout(logoLayout)

        # add the button to the layout
        self.generateButton = QPushButton("Generate")
        self.generateButton.clicked.connect(self.generateButtonClicked)
        layout.addWidget(self.generateButton)

        # add the layout to the tab
        self.GenerateTab.setLayout(layout)

        return self.GenerateTab
    
    def generateButtonClicked(self):
        pass

    def uploadImagesButtonClicked(self):
        pass
    
    def testLogoButtonClicked(self):
        pass

    def saveLogoButtonClicked(self):
        pass

    def deleteLogoButtonClicked(self):
        pass

    def doSomething(self, text):
        self.label.setText(text)