import cv2
import numpy as np
from matplotlib import pyplot as plt
import sys
import math
from IPython.display import Image
pi = math.pi

def __main__(path):
  img = cv2.imread(path)
  path = path.replace(".png", "") 
  outOfFocus(img, path, 5)
  gaussianBlur(img, path)
  horizontalBlur(img, path, 5)
  verticalBlur(img, path, 5)
  boxBlur(img, path, 5)
  medianBlur(img, path, 5) 

def gaussianBlur(img, path): 
  # Gaussian
  # K1 = 11, K2 = 13
  gausBlur = cv2.GaussianBlur(img, (11,11),0)  
  cv2.imwrite(path + "_gaussianBlur.png", gausBlur)
  

def outOfFocus(img, path, k):
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
  cv2.imwrite(path + "_outofFocus.png", focus)
  

def horizontalBlur(img, path, k):
  kernel = np.zeros((k, k)) 
  kernel[int((k - 1)/2), :] = np.ones(k) 
  kernel /= k
  horizontal = cv2.filter2D(img, -1, kernel)
  cv2.imwrite(path + "_horizontalBlur.png", horizontal)

def verticalBlur(img, path, k):
  # Create the vertical kernel. 
  kernel = np.zeros((k, k)) 
  # Fill the middle row with ones. 
  kernel[:, int((k - 1)/2)] = np.ones(k)   
  # Normalize. 
  kernel /= k   
  # Apply the vertical kernel. 
  vertical = cv2.filter2D(img, -1, kernel) 
  cv2.imwrite(path + "_verticalBlur.png", vertical)

def boxBlur(img, path, k): # Averaging/Box Blur
  kernel = np.ones((k,k),np.float32) / (k ** 2)
  avging = cv2.blur(img,(5,5)) 
  cv2.imwrite(path + "_boxBlur.png", avging)

def medianBlur(img, path, k):
  # Median blurring (not used in paper)
  medBlur = cv2.medianBlur(img,k)
  cv2.imwrite(path + "_medianBlur.png", medBlur)

if __name__ == "__main__":
  path = input("Enter the path of the image on which blurring should be applied: ")
  if path == "":
    path = "sample_input.png"
  __main__(path) 
