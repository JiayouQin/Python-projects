import numpy as np
from scipy.ndimage import gaussian_filter1d
import matplotlib.pyplot as plt
import cv2 as cv

img = cv.imread('egg.jpg',0)
h, w = img.shape[:2]


ret,thresh = cv.threshold(img,200,255,cv.THRESH_BINARY_INV)

contours, hierarchy = cv.findContours(thresh, cv.RETR_LIST, cv.CHAIN_APPROX_NONE)
M = cv.moments(contours[0])
center = (int(M["m10"] / M["m00"]),int(M["m01"] / M["m00"]))
print(f'found center: {center}')

pol = cv.warpPolar(thresh,(h*2,w*2),center,h,cv.WARP_POLAR_LINEAR| cv.WARP_FILL_OUTLIERS)
pol = cv.rotate(pol, cv.ROTATE_90_CLOCKWISE)



contours, hierarchy = cv.findContours(pol, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
contour_image = np.zeros((h*2,w*2))
cv.drawContours(contour_image, contours, contourIdx=-1, color=255,thickness=1)
discrete_function = np.zeros(w*2).astype(float)

#get max value
for pts in contours[0]:
	x,y = pts[0]
	if y > discrete_function[x]:
		discrete_function[x] = y

cv.namedWindow('img',cv.WINDOW_NORMAL)
cv.namedWindow('pol',cv.WINDOW_NORMAL)
cv.namedWindow('contImage',cv.WINDOW_NORMAL)
cv.namedWindow('thresh',cv.WINDOW_NORMAL)
cv.imshow('img',img)
cv.imshow('thresh',thresh)
cv.imshow('contImage',contour_image)
cv.imshow('pol',pol)
cv.waitKey(0)
# exit()



sp = np.fft.fft(discrete_function)
freq = np.fft.fftfreq(discrete_function.size)
# plt.plot(freq, sp.real, freq, sp.imag)
# plt.plot(sp)
l,h = 30,int(len(sp)/2)
sp_gauss = sp.copy()
sp_gauss[l:h] = gaussian_filter1d(sp[l:h], 1)
sp_gauss[-h:-l] = gaussian_filter1d(sp[-h:-l], 1)

ifft = np.fft.ifft(sp)
ifft2 = np.fft.ifft(sp_gauss)

# plt.plot(freq, sp.real, freq, sp.imag)
plt.plot(freq, sp_gauss.real, freq, sp_gauss.imag)
plt.show()
plt.plot(ifft)
plt.plot(ifft2)
plt.show()
diviation = ifft - ifft2
plt.plot(diviation)
plt.show()