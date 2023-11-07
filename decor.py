import glob
import cv2
import pygame

class Decor():
    def __init__(self, photoBooth):
        self.photoBooth = photoBooth
        self.overlays = glob.glob("/home/pi/photobooth/overlays/*.png")
        self.overlayId = len(self.overlays)
        self.nextOverlay()

    def nextOverlay(self):
        try:
            self.overlayId += 1
            self.overlayPath = self.overlays[self.overlayId]
        except:
            self.overlayId = 0
        finally:
            self.overlayPath = self.overlays[self.overlayId]
            self.overlay = cv2.imread(self.overlayPath, cv2.IMREAD_UNCHANGED)
            self.overlay = cv2.cvtColor(self.overlay, cv2.COLOR_BGRA2RGBA).swapaxes(0, 1)
            self.overlay = cv2.resize(self.overlay, self.photoBooth.camera.imageSize)

            self.photoBooth.stepsManager.steps[self.photoBooth.stepsManager.stepPreview].buttonsLabels[0] = "Décor suivant " + str(self.overlayId+1) + "/" + str(len(self.overlays))
            