Piston Simulation with air particles

![](https://github.com/JiayouQin/Python-projects/blob/master/26%20Piston%20with%20air%20particles/piston%20short.gif?raw=true)

Cellular Automata on steroids.
This is still a naive implementation and does in no way represent any physical simulation.
OpenCV is used for the implementation, runs in real-time on CPU, and could also be accelerated with GPU up to about 15 times.
The calculation is density-based, gradients are calculated using density in 4 directions, air will flow according to the gradient, and flow speed is retained.
Friction is used as the expression so airflow would smoothen over time. 
if set t0 0.5 the particle will be extremely unlikely to smoothen out.
