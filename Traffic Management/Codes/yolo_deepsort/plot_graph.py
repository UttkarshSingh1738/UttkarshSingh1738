import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import argparse
import cv2
import seaborn as sns
import random


# def barh(ax):
    
#     for p in ax.patches:
#         val = p.get_height() #height of the bar
#         x = p.get_x()+ p.get_width()/2 # x- position 
#         y = p.get_x()+ p.get_height()-10 #y-position
#         ax.annotate(round(val,2),(x,y))
#         # print('Executing bar count top')

def plot_graphx(df,y_name,frame,x_offset=400,y_offset=170):
    # print(y_name)

    # sns.color_palette("hls", 8)
    plt.style.use('dark_background')
    # matplotlib.rc('axes',edgecolor='white')
    # plt.rcParams['text.color'] = 'r'
    # plt.rcParams['axes.ylabel.color'] = 'r'


    plt.figure(facecolor="#121512")
    

    plt.subplot(2,1,1,facecolor="#121512")
    barx =sns.barplot(x='time_diff',y="vehicle_in",data=df,palette="husl")
    barx.set_title('Peak Hour Traffic',color = 'white')
    
    # barh(barx)
    sns.lineplot(x='time_diff',y="vehicle_in",data=df)

    plt.subplot(2,1,2,facecolor="#121512")
    bary =sns.barplot(x='time_diff',y="vehicle_out",data=df,palette="husl")
    # barh(bary)
    sns.lineplot(x='time_diff',y="vehicle_out",data=df)

    plt.subplots_adjust(left=0.1,
                    bottom=0.1, 
                    right=0.9, 
                    top=0.9, 
                    wspace=0.4, 
                    hspace=0.4)




    plt.savefig(f'./data/graph_{y_name}.png')#,transparent=True)

    gr = cv2.imread(f'./data/graph_{y_name}.png')
    

    gr = cv2.resize(gr,(950,850)) 

    cv2.putText(gr, "Vehicle in", (gr.shape[1]-200,60), cv2.FONT_HERSHEY_SIMPLEX, 0.56, (255, 0, 0), 2)
    cv2.putText(gr, "Vehicle out", (gr.shape[1]-200,460), cv2.FONT_HERSHEY_SIMPLEX, 0.56,  (0, 255, 0), 2)

    frame[y_offset : y_offset + gr.shape[0], x_offset : x_offset + gr.shape[1]]= gr



    

    return frame



