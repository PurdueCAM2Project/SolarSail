import cv2
import numpy as np
from matplotlib import pyplot as plt
import sys
import os
import math
pi = math.pi

def __main__(path, extension):
  img = cv2.imread(path)
  path = path.replace(extension, "") 
  outOfFocus(img, path, extension, 5)
  gaussianBlur(img, path, extension)
  horizontalBlur(img, path, extension, 5)
  verticalBlur(img, path, extension, 5)
  boxBlur(img, path, extension, 5)
  medianBlur(img, path, extension, 5) 

def gaussianBlur(img, path, extension): 
  gausBlur = cv2.GaussianBlur(img, (11,11),0)  
  cv2.imwrite(path + "_gaussianBlur" + extension, gausBlur)
  
def outOfFocus(img, path, extension, k):
  kernel = np.zeros((k, k)) 
  r = k/2
  rSquared = r**2
  for x in range(0, len(kernel)):
    for y in range(0, len(kernel)):
      condition = ((x+1)**2) + ((y+1)**2)
      condition = math.sqrt(condition)
      if condition <= rSquared:
        kernel[x, y] = 1
  kernel /= (rSquared * pi)
  focus = cv2.filter2D(img, -1, kernel) 
  cv2.imwrite(path + "_outofFocus" + extension, focus)
  
def horizontalBlur(img, path, extension, k):
  kernel = np.zeros((k, k)) 
  kernel[int((k - 1)/2), :] = np.ones(k) 
  kernel /= k
  horizontal = cv2.filter2D(img, -1, kernel)
  cv2.imwrite(path + "_horizontalBlur" + extension, horizontal)

def verticalBlur(img, path, extension, k):
  kernel = np.zeros((k, k)) 
  kernel[:, int((k - 1)/2)] = np.ones(k)   
  kernel /= k   
  vertical = cv2.filter2D(img, -1, kernel) 
  cv2.imwrite(path + "_verticalBlur" + extension, vertical)

def boxBlur(img, path, extension, k):
  kernel = np.ones((k,k),np.float32) / (k ** 2)
  avging = cv2.blur(img,(5,5)) 
  cv2.imwrite(path + "_boxBlur" + extension, avging)

def medianBlur(img, path, extension, k):
  medBlur = cv2.medianBlur(img,k)
  cv2.imwrite(path + "_medianBlur" + extension, medBlur)

if __name__ == "__main__":
  path = input("Enter the path of the image on which blurring should be applied: ")
  if path == "":
    path = "sample_input.png"
  extension = os.path.splitext(path)[1]
  print(extension)
  __main__(path, extension)