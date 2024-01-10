import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import cv2
import seaborn as sns
import random



capture = cv2.VideoCapture("./data/video/client1.mp4")
df = pd.DataFrame({'time':[],"vehicle_count":[],"time_diff":[]})
df_diff = pd.DataFrame({"time_diff":[],"count_diff":[]})
# for i in range(10):
#     df = df.append({'time':i,'vehicle_count':i+5},ignore_index=True)


i=0
k=0
x_offset = 400
y_offset = 170  
# Grab, process, and display video frames. Update plot line object(s).
while True:
    (grabbed, frame) = capture.read()

    if not grabbed:
        break

    j = random.randint(1,100)

    df = df.append({'time':i,'vehicle_count':i+j},ignore_index=True)

    # if i >5:
    #     df_tail = df.iloc[-5:]
    # else:
    #     df_tail = df

    if i>=5:
        for k in range(5,len(df))






    
    sns.lineplot(x='time_diff',y='vehicle_count',data=df)
    sns.set_title('Peak Hour Traffic')
    # plt.show()
    plt.savefig('./data/graph.png',transparent=True)



    gr = cv2.imread("./data/graph.png")
    gr = cv2.resize(gr,(500,300))
    # roi = frame[y_offset:470, x_offset:700] 

    # gr_gray = cv2.cvtColor(gr, cv2.COLOR_RGB2GRAY)
    # ret, mask = cv2.threshold(gr_gray , 120, 255, cv2.THRESH_BINARY)
    # bg = cv2.bitwise_or(roi,roi,mask = mask)
    # mask_inv = cv2.bitwise_not(gr_gray)
    # fg = cv2.bitwise_and(gr,gr, mask=mask_inv)

    # small_img = cv2.add(bg,fg)
    small_img = gr
    frame[y_offset : y_offset + small_img.shape[0], x_offset : x_offset + small_img.shape[1]]= small_img

    # print(gr.shape)
    # frame = cv2.addWeighted(frame, 0.5, gr, 0.5, 0)
    # frame[0:480,0:640,:] = gr
    # i +=1
    print(df)




    cv2.imshow("Traffic video",frame)

    


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

capture.release()
cv2.destroyAllWindows()





