from PyQt6.QtWidgets import QWidget, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QLineEdit, QPushButton, QTabWidget, QFileDialog
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QImage, QPixmap, QIntValidator, QDoubleValidator
from viewmodel.viewmodel import ViewModel
from _widgets.labeled_button import LabeledButton
from _widgets.labeled_textedit import LabeledTextEdit
from _widgets.labeled_dropdown import LabeledDropdown
from _widgets.labeled_line_edit import LabeledLineEdit
from _modals.destructive_modal import DestructiveModal
from _modals.image_modal import ImageModal
import os
import re
from PIL import Image

INTVALIDATOR = QIntValidator()
DOUBLEVALIDATOR = QDoubleValidator()
DOUBLEVALIDATOR.setBottom(0.01)
DOUBLEVALIDATOR.setTop(1.00)
DOUBLEVALIDATOR.setDecimals(2)


class View(QWidget):
    def __init__(self, viewModel: ViewModel):
        super().__init__()
        self._viewModel = viewModel
        self._viewModel.fetchedLogoNames.connect(self.fetchedLogoNames)
        self._viewModel.logoLoaded.connect(self.logoLoaded)
        self._viewModel.savedLogo.connect(self.savedLogo)
        self._viewModel.deletedLogo.connect(self.deletedLogo)
        self._viewModel.testedLogo.connect(self.testedLogo)
        self._viewModel.logoized.connect(self.logoized)
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
        self.logoName.textChanged.connect(self.canSaveAndTest)
        logoLayout.addWidget(self.logoName)
        self.selectedLogo = LabeledDropdown("Logo Select:", ["New Logo"] + sorted(self._viewModel.model.fetchLogoNames()))
        self.selectedLogo.currentTextChanged.connect(lambda: self._viewModel.loadLogo(self.selectedLogo.getCurrentText()))
        logoLayout.addWidget(self.selectedLogo)
        layout.addLayout(logoLayout)

        # layout the upload and position section
        pathLayout = QHBoxLayout()
        self.uploadLogo = LabeledButton("Logo:", "Upload")
        self.uploadLogo.clicked.connect(self.uploadLogoButtonClicked)
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
        self.Xpadding.setValidator(INTVALIDATOR)
        self.Ypadding.setValidator(INTVALIDATOR)
        paddingLayout.addWidget(self.paddingLabel)
        paddingLayout.addWidget(self.Xpadding)
        paddingLayout.addWidget(self.Ypadding)
        detailsLayout.addLayout(paddingLayout)

        # layout the scale section
        scaleLayout = QVBoxLayout()
        scaleLayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scaleLabel = QLabel("Scale:")
        self.scale = QComboBox()
        self.scale.addItems(["1.0                   ", "0.95", "0.9", "0.85", "0.8", "0.75", "0.7", "0.65", "0.6", "0.55", "0.5", "0.45", "0.4", "0.35", "0.3", "0.25", "0.2", "0.15", "0.1", "0.05"])
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
        self.Xresolution.setValidator(INTVALIDATOR)
        self.Yresolution.setValidator(INTVALIDATOR)
        resolutionLayout.addWidget(self.resolutionLabel)
        resolutionLayout.addWidget(self.Xresolution)
        resolutionLayout.addWidget(self.Yresolution)
        detailsLayout.addLayout(resolutionLayout)

        # add the details section to the layout
        layout.addLayout(detailsLayout)

        # layout the button section
        buttonLayout = QHBoxLayout()
        initialWarning = "Logo name cannot be empty\nYou must upload a logo"
        self.testLogoButton = QPushButton("Test Logo")
        self.testLogoButton.setEnabled(False)
        self.testLogoButton.setToolTip(initialWarning)
        self.testLogoButton.clicked.connect(self.testLogoButtonClicked)
        buttonLayout.addWidget(self.testLogoButton)
        self.saveLogoButton = QPushButton("Save")
        self.saveLogoButton.setEnabled(False)
        self.saveLogoButton.setToolTip(initialWarning)
        self.saveLogoButton.clicked.connect(self.saveLogoButtonClicked)
        buttonLayout.addWidget(self.saveLogoButton)
        self.deleteLogoButton = QPushButton("Delete")
        self.deleteLogoButton.setObjectName("destructiveButton")
        self.deleteLogoButton.setEnabled(False)
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
    
    def canSaveAndTest(self):
        name = self.logoName.getText()
        why = ""
        if name == "New Logo":
            why += "Logo name cannot be New Logo\n"
        elif name.isspace() or name == "":
            why += "Logo name cannot be empty\n"

        path = self.uploadLogo.toolTip()
        if path == "":
            why += "You must upload a logo\n"
        elif os.path.exists(path) == False:
            why += "Logo does not exist\n"

        why = why[:-1]

        if why != "":
            self.testLogoButton.setToolTip(why)
            self.saveLogoButton.setToolTip(why)
            self.testLogoButton.setEnabled(False)
            self.saveLogoButton.setEnabled(False)
            return
        
        self.testLogoButton.setToolTip("")
        self.saveLogoButton.setToolTip("")
        self.testLogoButton.setEnabled(True)
        self.saveLogoButton.setEnabled(True)

        
    
    def uploadLogoButtonClicked(self):

        self.uploadLogo.setEnabled(False)
        self.uploadLogo.button.setText("Uploading...")
        uploadPath, _ = QFileDialog.getOpenFileName(self, 'Upload File', '', 'Images (*.png *.jpg *.jpeg *.avif)')
        if uploadPath:
            self.uploadLogo.setToolTip(uploadPath)
            self.uploadLogo.button.setText("Uploaded!")
            self.uploadLogo.setEnabled(True)
            QTimer.singleShot(1500, lambda: self.uploadLogo.button.setText("Upload"))
            self.canSaveAndTest()
            return
        self.uploadLogo.button.setText("Failed!")
        self.uploadLogo.setEnabled(True)
        QTimer.singleShot(1500, lambda: self.uploadLogo.button.setText("Upload"))
        return

        
    def fetchedLogoNames(self, names: list):
        currentEditingLogo = self.selectedLogo.getCurrentText()
        currentGeneratingLogo = self.logoSelection.getCurrentText()
        self.selectedLogo.blockSignals(True)
        self.logoSelection.blockSignals(True)
        self.selectedLogo.clear()
        self.logoSelection.clear()
        self.selectedLogo.addItems(["New Logo"] + names)
        self.logoSelection.addItems(names)
        if currentEditingLogo not in names:
            self.selectedLogo.blockSignals(False)
            self.selectedLogo.setCurrentText("New Logo")
        else:
            self.selectedLogo.setCurrentText(currentEditingLogo)
            self.selectedLogo.blockSignals(False)
        if currentGeneratingLogo not in names:
            self.logoSelection.blockSignals(False)
            self.logoSelection.setCurrentText(names[0])
        else:
            self.logoSelection.setCurrentText(currentGeneratingLogo)
            self.logoSelection.blockSignals(False)

    def logoLoaded(self, logo: dict):

        if logo:
            self.testLogoButton.setEnabled(True)
            self.saveLogoButton.setEnabled(True)
            self.saveLogoButton.setText("Update")
            self.deleteLogoButton.setEnabled(True)
            self.uploadLogo.setToolTip(logo['path'])
            self.positionLogo.setCurrentText(logo['position'])
            self.Xpadding.setText(str(logo['padding'][0]))
            self.Ypadding.setText(str(logo['padding'][1]))
            self.scale.setCurrentText(str(logo['scale']))
            self.Xresolution.setText(str(logo['resolution'][0]))
            self.Yresolution.setText(str(logo['resolution'][1]))
            self.logoName.setText(self.selectedLogo.getCurrentText())
            return
        self.testLogoButton.setEnabled(False)
        self.saveLogoButton.setEnabled(False)
        self.saveLogoButton.setText("Save")
        self.deleteLogoButton.setEnabled(False)
        self.uploadLogo.setToolTip("")
        self.positionLogo.setCurrentText("Top Left")
        self.Xpadding.setText("")
        self.Ypadding.setText("")
        self.scale.setCurrentText("1.0                   ")
        self.Xresolution.setText("")
        self.Yresolution.setText("")
        self.logoName.setText("")

    def savedLogo(self, success: bool):
        pass

    def deletedLogo(self, success: bool):
        pass

    def testedLogo(self, image: Image.Image):
        data = image.tobytes("raw", image.mode)
        qimage = QImage(data, image.width, image.height,
                        {
                            "RGB": QImage.Format.Format_RGB888,
                            "RGBA": QImage.Format.Format_RGBA8888,
                            "L": QImage.Format.Format_Grayscale8
                        }[image.mode],
                        )
        pixmap = QPixmap(qimage)

        dialog = ImageModal(self.logoName.getText(), pixmap)
        dialog.exec()

    def logoized(self, success: bool):
        pass
    
    def generateButtonClicked(self):
        self.generateButton.setEnabled(False)
        self.generateButton.setText("Generating...")
        directory = QFileDialog.getExistingDirectory(self, 'Select Output Directory')
        if directory:
            self._viewModel.handleLogoization(self.logoSelection.getCurrentText(), self.imagesUpload.toolTip().split("\n"), directory)
            self.generateButton.setText("Generated!")
            self.generateButton.setEnabled(True)
            QTimer.singleShot(1500, lambda: self.generateButton.setText("Generate"))
            return
        self.generateButton.setText("Failed!")
        self.generateButton.setEnabled(True)
        QTimer.singleShot(1500, lambda: self.generateButton.setText("Generate"))

    def uploadImagesButtonClicked(self):
        self.imagesUpload.setEnabled(False)
        self.imagesUpload.button.setText("Uploading...")
        uploadPaths, _ = QFileDialog.getOpenFileNames(self, 'Upload File', '', 'Images (*.png *.jpg *.jpeg *.avif)')
        if uploadPaths:
            tooltip = ""
            for path in uploadPaths:
                tooltip += f"{path}\n"
            self.imagesUpload.setToolTip(tooltip[:-1])
            self.imagesUpload.button.setText("Uploaded!")
            self.imagesUpload.setEnabled(True)
            QTimer.singleShot(1500, lambda: self.imagesUpload.button.setText("Upload"))
            return
        self.imagesUpload.button.setText("Failed!")
        self.imagesUpload.setEnabled(True)
        QTimer.singleShot(1500, lambda: self.imagesUpload.button.setText("Upload"))
        return
    
    def testLogoButtonClicked(self):
        xPad = int(self.Xpadding.text()) if self.Xpadding.text() != "" else 0
        yPad = int(self.Ypadding.text()) if self.Ypadding.text() != "" else 0
        xRes = int(self.Xresolution.text()) if self.Xresolution.text() != "" else 1280
        yRes = int(self.Yresolution.text()) if self.Yresolution.text() != "" else 720
        self._viewModel.handleTestLogoization(self.uploadLogo.toolTip(), self.positionLogo.getCurrentText(), [xPad, yPad], float(self.scale.currentText()), [xRes, yRes])

    def saveLogoButtonClicked(self):

        logos = [self.selectedLogo.dropdown.itemText(i) for i in range(self.selectedLogo.dropdown.count())]
        if self.logoName.getText() in logos and self.logoName.getText() != self.selectedLogo.getCurrentText():
            dialog = DestructiveModal(f"A Logo named {self.logoName.getText()} already exists. Are you sure you want to overwrite it?", "Overwrite")
            result = dialog.exec()
            if result == QDialog.DialogCode.Accepted:
                xPad = int(self.Xpadding.text()) if self.Xpadding.text() != "" else 0
                yPad = int(self.Ypadding.text()) if self.Ypadding.text() != "" else 0
                xRes = int(self.Xresolution.text()) if self.Xresolution.text() != "" else 1280
                yRes = int(self.Yresolution.text()) if self.Yresolution.text() != "" else 720
                self._viewModel.saveLogo(self.logoName.getText(), self.uploadLogo.toolTip(), self.positionLogo.getCurrentText(), [xPad, yPad], float(self.scale.currentText()), [xRes, yRes])
                return
            text = self.saveLogoButton.text()
            self.saveLogoButton.setText("Cancelled")
            QTimer.singleShot(1500, lambda: self.saveLogoButton.setText(text))
            return
        xPad = int(self.Xpadding.text()) if self.Xpadding.text() != "" else 0
        yPad = int(self.Ypadding.text()) if self.Ypadding.text() != "" else 0
        xRes = int(self.Xresolution.text()) if self.Xresolution.text() != "" else 1280
        yRes = int(self.Yresolution.text()) if self.Yresolution.text() != "" else 720
        self._viewModel.saveLogo(self.logoName.getText(), self.uploadLogo.toolTip(), self.positionLogo.getCurrentText(), [xPad, yPad], float(self.scale.currentText()), [xRes, yRes])
        return

    def deleteLogoButtonClicked(self):

        dialog = DestructiveModal(f"Are you sure you want to delete {self.selectedLogo.getCurrentText()}?", "Delete")
        result = dialog.exec()
        if result == QDialog.DialogCode.Accepted:
            self._viewModel.deleteLogo(self.selectedLogo.getCurrentText())
            return
        text = self.deleteLogoButton.text()
        self.deleteLogoButton.setText("Cancelled")
        QTimer.singleShot(1500, lambda: self.deleteLogoButton.setText(text))
        return