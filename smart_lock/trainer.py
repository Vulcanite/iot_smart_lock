import cv2
import os
import numpy as np
from PIL import Image
import pickle
import shutil
import cv2
import os
import numpy as np
from PIL import Image
import pickle
import shutil


class FaceTrainer(object):
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

    def trainer(self):
        for root ,dirs , files in os.walk(img_dir):
            for file in files:
                if file.endswith('jpg') or file.endswith('jpeg'):
                    path= os.path.join(root,file)
                    label= os.path.basename(os.path.dirname(path))
                    #print(label_ids)
                    if  not label in label_ids:
                        label_ids[label] = current_id
                        current_id =current_id+ 1
                    id_ = label_ids[label]
                    pil_img = Image.open(path).convert("L")
                    img_array = np.array(pil_img, "uint8")
                    faces = face_cascade.detectMultiScale(img_array, scaleFactor=1.5,minNeighbors=5)
                    #fetch the ROI from imgs
                    for (x, y, w, h) in faces:
                        roi = img_array[y:y + h, x:x + w]
                        x_train.append(roi)
                        y_labels.append(id_)

        with open("face-labels.pkl", 'wb') as f:
            pickle.dump(label_ids, f)
        nn.train(x_train, np.array(y_labels))
        nn.save("face-trainner.yml")

    def del_data(self):
        for root, dirs, files in os.walk(img_dir):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))





base_dir= os.path.dirname(os.path.abspath(__file__))
img_dir= os.path.join(base_dir,'train')

face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')
nn = cv2.face.LBPHFaceRecognizer_create()

current_id = 0
label_ids = {}
y_labels = []
x_train = []

for root ,dirs , files in os.walk(img_dir):
    for file in files:
        if file.endswith('png') or file.endswith('jpg') or file.endswith('jpeg'):
            path= os.path.join(root,file)
            label= os.path.basename(os.path.dirname(path))
            #print(label_ids)
            if  not label in label_ids:
                label_ids[label] = current_id
                current_id =current_id+ 1
            id_ = label_ids[label]
            pil_img = Image.open(path).convert("L")
            img_array = np.array(pil_img, "uint8")
            faces = face_cascade.detectMultiScale(img_array, scaleFactor=1.5,minNeighbors=5)
            #fetch the ROI from imgs
            for (x, y, w, h) in faces:
                roi = img_array[y:y + h, x:x + w]
                x_train.append(roi)
                y_labels.append(id_)
                #print(y_labels)

#code to delete the train data after training
'''
for root, dirs, files in os.walk(img_dir):
    for f in files:
        os.unlink(os.path.join(root, f))
    for d in dirs:
        shutil.rmtree(os.path.join(root, d))
'''

with open("face-labels.pkl", 'wb') as f:
	pickle.dump(label_ids, f)
nn.train(x_train, np.array(y_labels))
nn.save("face-trainner.yml")