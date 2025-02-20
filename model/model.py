from PyQt6.QtCore import QObject
import json
from PIL import Image
import pillow_avif
from typing import TypedDict
import os

#LOGOSTYPEHINT = TypedDict(str, {'path': str, 'position': str, 'padding': list[int], 'scale': float, 'resolution': list[int]})


class Model(QObject):
    def __init__(self):
        super().__init__()
        self.logos = self.fetchLogos()
        self.logoTabSelection : str = ''
        self.generateTabSelection : str = ''

    def fetchLogos(self):
        logos = {}
        with open('logos.json') as f:
            logos = json.load(f)
        return logos
    
    def fetchLogoNames(self):
        return list(self.logos.keys())

    def loadLogo(self, name: str):
        if name not in self.logos:
            return None
        return self.logos[name]
    
    def saveLogo(self, name: str, path: str, position: str, padding: list[int], scale: float, resolution: list[int]):
        try:
            self.logos[name] = {
                'path': path,
                'position': position,
                'padding': padding,
                'scale': scale,
                'resolution': resolution
            }
            with open('logos.json', 'w') as f:
                json.dump(self.logos, f, indent=2)
            return True
        except:
            return False

    def deleteLogo(self, name: str):
        try: 
            del self.logos[name]
            with open('logos.json', 'w') as f:
                json.dump(self.logos, f)
            return True
        except:
            return False
    
    def saveLogoized(self, saveName: str, saveDestination: str, image: Image):
        image = image.convert('RGB')
        image.save(os.path.join(saveDestination, saveName))

    def generateLogoized(self, logo, images: list[str]):

        # load the logo
        _logo = logo
        print(_logo)
        try:
            logo_image = Image.open(_logo['path'])
        except:
            return "Logo not found"
        
        logo_image = self.resizeLogo(logo_image, _logo['scale'], _logo['resolution'])

        logoizedImages = []

        for image in images:
            print(image)
            _image = Image.open(image)
            print(_image)
            _image = self.resizeImage(_image, _logo['resolution'])
            print(_image)
            _image = self.cropImage(_image, _logo['resolution'])
            print(_image)
            _image = self.placeLogo(_image, logo_image, _logo['position'], _logo['padding'])
            print(_image)
            logoizedImages.append(_image)
        
        print(logoizedImages)

        return logoizedImages
    
    def handleTestLogoization(self, testPath: str, testPosition: str, testPadding: list[int], testScale: float, testResolution: list[int]):
        logo = {
            'path': testPath,
            'position': testPosition,
            'padding': testPadding,
            'scale': testScale,
            'resolution': testResolution
        }

        logoizedImage = self.generateLogoized(logo, ["grid.png"])
        return logoizedImage[0]

    def handleLogoization(self, logoName: str, images: list[str], saveDesination: str):

        try:
            _logo = self.logos[logoName]

            logoizedImages = self.generateLogoized(_logo, images)

            for logoizedImage, image in zip(logoizedImages, images):
                base_filename = os.path.basename(image)
                stripped_filename = os.path.splitext(base_filename)[0]
                extension = stripped_filename + '.jpg'
                self.saveLogoized(extension, saveDesination, logoizedImage)
            return True
        except:
            return False


    def placeLogo(self, image: Image, logo: Image, position: str, padding: list[str]):
        imageWidth, imageHeight = image.size
        logoWidth, logoHeight = logo.size
        paddingX = padding[0]
        paddingY = padding[1]
        _, _, _, mask = logo.split()

        xPos = 0
        yPos = 0
        if position.lower() == "top left":
            xPos = int(paddingX)
            yPos = int(paddingY)
        elif position.lower() == "top right":
            xPos = int(imageWidth - logoWidth - paddingX)
            yPos = int(paddingY)
        elif position.lower() == "bottom left":
            xPos = int(paddingX)
            yPos = int(imageHeight - logoHeight - paddingY)
        elif position.lower() == "bottom right":
            xPos = int(imageWidth - logoWidth - paddingX)
            yPos = int(imageHeight - logoHeight - paddingY)

        image.paste(logo, (xPos, yPos), mask)
        return image

    def cropImage(self, image: Image, resolution: list[int]):
        width, height = image.size
        newWidth = int(resolution[0])
        newHeight = int(resolution[1])

        halfWidth = newWidth // 2
        widthExtra = newWidth % 2
        halfHeight = newHeight // 2
        heightExtra = newHeight % 2

        centerX = width // 2
        centerY = height // 2

        leftBound = centerX - halfWidth
        rightBound = centerX + halfWidth + widthExtra
        topBound = centerY - halfHeight
        bottomBound = centerY + halfHeight + heightExtra

        box = (leftBound, topBound, rightBound, bottomBound)
        image = image.crop(box)
        return image


    def resizeImage(self, image: Image, resolution: list[int]):
        width, height = image.size
        newWidth = int(resolution[0])
        newHeight = int(resolution[1])

        widthRatio = width / newWidth
        heightRatio = height / newHeight
        finalRatio = min(widthRatio, heightRatio)

        image = image.resize((int(width * (1 / finalRatio)), int(height * (1 / finalRatio))))
        return image


    def resizeLogo(self, logo: Image, scale: float, resolution: list[int]):
        logoWidth, logoHeight = logo.size
        newHeight = int(resolution[1] * scale)
        newWidth = int((newHeight * logoWidth) / logoHeight)
        logo = logo.resize((newWidth, newHeight))
        return logo




        