import datetime
import urllib.request
import cv2
import numpy as np
from .models import logs
import time
import os
count = 0

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self,name):
        global count
        count = count +1
        success, image = self.video.read()
        frame_flip = cv2.flip(image, 1)
        parent_dir = "C:\\Users\\amish\\Desktop\\Trainer\\"
        directory = name
        path = os.path.join(parent_dir, directory)
        try: 
            os.mkdir(path)
            filename = "C:\\Users\\amish\\Desktop\\Trainer\\%s\\frame%d.jpg" %(name, count)
            cv2.imwrite(filename, frame_flip)
            ret, jpeg = cv2.imencode('.jpg', frame_flip)
        except OSError as error: 
            filename = "C:\\Users\\amish\\Desktop\\Trainer\\%s\\frame%d.jpg" %(name, count)
            cv2.imwrite(filename, frame_flip)
            ret, jpeg = cv2.imencode('.jpg', frame_flip)
        return jpeg.tobytes()


class IPWebCam(object):
    def __init__(self):
        self.url = "http://192.168.0.102:8080/shot.jpg"

    def __del__(self):
        cv2.destroyAllWindows()

    def get_frame(self):
        imgResp = urllib.request.urlopen(self.url)
        imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
        img = cv2.imdecode(imgNp, -1)
        frame_flip = cv2.flip(img, 1)
        date_time = str(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
        font = cv2.FONT_HERSHEY_SIMPLEX
        frame_flip = cv2.putText(frame_flip, date_time, (10, 100), font, 1, (0, 255, 255), 2, cv2.LINE_AA)
        ret, jpeg = cv2.imencode('.jpg', frame_flip)
        return jpeg.tobytes()
