A simple algorithm that I came out, trying to eliminate disproportional lighting/shadows etc... 
pretty sure there's already some similar method out there but I do not know what name it would be.
It does not work on shadows as expected however it removes background gradient rather well.

thought process: Calculate the average value of each kernel and compare it with histogram average,
then add the value to the center kernel. the unbalance in the image would be compensated, smaller kernel size would result in greater changes.

Because I'm lazy this code uses a library that I have written, it loads all images in the current path and I can write less code with it.
If you do not like this simply replace the code with (cvs.) with default openCV code.

to use this library use:

pip install cvsimpleton  --upgrade

![](https://github.com/JiayouQin/Python-projects/blob/master/pictures/17%20Image%20Balancing/1.png)
![](https://github.com/JiayouQin/Python-projects/blob/master/pictures/17%20Image%20Balancing/2.png)
![](https://github.com/JiayouQin/Python-projects/blob/master/pictures/17%20Image%20Balancing/3.png)
![](https://github.com/JiayouQin/Python-projects/blob/master/pictures/17%20Image%20Balancing/5.png)
