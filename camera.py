import gphoto2 as gp
import io
import numpy
import cv2
import os
from threading import Thread
import sys
import random
import string

class Camera():
    def __init__(self, photoBooth):
        self.photoBooth = photoBooth
        self.checkError() #Init camera if not error
        self.height = int(self.photoBooth.height/1.5)
        self.width = int(self.height*3/2)
        self.imageSize = (self.height, self.width)
        
    def checkError(self):
        self.cameraDetected = gp.Camera.autodetect()
        if self.cameraDetected:
            self.camera = gp.Camera()
            self.camera.init()
            self.photoBooth.stepsManager.step = self.photoBooth.stepsManager.stepPreview
        else:
            self.photoBooth.stepsManager.step = self.photoBooth.stepsManager.stepCameraError
        
    def startPreview(self):
        #Get preview image from gphoto
        OK, self.previewFile = gp.gp_camera_capture_preview(self.camera)
        if OK < gp.GP_OK:
            self.photoBooth.stepsManager.step = self.photoBooth.stepsManager.stepCameraError
        else:
            self.previewFileData = gp.check_result(gp.gp_file_get_data_and_size(self.previewFile))
            #Convert to ByteIO data
            self.previewBytesIO = io.BytesIO(self.previewFileData)
            #Convert to OpenCV image
            self.previewcv = cv2.imdecode(numpy.frombuffer(self.previewBytesIO.read(), numpy.uint8), 1)
            self.preview = cv2.cvtColor(self.previewcv, cv2.COLOR_BGR2RGB).swapaxes(0, 1)
            self.preview = cv2.resize(self.preview, self.imageSize)
            self.preview = cv2.flip(self.preview, 0)
        return self.preview
    
    def captureImage(self):
        self.threadCapture = Thread(target=self.captureImageThread)
        self.threadCapture.start()
        
    def captureImageThread(self):
        try:
            self.imagePath = self.camera.capture(gp.GP_CAPTURE_IMAGE)
            self.photoBooth.stepsManager.isCaptured = True
            
            self.imageName = ''.join(random.choice(string.ascii_letters) for i in range(6))
            
            self.target = os.path.join('/home/pi/photobooth/captures/', self.imageName)

            self.cameraFile = self.camera.file_get(self.imagePath.folder, self.imagePath.name, gp.GP_FILE_TYPE_NORMAL)
            self.cameraFile.save(self.target)
            self.photoBooth.stepsManager.loadingLabel = "Super ! ça arrive..."
            self.capture = cv2.imread(self.target)
            self.capture = cv2.cvtColor(self.capture, cv2.COLOR_BGR2RGB).swapaxes(0, 1)
            self.capture = cv2.resize(self.capture, self.imageSize)
            self.capture = cv2.flip(self.capture, 0)
                        
            self.photoBooth.stepsManager.captureIsShown = True
            self.photoBooth.stepsManager.disabledButtons = False
        except: 
            self.photoBooth.stepsManager.step = self.photoBooth.stepsManager.stepCaptureError
        
        sys.exit()
        
