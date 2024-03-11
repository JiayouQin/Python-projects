import torch
import torchvision.io
import torchvision.transforms.functional as F

import cv2 as cv
import numpy as np
# from torchvision.utils import flow_to_image
from torchvision.models.optical_flow import raft_large
import torchvision.transforms as T


def preprocess(batch):
    transforms = T.Compose([
            T.ConvertImageDtype(torch.float32),
            T.Normalize(mean=0.5, std=0.5),  # map [0, 1] into [-1, 1]
            T.Resize(size=(640, 384)),
        ]
    )
    batch = transforms(batch)
    return batch.to(device)


device = "cuda" if torch.cuda.is_available() else "cpu"
model = raft_large(pretrained=True, progress=False).to(device)
model = model.eval()

# Open the video file
video_path = "1.mp4"
cap = cv.VideoCapture(video_path)

# Store the track history
cv.namedWindow("image", cv.WINDOW_NORMAL)
# cv.namedWindow("flow image", cv.WINDOW_NORMAL)
failed = False

for i in range(1):
    success, frame = cap.read()
last_frame = preprocess(torch.from_numpy(frame.transpose(2,0,1)[None,:])) #needed for buffering

center = np.array((320,224),dtype=float)
while True:
    buffer_length = 2  #skip frames
    for i in range(buffer_length): 
        success, frame = cap.read()
        failed = False
        if not success:
            print('failed')
            failed = True
            continue
        # frame = cv.rotate(frame, cv.ROTATE_90_CLOCKWISE)
    if failed:
        break
        #processing starts here
    frame = cv.resize(frame, (640, 384))
    frameTensor = preprocess(torch.from_numpy(frame.transpose(2,0,1)[None,:]) ) #(N, C, H, W)
    list_of_flows = model(last_frame,frameTensor)
    predicted_flows = list_of_flows[-1]             #predicted_flows is a 2d vector field
    last_frame = frameTensor
    optical_flow = predicted_flows[0].permute(0,2,1)
    meanX = torch.mean(optical_flow[0]).detach().cpu().numpy()
    meanY = torch.mean(optical_flow[1]).detach().cpu().numpy()
    center[0] += meanX
    center[1] += meanY
    p1 = center + np.array([-30,-30]) 
    p2 = center + np.array([30,30]) 

    frame = cv.rectangle(frame,p1.astype(int), p2.astype(int), (0,0,255), 3)
        
    cv.imshow('image',frame)

    k = cv.waitKey(5)
    if k & 0xFF == 27:
        break

# Release the video capture object and close the display window
cap.release()
cv.destroyAllWindows()


