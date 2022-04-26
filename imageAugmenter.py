import os
#import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import tensorflow_datasets as tfds
import PIL.Image
from PIL import Image, ImageEnhance
#import cv2



#def getJPG(listdr):
   # for fileName in os.listdir(listdr):
      #  if fileName.endswith('.JPG'):
      #      jpeglist.append(fileName)

def enhancer(listdr):
    for fileName in os.listdir(listdr):
        if fileName.endswith('.JPG'):
            fileName = fileName.replace('.JPG',"")
            im = Image.open(os.getcwd()+'/'+listdr+'/'+fileName)
            im = im.rotate(270,expand=True)
            enhancer = ImageEnhance.Contrast(im)
            factor = 2
            im_output = enhancer.enhance(factor)
            #im_output = im_output.rotate(270,expand=True)
            im_output.save(os.getcwd()+'/'+listdr+'/'+fileName+'augmented.JPG')
            im1 = tf.image.random_brightness(im, 0.3)
            tf.keras.utils.save_img(os.getcwd()+'/'+listdr+'/'+fileName+'brightness.JPG', im1)
            im2 = tf.image.random_saturation(im, 0, 5)
            tf.keras.utils.save_img(os.getcwd()+'/'+listdr+'/'+fileName+'saturation.JPG', im2)

def delete(listdr):
    
    for fileName in os.listdir(listdr):
        if fileName.endswith('.JPGaugmented.JPG'):
            os.remove(os.getcwd()+'/'+listdr+'/'+fileName)
        if fileName.endswith('.JPGbrightness.JPG'):
            os.remove(os.getcwd()+'/'+listdr+'/'+fileName)
        if fileName.endswith('.JPGsaturation.JPG'):
            os.remove(os.getcwd()+'/'+listdr+'/'+fileName)
            
            
    


for folderName in os.listdir('Images'):
    delete('Images/'+folderName)    #use this to delete the augmented images
    #enhancer('Images/'+folderName)
    
