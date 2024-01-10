import numpy as np
import cv2


def add_area(frame, logo, width):
    frame_h, frame_w = frame.shape[0], frame.shape[1]
    logo = cv2.cvtColor(logo,cv2.COLOR_BGR2RGB)
    logo = cv2.resize(logo, (1010,215))
    black_area = np.zeros([frame.shape[0], width, 3], dtype=np.uint8)
    # black_area.fill(175)
    black_area.fill(20)
    frame = np.concatenate((frame, black_area), axis=1)
    frame[0:logo.shape[0], frame.shape[1] - logo.shape[1] -20 :frame.shape[1]-20] = logo

    cv2.putText(frame, "Vehicle Tracking System", (frame_w + (width//4), logo.shape[0]+50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255,255), 2)
    cv2.line(frame, (frame_w,logo.shape[0]+70),(frame_w+width,logo.shape[0]+70),(255,255,255),2)
    
    return frame
