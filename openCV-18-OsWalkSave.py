import face_recognition as fr
import cv2 as cv
import os
import time as t
import pickle as pkl
print(cv.__version__)

Encodings=[]
Names=[]

imageDir='C:\\Users\es017590\Documents\py\demoImages\known'
for root,dirs,files in os.walk(imageDir):
    for file in files:
        f=fr.load_image_file(os.path.join(root,file))
        face=fr.face_encodings(f)
        Encodings.append(face[0])
        Names.append(os.path.splitext(file)[0])

with open('trainingData.pkl', 'wb') as fo:
    pkl.dump(Encodings, fo)
    pkl.dump(Names, fo)
fo.close()

print('Done!')