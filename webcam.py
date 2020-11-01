import cv2

def takeImage():
    webcam = cv2.VideoCapture(0)
    check, frame = webcam.read()
    cv2.imwrite(filename='saved_img.jpg', img=frame)
    webcam.release()
    img_new = cv2.imread('saved_img.jpg', cv2.IMREAD_GRAYSCALE)
    
    
takeImage()


