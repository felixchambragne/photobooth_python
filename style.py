import pygame
import numpy as np
import cv2

class Style():
    def __init__(self, photoBooth):
        self.photoBooth = photoBooth
        self.screen = self.photoBooth.screen
        
        #--------Fonts------
        self.fontButton = pygame.font.SysFont(None, 100)
        self.fontTitle = pygame.font.SysFont(None, 80)
        self.fontText = pygame.font.SysFont(None, 30)
        self.fontCounter = pygame.font.SysFont(None, 200)
        
        #-------Colors--------
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREY = (196, 196, 196)
        self.RED = (252, 53, 70)
        self.BLUE = (53, 70, 252)
        
        self.padding = 40
        self.radius = 10

        self.topRect = pygame.Rect(0, 0, self.photoBooth.width, self.photoBooth.height/6)
        self.bottomRect = pygame.Rect(0, self.photoBooth.height-self.photoBooth.height/6, self.photoBooth.width, self.photoBooth.height/6)
        
        self.loadingPercentage = 0
        self.loadingDirection = 1
        
    def update(self):
        self.screen.fill(self.BLACK)
        
    def showTitle(self, label):
        self.title = self.fontTitle.render(label, True,  self.WHITE)
        self.titleRect = self.title.get_rect(center=(self.photoBooth.width/2, self.photoBooth.height/12))
        self.screen.blit(self.title, self.titleRect)
        
    def showImage(self, image):
        self.imageSurface = pygame.surfarray.make_surface(image)
        self.imageRect = self.imageSurface.get_rect(center=(self.photoBooth.width/2, self.photoBooth.height/2))
        self.screen.blit(self.imageSurface, self.imageRect)
            
    def showCounter(self, counter):
        #Background
        self.counterBackgroundSurface = pygame.Surface((200, 200))
        self.counterBackgroundSurface.set_alpha(128)
        self.counterBackgroundSurface.fill(self.BLACK)
        self.counterBackgroundRect = self.counterBackgroundSurface.get_rect(
            center=(self.photoBooth.width/2, self.photoBooth.height/2),
        )
        self.screen.blit(self.counterBackgroundSurface, self.counterBackgroundRect)
        #Text
        self.counterText = self.fontCounter.render(str(counter), True, self.WHITE)
        self.counterRect = self.counterText.get_rect(center=(self.photoBooth.width/2, self.photoBooth.height/2))
        self.screen.blit(self.counterText, self.counterRect)
        
    def showButtons(self, buttonsLabels):
        self.buttonsColors = [self.WHITE, self.WHITE]
        self.buttonY = self.photoBooth.height-self.photoBooth.height/6+self.photoBooth.height/6/2
        self.buttonX = (self.photoBooth.width/6, self.photoBooth.width-self.photoBooth.width/6)
        for i in range(2):
            self.buttonLeft = self.fontButton.render(buttonsLabels[i], True,  self.BLACK)
            self.buttonLeftRect = self.buttonLeft.get_rect(center=(self.buttonX[i], self.buttonY))
            #Background
            if buttonsLabels[i] != "":
                self.buttonLeftBackgroundRect = self.buttonLeft.get_rect(center=(self.buttonX[i]-self.padding/2, self.buttonY-self.padding/2))
                self.buttonLeftBackgroundRect.w, self.buttonLeftBackgroundRect.h = self.buttonLeftRect.w + self.padding, self.buttonLeftRect.h + self.padding
                pygame.draw.rect(self.screen, self.buttonsColors[i], self.buttonLeftBackgroundRect,  0, self.radius)
            self.screen.blit(self.buttonLeft, self.buttonLeftRect)
    
    def centerIcon(self, path):
        self.icon = pygame.image.load(path).convert_alpha()
        self.icon = pygame.transform.scale(self.icon, (300, 300))
        self.iconnRect = self.icon.get_rect(center=(self.photoBooth.width/2, self.photoBooth.height/2))
        self.screen.blit(self.icon, self.iconRect)

    def centerText(self, textString):
        self.text = self.fontText.render(textString, True,  self.WHITE)
        self.textRect = self.text.get_rect(center=(self.photoBooth.width/2, self.photoBooth.height/2+self.captureIcon.get_rect().height))
        self.screen.blit(self.text, self.textRect)

    def showCaptureIcon(self):
        self.centerIcon("/home/pi/photobooth/program/camera.bmp")
        self.centerText("Ne bougez plus c'est parfait !")
    
    def showErrorIcon(self):
        self.centerIcon("/home/pi/photobooth/program/warning.bmp")
    
    def showPrintIcon(self):
        self.centerIcon("/home/pi/photobooth/program/print.bmp")
        self.centerText("Merci de patienter quelques secondes")
        
    def showLoading(self, label):
        if self.loadingPercentage > 100:
            if self.loadingDirection == 1:
                self.loadingDirection = -1
            else:
                self.loadingDirection = 1
            self.loadingPercentage = 0
        self.loadingPercentage += 6
        if self.loadingDirection == 1:
            endAngle = 360*self.loadingPercentage/100
            startAngle = 0
        else:
            startAngle = 360*self.loadingPercentage/100
            endAngle = 360
        width = 4
        radius = 50
        circleImage = np.zeros((radius*2+4, radius*2+4, 4), dtype = np.uint8)
        circleImage = cv2.ellipse(circleImage, (radius+2, radius+2),(radius-width//2, radius-width//2), 
                                0, startAngle, endAngle, (*self.WHITE, 255), width, lineType=cv2.LINE_AA)
        circleSurface = pygame.image.frombuffer(circleImage.flatten(), (radius*2+4, radius*2+4), 'RGBA')
        self.screen.blit(circleSurface, circleSurface.get_rect(center=(self.photoBooth.width/2, self.photoBooth.height/2)))
        
        self.loadingText = self.fontText.render(label, True,  self.WHITE)
        self.loadingTextRect = self.loadingText.get_rect(center=(self.photoBooth.width/2, self.photoBooth.height/2+circleSurface.get_rect().height))
        self.screen.blit(self.loadingText, self.loadingTextRect)
