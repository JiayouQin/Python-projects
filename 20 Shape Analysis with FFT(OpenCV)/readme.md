This is a algorithm for outer shape analysis targeting abrupt change, it could also be used for movement analysis (analysing anomalies of a circular movement for example) provided both x and y coordinates in discrete time series is given.
The algorithem works well if the shape and flaw exist on distinctive different frequency domain.
The main Idea is using fourier transformation and apply gaussian smooth on high frequency only, the low frequency components are unchanged.
In this example the egg mainly consists of low frequency component and the flaw is only high frequency component.
This way the outer shape should be smoothened and by calculating each pixel distance of the smoothened discrete points to the original and thresholding given value, the sudden changes on high frequency components would be found, which usually are flaws.
Notice the smoothened function does not represent ideal function without the flaw but rather a approximation, the flaw itself will leave residues after smoothened.

![image](https://github.com/JiayouQin/Python-projects/blob/master/20%20Shape%20Analysis%20with%20FFT(OpenCV)/egg_flawed.jpg)
    this example will try to find an artificial flaw on an egg

![image](https://github.com/JiayouQin/Python-projects/blob/master/20%20Shape%20Analysis%20with%20FFT(OpenCV)/smoothy.png)
    this chart shows the discrete function of the shape after polar transformation and the smoothened function.
    by using inverse polar transformation the flaw could also be marked on the original picture.
