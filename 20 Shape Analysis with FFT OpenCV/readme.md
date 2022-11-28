This is a algorithm for outer shape analysis(flaw detection), it could also be used for movement analysis 
(analysing anomalies of a circular movement for example, provided both x and y coordinates in discrete time series were given.) 
The algorithem works well if there is a clear gap on the frequecy domain of the shape and the flaw.
The main idea is using fourier transformation and apply gaussian smooth on high frequency only, the low frequency components are unchanged.
In this example the egg mainly consists of low frequency component and the flaw is only high frequency component.
By calculating each pixel distance between the smoothened discrete points and the original and thresholding given value, the sudden changes on high frequency components can be found, which usually are flaws.
Notice the smoothened function does not represent the ideal function without the flaw but rather an approximation, the flaw itself will leave residues after smoothened.

![image](https://github.com/JiayouQin/Python-projects/blob/master/20%20Shape%20Analysis%20with%20FFT%20OpenCV/egg_flawed.jpg)
    this example will try to find an artificial flaw on an egg

![image](https://github.com/JiayouQin/Python-projects/blob/master/20%20Shape%20Analysis%20with%20FFT%20OpenCV/smoothy.jpg)
    this chart shows the discrete function of the shape after polar transformation and the smoothened function.
    by using inverse polar transformation the flaw could also be marked on the original picture.
