# https://stackoverflow.com/questions/53537561/radius-of-a-disk-in-a-binary-image

from skimage import io
import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
from skimage.draw import circle

image = io.imread('20-1.tif')

plt.figure(figsize=[16,8])
image_pixels=image.reshape(-1,3)

m_image_pixels = np.zeros_like(image_pixels)
idx = np.argmax(image_pixels,axis=1)
m_image_pixels[idx==0]=[255,0,0]
m_image_pixels[idx==1]=[0,255,0]
m_image_pixels[idx==2]=[0,0,255]
m_image = m_image_pixels.reshape(image.shape)
plt.subplot(2,2,1)
plt.imshow(m_image)

m_image_pixels[idx==2] = [255, 255, 255]
m_image_pixels[idx!=2] = [0, 0, 0]
m_image = m_image_pixels.reshape(image.shape)
plt.subplot(2,2,2)
plt.imshow(m_image)

# https://docs.opencv.org/master/d9/d61/tutorial_py_morphological_ops.html
binary_image = np.mean(m_image, axis=2)
binary_image[binary_image>0]=1
kernel = np.ones((3, 3), np.uint8)
# kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE,(5,5))
image_opening = cv.morphologyEx(binary_image, cv.MORPH_OPEN, kernel, iterations=5)
image_closing = cv.morphologyEx(image_opening, cv.MORPH_CLOSE, kernel, iterations=2)

plt.subplot(2,2,3)
plt.imshow(image_opening)
plt.subplot(2,2,4)
plt.imshow(image_closing)

# https://www.pyimagesearch.com/2014/07/21/detecting-circles-images-using-opencv-hough-circles/

plt.figure(figsize=[16,8])
img = np.array(image_closing * 255,dtype=np.uint8)
img = cv.medianBlur(img,5)
cimg = cv.cvtColor(img,cv.COLOR_GRAY2BGR)

circles = cv.HoughCircles(img,cv.HOUGH_GRADIENT,1.7,15,param1=1e-8,param2=20,minRadius=3,maxRadius=60)
circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    cv.circle(cimg,(i[0],i[1]),i[2],(255,0,0),10)

plt.subplot(1,2,1)
plt.imshow(cimg)
print(circles.shape[1])

particles = []
for i in circles[0,:]:
  rr, cc = circle(i[1],i[0],i[2])
  rr[rr>=img.shape[0]] = img.shape[0]-1
  cc[cc>=img.shape[1]] = img.shape[1]-1
  if np.count_nonzero(img[rr, cc]) / np.size(img[rr, cc]) > 0.6:
    img[rr, cc]=0
    particles.append(i)

plt.subplot(1,2,2)
plt.imshow(img)

plt.figure(figsize=[16,8])
print(len(particles))
digital_image = 0 * img
for i in particles:
  rr, cc = circle(i[1],i[0],i[2])
  rr[rr>=img.shape[0]] = img.shape[0]-1
  cc[cc>=img.shape[1]] = img.shape[1]-1
  digital_image[rr, cc]=1

plt.subplot(1,2,1)
plt.imshow(image)
plt.subplot(1,2,2)
plt.imshow(digital_image)
