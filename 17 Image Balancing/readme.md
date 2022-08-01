A simple algorithm that I came out, trying to eliminate disproportional lighting/shadows etc... 
pretty sure there's already some similar method out there but I do not know what name it would be.
It does not work on shadows as expected however it removes background gradient rather well.

thought process: Calculate the average value of each kernel and compare it with histogram average,
then add the value to the center kernel. the unbalance in the image would be compensated, smaller kernel size would result in greater changes.
