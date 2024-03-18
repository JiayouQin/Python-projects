Video Stabilizer based on SIFT

![](https://github.com/JiayouQin/Python-projects/blob/master/28%20SIFT%20Stablizer/Sift%20Stablizer.gif?raw=true)
![](https://github.com/JiayouQin/Python-projects/blob/master/28%20SIFT%20Stablizer/psc.gif?raw=true)
Using SIFT feature extraction and brute force feature matching to calculate pixel shift</br>
cv.estimateAffine2d is used to achieve stabilization.</br>
For real application purpose, some smoothing function could be implemented for the lock-on center so the camera could move around.</br>

higher accuracy than previous optical flow test:</br>
https://github.com/JiayouQin/Python-projects/tree/master/25%20Optical%20Flow%20Stablizer
