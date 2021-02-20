import cv2
import numpy as np
import matplotlib.pyplot as plt 
import math

def __main__(path, strength, zoom):
  img = cv2.imread(path)
  width = img.shape[1]
  height = img.shape[0]
  halfWidth = width / 2
  halfHeight = height / 2
  if strength == 0:
    strength = 0.0001
  correctionRadius = math.sqrt((width ** 2) + (height ** 2)) / strength
  for x in range(0, width):
    for y in range(0, height):
      newX = x - halfWidth
      newY = y - halfHeight
      dist = math.sqrt((newX ** 2) + (newY ** 2))
      r = dist / correctionRadius
      if r == 0:
        theta = 1
      else:
        theta = math.atan(r) / r
      sourceX = halfWidth + theta * newX * zoom
      print(x)
      print(y)
      sourceY = halfWidth + theta * newY * zoom
      if sourceX < width and sourceY < height:
        img[int(y), int(x)] = img[int(sourceY), int(sourceX)] 
  cv2.imwrite("output.png", img)
  

if __name__ == "__main__":
  path = input("Input the path of the image here: ")
  strength = float(input("Input the strength of correction here: "))
  zoom = float(input("Input the zoom of correction here: "))
  if path == "":
    path = "sample_input.png"
  __main__(path, strength, zoom)
