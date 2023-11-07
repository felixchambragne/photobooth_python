import pygame
from camera import Camera
from stepsManager import StepsManager
from button import Button
from style import Style
from decor import Decor
import os

class PhotoBooth():
    def __init__(self):
        self.emptyTempFolder()
        self.name = "PhotoBooth"
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.width, self.height = pygame.display.get_surface().get_size()
        pygame.display.set_caption(self.name)
        self.style = Style(self)
                
        self.stepsManager = StepsManager(self)
        self.buttonLeft = Button(self, 20, 0)
        self.buttonRight = Button(self, 21, 1)

        self.camera = Camera(self)
        self.decor = Decor(self)
    
    def emptyTempFolder(self):
        try:
            tempFolder = '/home/pi/photobooth/captures/'
            files = [f for f in os.listdir(tempFolder) if os.path.isfile(os.path.join(tempFolder, f))]
            if len(files) != 0:
                for file in files:
                    os.remove(os.path.join(tempFolder, file))
        except:
            print("erreur suppression")

    def update(self):
        self.style.update()
        self.buttonLeft.update()
        self.buttonRight.update()
        self.stepsManager.update()
        pygame.display.flip()
    
    def run(self):
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False     
            self.update()
            clock.tick(60)
        self.camera.camera.exit()
        pygame.quit() 