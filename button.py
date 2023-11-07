import RPi.GPIO as GPIO

class Button:
    def __init__(self, photoBooth, pin, buttonId):
        self.photoBooth = photoBooth
        self.stepsManager = self.photoBooth.stepsManager
        self.pressed = False
        self.pin = pin
        self.buttonId = buttonId
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def update(self):
        if not self.stepsManager.disabledButtons:
            if GPIO.input(self.pin) == GPIO.LOW:
                if not self.pressed:
                    self.pressed = True
                    self.stepsManager.stepAction(self.buttonId)
            else:
                self.pressed = False
            
        
