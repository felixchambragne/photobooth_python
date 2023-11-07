import os
import win32print
import win32api
import time
import shutil

dirPath = "Z:\\"
keyPath = "D:\\"

while True:
    try:
        files = [f for f in os.listdir(os.path.join(dirPath, "print_queue")) if os.path.isfile(os.path.join(dirPath, "print_queue", f))]
        #List of all files in print queue
        if len(files) != 0:
            filePath = os.path.join(dirPath, "print_queue", files[0]) #Get first file

            while not os.path.exists(filePath): #Wait while file doesn't exist
                time.sleep(0.1)
            while os.stat(filePath).st_size == 0: #Wait while file isn't charged
                time.sleep(0.1)

            win32api.ShellExecute(
                0,
                "printto",
                filePath,
                '"%s"' % win32print.GetDefaultPrinter(),
                ".",
                0
            )
            time.sleep(5)
            
            #move file in USB key
            shutil.move(filePath, os.path.join(keyPath, files[0]))

            while not os.path.exists(os.path.join(keyPath, files[0])):
                time.sleep(0.1)
            while os.stat(os.path.join(keyPath, files[0])).st_size == 0:
                time.sleep(0.1)
            filePath = os.path.join(keyPath, files[0])

            print("Impression de : ", filePath)
    except Exception as e:
        print(e)