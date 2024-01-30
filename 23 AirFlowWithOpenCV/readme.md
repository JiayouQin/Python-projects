![](https://github.com/JiayouQin/Python-projects/blob/master/pictures/particle.gif?raw=true)

Basic air flow simulation
Frame work used: OpenCV
each pixel represent a unit with intensity indicates it's air volume or density. In this demo each 4 direction of gradient is calculated and only the direction with max gradient will exchange air.
the gradient in this demo represents air speed. A parameter friction and propagation could be set.(propagation only affect volume exchanged, each iteration only nearby pixel exchange values)
