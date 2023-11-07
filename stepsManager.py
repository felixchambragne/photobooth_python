from countdown import Countdown
import os
import cv2
from PIL import Image
import numpy as np

class Step():
    def __init__(self, actions, buttonsLabels, titleLabel):
        self.actions = actions
        self.buttonsLabels = buttonsLabels
        self.titleLabel = titleLabel

class StepsManager():
    def __init__(self, photoBooth):
        self.photoBooth = photoBooth
        self.screen = self.photoBooth.screen
        self.style = self.photoBooth.style
        self.isCaptured = False
        self.captureIsStarted = False
        self.captureIsShown = False
        self.loadingLabel = "Chargement..."
        self.disabledButtons = False
        
        self.countdown = Countdown(self, 3, self.stepCapture)

        self.steps = {
            self.stepCameraError: Step(
                actions = (self.stepCameraError, self.checkCamera),
                buttonsLabels = ["", "Réessayer"],
                titleLabel = "Appareil photo non détecté",
            ),
            self.stepPreview: Step(
                actions = (self.nextOverlay, self.startCountdown),
                buttonsLabels = ["Décor suivant", "Prendre la photo !"],
                titleLabel = "Préparez-vous",
            ),
            self.stepCapture: Step(
                actions = (self.retry, self.printCapture),
                buttonsLabels = ["Refaire", "Imprimer"],
                titleLabel = "Valider la photo",
            ),
            self.stepCaptureError: Step(
                actions = (self.stepCaptureError, self.stepPreview),
                buttonsLabels = ["", "Réessayer"],
                titleLabel = "Erreur lors de la capture",
            ),
            self.stepPrint: Step(
                actions = (self.stepPrint, self.stepPrint),
                buttonsLabels = ["", ""],
                titleLabel = "Impression en cours ...",
            ),
        }
        self.step = self.stepPreview
  
    def checkCamera(self):
        self.photoBooth.camera.checkError()
    
    def stepCameraError(self):
        self.disabledButtons = False
        self.style.showErrorIcon()

    def stepCaptureError(self):
        self.disabledButtons = False
        self.style.showErrorIcon()
    
    def nextOverlay(self):
        self.photoBooth.decor.nextOverlay()
    
    def retry(self):
        try:
            os.remove(self.photoBooth.camera.target)
        except:
            pass
        self.step = self.stepPreview

    def stepPreview(self):
        if self.captureIsStarted:
            self.captureIsStarted = False
            self.isCaptured = False
            self.captureIsShown = False
        
        self.image = self.photoBooth.camera.startPreview()

        self.style.showImage(self.image)
        self.style.showImage(self.photoBooth.decor.overlay)

        if self.countdown.isStarted:
            self.style.showCounter(self.countdown.counter)
        
    def startCountdown(self):
        self.disabledButtons = True
        self.countdown = Countdown(self, 3, self.stepCapture)
        self.countdown.start()
                
    def startCapture(self):
        self.photoBooth.camera.captureImage()

    def stepCapture(self):
        if not self.captureIsShown and self.isCaptured: #La photo est prise et ça charge
            self.steps[self.stepCapture].titleLabel = ""
            self.style.showLoading(self.loadingLabel)
        elif not self.isCaptured: #La photo est en cours
            self.steps[self.stepCapture].titleLabel = "Ne bougez plus c'est parfait !"
            self.style.showCaptureIcon()
        else: #La photo est prise, afficher
            self.steps[self.stepCapture].titleLabel = "Valider la photo"
            self.style.showImage(self.photoBooth.camera.capture)

        if not self.captureIsStarted: #La photo n'est pas prise -> Prendre la photo
            self.captureIsStarted = True
            self.startCapture()

    def stepPrint(self):
        self.style.showPrintIcon()

    def printCapture(self):
        self.disabledButtons = True
        self.step = self.stepPrint
        self.countdownPrint = Countdown(self, 5, self.stepPreview)
        self.countdownPrint.start()
        
        self.finalImage = self.photoBooth.camera.capture
        alpha_channel = self.photoBooth.decor.overlay[:, :, 3] / 255
        overlay_colors = self.photoBooth.decor.overlay[:, :, :3]
        alpha_mask = np.dstack((alpha_channel, alpha_channel, alpha_channel))
        h, w = self.photoBooth.decor.overlay.shape[:2]
        background_subsection = self.finalImage[0:h, 0:w]
        composite = background_subsection * (1 - alpha_mask) + overlay_colors * alpha_mask
        self.finalImage[0:h, 0:w] = composite

        self.image = Image.fromarray(self.finalImage)
        self.image.convert('RGB')
        self.image.save((self.finalImagePath + ".pdf"))
               
        try:
            os.remove(self.photoBooth.camera.target)
        except:
            pass

        self.disabledButtons = False
    
    def update(self): 
        self.step()
        self.style.showTitle(self.steps[self.step].titleLabel)
        if not self.disabledButtons:
            self.style.showButtons(self.steps[self.step].buttonsLabels)
        
    def stepAction(self, buttonId):
        #If action is a step changement -> Change current step to new step
        #Else -> start action
        if self.steps[self.step].actions[buttonId] in list(self.steps.keys()):
            self.step = self.steps[self.step].actions[buttonId]
        else:
            self.steps[self.step].actions[buttonId]()
