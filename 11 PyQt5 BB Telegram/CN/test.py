# import the opencv library
import cv2
import numpy as np
import zlib

# define a video capture object
vid = cv2.VideoCapture(0)


def run():
    # Capture the video frame
    # by frame
    ret, frame = vid.read()
    h,w,c=frame.shape
    some_var=frame.tobytes()
    compressed_data = zlib.compress(some_var)

    decompressed_byte_data = zlib.decompress(compressed_data)
    print(f'{len(compressed_data)/1024} Kb/frame')
    print(f'{len(some_var)/1024} Kb/frame')
    
    nparr = np.fromstring(decompressed_byte_data, np.uint8).reshape(h,w,c)
    cv2.imshow('frame', nparr)

    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    
while(True):
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    
    run()

  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()