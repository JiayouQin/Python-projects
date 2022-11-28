This is a algorithm for outer shape analysis targeting abrupt change, it could also be used for movement analysis (analysing anomalies of a circular movement for example) provided both x and y coordinates in discrete time series is given.
The main Idea is using fourier transformation and apply gaussian smooth on high frequency only, the low frequency components are unchanged.
This way the outer shape should be smoothened and by calculating each pixel distance of the smoothened discrete points to the original and thresholding given value, the sudden changes on high frequency components would be found, which usually are flaws.

![image](https://github.com/JiayouQin/Python-projects/blob/master/20%20Shape%20Analysis%20with%20FFT(OpenCV)/egg_flawed.jpg)
    this example will try to find an artificial flaw on an egg

![image](https://github.com/JiayouQin/Python-projects/blob/master/20%20Shape%20Analysis%20with%20FFT(OpenCV)/smoothy.png)
    this chart shows the discrete function of the shape after polar transformation and the smoothened function.
    by using inverse polar transformation the flaw could also be marked on the original picture.
