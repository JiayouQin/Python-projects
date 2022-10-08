import pyaudio
import wave
import numpy as np
import cv2 as cv

FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 1

 
audio = pyaudio.PyAudio()
 
# start Recording
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)
print( "recording...")


i=0
while True:
    data = stream.read(CHUNK)
    npData = np.frombuffer(data, np.int8)
    visualized = np.zeros((256,1024,3),np.uint8)
    freq_img = np.zeros((256,2049,3),np.uint8)
    magnitude = 128-int(np.average(np.absolute(npData)))
    
    for i in range(len(npData)-4):
        if i%4!=0:
            continue
        cv.line(visualized, (int(i/4),127+npData[i]), (int((i+4)/4),127+npData[i+4]), (0,255,0), 1) 
    cv.line(visualized, (0,magnitude), (1024,magnitude), (255,0,0), 1) 

    fourier = np.fft.rfft(npData)
    norm =  (np.abs(fourier)/100).astype(int)
    n = npData.size
    timestep = 1/43
    freq = np.fft.rfftfreq(n, d=timestep)
    
                          
    for i in range(len(norm)-4):
        cv.line(freq_img, (int(i),255), (int(i),255-norm[i]), (0,255,255), 1) 

    
    cv.namedWindow('Audio Visualizer',cv.WINDOW_NORMAL)
    cv.imshow('Audio Visualizer',visualized)
    cv.namedWindow('Frequency Visualizer',cv.WINDOW_NORMAL)
    cv.imshow('Frequency Visualizer',freq_img)
    k = cv.waitKey(5)
    if k == 27:
        break

stream.stop_stream()
stream.close()
audio.terminate()
cv.destroyAllWindows()
