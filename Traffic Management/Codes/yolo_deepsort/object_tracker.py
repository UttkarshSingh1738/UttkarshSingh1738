import os
# comment out below line to enable tensorflow logging outputs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import time
import tensorflow as tf
physical_devices = tf.config.experimental.list_physical_devices('GPU')
if len(physical_devices) > 0:
    tf.config.experimental.set_memory_growth(physical_devices[0], True)
from absl import app, flags, logging
from absl.flags import FLAGS
import core.utils as utils
from core.yolov4 import filter_boxes
from tensorflow.python.saved_model import tag_constants
from core.config import cfg
from PIL import Image
import cv2
import numpy as np
import matplotlib.pyplot as plt
from tensorflow.compat.v1 import ConfigProto
from tensorflow.compat.v1 import InteractiveSession
# deep sort imports
from deep_sort import preprocessing, nn_matching
from deep_sort.detection import Detection
from deep_sort.tracker import Tracker
from tools import generate_detections as gdet
import datetime

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from plot_graph import plot_graphx
from dashboard import add_area

### custom open cv method for centroid tracking
from collections import deque




flags.DEFINE_string('framework', 'tf', '(tf, tflite, trt')
flags.DEFINE_string('weights', './checkpoints/yolov4-416',
                    'path to weights file')
flags.DEFINE_integer('size', 416, 'resize images to')
flags.DEFINE_boolean('tiny', False, 'yolo or yolo-tiny')
flags.DEFINE_string('model', 'yolov4', 'yolov3 or yolov4')
flags.DEFINE_string('video', './data/video/test.mp4', 'path to input video or set to 0 for webcam')
flags.DEFINE_string('output', None, 'path to output video')
flags.DEFINE_string('output_format', 'XVID', 'codec used in VideoWriter when saving video to file')
flags.DEFINE_float('iou', 0.45, 'iou threshold')
flags.DEFINE_float('score', 0.50, 'score threshold')
flags.DEFINE_boolean('dont_show', False, 'dont show video output')
flags.DEFINE_boolean('info', False, 'show detailed info of tracked objects')
flags.DEFINE_boolean('count', False, 'count objects being tracked on screen')




deque_len = 7
# framesx = 1


def main(_argv):
    # Definition of the parameters
    max_cosine_distance = 0.4
    nn_budget = None
    nms_max_overlap = 1.0
    
    # initialize deep sort
    model_filename = 'model_data/mars-small128.pb'
    encoder = gdet.create_box_encoder(model_filename, batch_size=1)
    # calculate cosine distance metric
    metric = nn_matching.NearestNeighborDistanceMetric("cosine", max_cosine_distance, nn_budget)
    # initialize tracker
    tracker = Tracker(metric)

    # load configuration for object detector
    config = ConfigProto()
    config.gpu_options.allow_growth = True
    session = InteractiveSession(config=config)
    STRIDES, ANCHORS, NUM_CLASS, XYSCALE = utils.load_config(FLAGS)
    input_size = FLAGS.size
    video_path = FLAGS.video


    ####### LOADING TFLITE MODEL ###################

    # load tflite model if flag is set
    if FLAGS.framework == 'tflite':
        interpreter = tf.lite.Interpreter(model_path=FLAGS.weights)
        interpreter.allocate_tensors()
        input_details = interpreter.get_input_details()
        output_details = interpreter.get_output_details()
        print(input_details)
        print(output_details)
    # otherwise load standard tensorflow saved model
    else:
        saved_model_loaded = tf.saved_model.load(FLAGS.weights, tags=[tag_constants.SERVING])
        infer = saved_model_loaded.signatures['serving_default']

    # begin video capture
    try:
        vid = cv2.VideoCapture(int(video_path))
    except:
        vid = cv2.VideoCapture(video_path)

    out = None



    ########### GETTING FPS + VIDEO DURATION INFO ############################

    #total fps information
    framesx = 1
    total_frames = vid.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = int(vid.get(cv2.CAP_PROP_FPS))
    print('total frames',total_frames,'fps',fps)
    # calculate duration of the video
    seconds = int(total_frames / fps)
    video_time = str(datetime.timedelta(seconds=seconds))#.total_seconds())
    print("duration in seconds:", seconds)
    print("video time:", video_time)



    ########################### DASHBOARD + CREATING VARIABLES FOR GRAPH (peak hour calculation) ##################
    res_logo = cv2.imread("./data/Updated_Logo@2x.jpg")
    dashboard_width = 1050

    frame_time = list(range(fps,(seconds*fps)+1,fps)) #creating a frame list
    hr_diff=[] #to create a 5 sec diff time interval
    for ft in range(1,(seconds//5)+1):
        hr_diff.append(ft*5)
    # print(hr_diff)

    count_df = pd.DataFrame({'time':[],"vehicle_count_in":[],"vehicle_count_out":[]})

    hr_df_diff = pd.DataFrame({"time_diff":[],"vehicle_in":[],"vehicle_out":[]})




    hr = 0 # will be used during sec calculation
    hrx = 0
    # print(frame_time)

    distancex = 20 ## to calculate speed

    ############################## CREATING VIDEO WRITER ###########################

    # get video ready to save locally if flag is set
    if FLAGS.output:
        # by default VideoCapture returns float instead of int
        width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(vid.get(cv2.CAP_PROP_FPS))
        codec = cv2.VideoWriter_fourcc(*FLAGS.output_format)
        out = cv2.VideoWriter(FLAGS.output, codec, fps, (width + dashboard_width, height))

    
    ########## variables for object tracking ################
    cent_dict = {} #to show trailing end
    cent_dict_count = [] # for vehicle count
    speed_df = pd.DataFrame({"vehicle_id":[],"time_in_1":[],"time_in_2":[],"time_out_1":[],"time_out_2":[],"time_diff":[],"speed":[]})
    carsin = 0
    carsout = 0

    frame_num = 0

    ############## LOOPING THROUGH THE VIDEO FRAME BY FRAME #########################
    # while video is running
    while True:

        rects = [] ##for open cv tracking
        return_value, frame = vid.read()
        if return_value:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
        else:
            print('Video has ended or failed, try a different video format!')
            break
        frame_num +=1
        print('Frame #: ', frame_num)
        cv2.putText(frame, "Frame #:" + str(frame_num) , (9, 75), cv2.FONT_HERSHEY_SIMPLEX, 1,  (0, 0,255), 2)


        frame_size = frame.shape[:2]
        image_data = cv2.resize(frame, (input_size, input_size))
        image_data = image_data / 255.
        image_data = image_data[np.newaxis, ...].astype(np.float32)
        start_time = time.time()

        # run detections on tflite if flag is set
        if FLAGS.framework == 'tflite':
            interpreter.set_tensor(input_details[0]['index'], image_data)
            interpreter.invoke()
            pred = [interpreter.get_tensor(output_details[i]['index']) for i in range(len(output_details))]
            # run detections using yolov3 if flag is set
            if FLAGS.model == 'yolov3' and FLAGS.tiny == True:
                boxes, pred_conf = filter_boxes(pred[1], pred[0], score_threshold=0.25,
                                                input_shape=tf.constant([input_size, input_size]))
            else:
                boxes, pred_conf = filter_boxes(pred[0], pred[1], score_threshold=0.25,
                                                input_shape=tf.constant([input_size, input_size]))
        else:
            batch_data = tf.constant(image_data)
            pred_bbox = infer(batch_data)
            for key, value in pred_bbox.items():
                boxes = value[:, :, 0:4]
                pred_conf = value[:, :, 4:]

        boxes, scores, classes, valid_detections = tf.image.combined_non_max_suppression(
            boxes=tf.reshape(boxes, (tf.shape(boxes)[0], -1, 1, 4)),
            scores=tf.reshape(
                pred_conf, (tf.shape(pred_conf)[0], -1, tf.shape(pred_conf)[-1])),
            max_output_size_per_class=50,
            max_total_size=50,
            iou_threshold=FLAGS.iou,
            score_threshold=FLAGS.score
        )

        # convert data to numpy arrays and slice out unused elements
        num_objects = valid_detections.numpy()[0]
        bboxes = boxes.numpy()[0]
        bboxes = bboxes[0:int(num_objects)]
        scores = scores.numpy()[0]
        scores = scores[0:int(num_objects)]
        classes = classes.numpy()[0]
        classes = classes[0:int(num_objects)]

        # format bounding boxes from normalized ymin, xmin, ymax, xmax ---> xmin, ymin, width, height
        original_h, original_w, _ = frame.shape
        bboxes = utils.format_boxes(bboxes, original_h, original_w)

        # store all predictions in one parameter for simplicity when calling functions
        pred_bbox = [bboxes, scores, classes, num_objects]

        # read in all class names from config
        class_names = utils.read_class_names(cfg.YOLO.CLASSES)

        # by default allow all classes in .names file
        # allowed_classes = list(class_names.values())
        
        # custom allowed classes (uncomment line below to customize tracker for only people)
        allowed_classes = ['car','motorbike','bus','truck']

        # loop through objects and use class index to get class name, allow only classes in allowed_classes list
        names = []
        deleted_indx = []
        for i in range(num_objects):
            class_indx = int(classes[i])
            class_name = class_names[class_indx]
            if class_name not in allowed_classes:
                deleted_indx.append(i)
            else:
                names.append(class_name)
        names = np.array(names)
        count = len(names)
        if FLAGS.count:
            cv2.putText(frame, "Objects being tracked: {}".format(count), (5, 35), cv2.FONT_HERSHEY_COMPLEX_SMALL, 2, (0, 255, 0), 2)
            print("Objects being tracked: {}".format(count))
        # delete detections that are not in allowed_classes
        bboxes = np.delete(bboxes, deleted_indx, axis=0)
        scores = np.delete(scores, deleted_indx, axis=0)

        # print('bbox', bboxes) 

        






        # encode yolo detections and feed to tracker
        features = encoder(frame, bboxes)
        detections = [Detection(bbox, score, class_name, feature) for bbox, score, class_name, feature in zip(bboxes, scores, names, features)]

        #initialize color map
        cmap = plt.get_cmap('tab20b')
        colors = [cmap(i)[:3] for i in np.linspace(0, 1, 20)]

        # run non-maxima supression
        boxs = np.array([d.tlwh for d in detections])
        scores = np.array([d.confidence for d in detections])
        classes = np.array([d.class_name for d in detections])
        indices = preprocessing.non_max_suppression(boxs, classes, nms_max_overlap, scores)
        detections = [detections[i] for i in indices]  


        if framesx in frame_time:
                    hr = frame_time.index(framesx) +1 #tracking time w.r.t. frames/seconds

        # print('bbox', boxs)     

        # Call the tracker
        tracker.predict()
        tracker.update(detections)

        # update tracks
        for track in tracker.tracks:
            if not track.is_confirmed() or track.time_since_update > 1:
                continue 
            bbox = track.to_tlbr()
            class_name = track.get_class()
            
        # draw bbox on screen
            color = colors[int(track.track_id) % len(colors)]
            color = [i * 255 for i in color]
            cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color, 2)
            cv2.rectangle(frame, (int(bbox[0]), int(bbox[1]-30)), (int(bbox[0])+(len(class_name)+len(str(track.track_id)))*17, int(bbox[1])), color, -1)
            cv2.putText(frame, class_name + "-" + str(track.track_id),(int(bbox[0]), int(bbox[1]-10)),0, 0.75, (255,255,255),2)


            # ########## object tracing trail ############

            objectIDx = str(track.track_id)
            cx = int(bbox[0]) +  int(((bbox[2])-(bbox[0]))/2) 
            cy = int(bbox[1]) + int(((bbox[3])-(bbox[1]))/2)




            centroidx = (cx,cy)
            # print("IDx", objectIDx,'------ Centroid', centroidx)
         

            #### creating a dictionary for vehicle count #######

            if centroidx not in cent_dict_count:
                cent_dict_count.append(centroidx)
            else:
                continue



            ############# vehicle SPEED calculation ############### {"vehicle_id":[],"time_in_1":[],"time_in_2":[],"time_out_1":[],"time_out_2":[],"time_diff":[],"speed":[]}

            cv2.line(frame, (1355,920), (1750,920), (0, 255, 0), 2) #out
            cv2.line(frame, (900,890), (1255,890), (255, 0, 0), 2) #in

            # if framesx in frame_time:
            #         hrob = frame_time.index(framesx) +1  ### calculating time w.r.t frames

            if objectIDx not in speed_df["vehicle_id"].values:

                # print("Entering into the first loop")
                # if (1120< cy < 1150 ) and (1255< cx < 1820):
                if (920< cy < 950 ) and (1355< cx < 1750):
                    # print("Creating speed_df_out_1 +++++++++******************")

                
                    #out
                    speed_df = speed_df.append({"vehicle_id":objectIDx,"time_in_1":0,"time_in_2":0,"time_out_1":hr,"time_out_2":0,"time_diff":0,"speed":0},ignore_index=True)
                    # print(speed_df)

                elif (890 < cy < 920) and (900 < cx < 1255 ):
                    #in
                     speed_df = speed_df.append({"vehicle_id":objectIDx,"time_in_1":hr,"time_in_2":0,"time_out_1":0,"time_out_2":0,"time_diff":0,"speed":0},ignore_index=True)

            elif objectIDx in speed_df["vehicle_id"].values :  ### to check wether a value is present inside a panda column: use ---> i in df['column'].values----  not--- i in df['column']
                                                                #### coz: df['column'] returns a series and (i in df['column']) will search availability of i in index not in values 
                # print('Entering else state')
                if (700 < cy < 730) and (1455 < cx < 1716):

                    # print(" Entering in to the final time stamp")
                    #out 

                    speed_df.loc[speed_df['vehicle_id']==objectIDx,"time_out_2"] = hr
                    speed_df.loc[speed_df['vehicle_id']==objectIDx,"time_diff"] = speed_df.loc[speed_df['vehicle_id']==objectIDx,"time_out_2"].iloc[0]-speed_df.loc[speed_df['vehicle_id']==objectIDx,"time_out_1"].iloc[0]
                    speed_df.loc[speed_df['vehicle_id']==objectIDx,"speed"] = (distancex/(speed_df.loc[speed_df['vehicle_id']==objectIDx,"time_diff"].iloc[0]))*3.6

                    # print(speed_df)
                   


                elif (1120< cy < 1150 ) and (600< cx < 1155):

                    ### in 
                    speed_df.loc[speed_df['vehicle_id']==objectIDx,"time_in_2"] = hr
                    speed_df.loc[speed_df['vehicle_id']==objectIDx,"time_diff"] = speed_df.loc[speed_df['vehicle_id']==objectIDx,"time_in_2"].iloc[0]-speed_df.loc[speed_df['vehicle_id']==objectIDx,"time_in_1"].iloc[0]
                    speed_df.loc[speed_df['vehicle_id']==objectIDx,"speed"] = (distancex/(speed_df.loc[speed_df['vehicle_id']==objectIDx,"time_diff"].iloc[0]))*3.6

                    # print(speed_df)
                  
                
                #### to show speed on screen
                if cy <= 730:
                    #out
                    cv2.putText(frame, "speed" + "-" + str(speed_df.loc[speed_df['vehicle_id']==objectIDx,"speed"].iloc[0]) + "km/h",(int(bbox[0]+110), int(bbox[1]-10)),0, 0.75, (0,0,255),2)
                elif cy >= 1120:
                    #in
                    cv2.putText(frame, "speed" + "-" + str(speed_df.loc[speed_df['vehicle_id']==objectIDx,"speed"].iloc[0]) + "km/h",(int(bbox[0]+110), int(bbox[1]-10)),0, 0.75, (0,0,255),2)
            
            
            #saving speed record
            speed_df.to_csv("./data/speed_df.csv",index=False) 

            


            ####### To show trailing line #####
            # ###### dictionary to store centroids of all detections according to perticular IDs ##

            # print(cent_dict) 
            # if objectIDx not in cent_dict:
            #     cent_dict[objectIDx] = deque(maxlen = deque_len) #maxlen=args["buffer"]
            # else:
            #     cent_dict[objectIDx].appendleft((centroidx[0], centroidx[1]))

            


            # # loop over the set of tracked points
            # # for idx in cent_dict.keys():

            # if track.is_confirmed():


            #     pts = cent_dict[objectIDx]

            #     for i in range(1, len(pts)):
            #         # print('printing points[i]>>>>>>>>>>', pts[i])
            #         # if either of the tracked points are None, ignore
            #         # them
            #         if pts[i - 1] is None or pts[i] is None:
            #             # print('printing points[i]>>>>>>>>>>', pts[i])
            #             continue

            #         # otherwise, compute the thickness of the line and
            #         # draw the connecting lines
            #         # thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
            #         color = list(np.random.random(size=3) * 256)
            #         cv2.line(frame, pts[i - 1], pts[i], color, thickness=5)
            #         # cv2.putText(frame,objectIDx,pts[i],0, 0.75, color,2)
            # elif track.is_deleted():
            #     continue

######################## vehicle counting #########################

        # cv2.line(frame, (206,200), (716,200), (0, 255, 0), 2) ### cars out
        # cv2.line(frame, (206,210), (716,210), (0, 255, 0), 2) ### cars out
        # cv2.line(frame, (720,320), (1275,320), (255, 0, 0), 2) ### cars in 
        # cv2.line(frame, (720,330), (1275,330), (255, 0, 0), 2) ### cars in  ####india.mp4


        cv2.line(frame, (1455,700), (1716,700), (0, 255, 0), 2) ### cars out
        cv2.line(frame, (1455,710), (1716,710), (0, 255, 0), 2) ### cars out
        cv2.line(frame, (600,1120), (1155,1120), (255, 0, 0), 2) ### cars in 
        cv2.line(frame, (600,1130), (1155,1130), (255, 0, 0), 2)  ############### client1




        # cv2.line(frame, (306,300), (716,300), (0, 255, 0), 2) ### cars out
        # cv2.line(frame, (306,310), (716,310), (0, 255, 0), 2) ### cars out
        # cv2.line(frame, (740,423), (1250,423), (255, 0, 0), 2) ### cars in 
        # cv2.line(frame, (740,433), (1250,433), (255, 0, 0), 2) ### cars in #### india2.MOV




        ############ vehicle counting #############
        for (cxx,cyy) in cent_dict_count:
             if (700 < cyy < 710) and (1455 < cxx < 1716):   ###715 for day
                    carsout += 1        
                    cent_dict_count.remove((cxx,cyy))
             elif (1120< cyy < 1150 ) and (600< cxx < 1155):
                     carsin = carsin + 1
                     cent_dict_count.remove((cxx,cyy))  ### client video

        # for (cxx,cyy) in cent_dict_count:
        #      if (300< cyy <303) and (306 < cxx < 710):
        #             carsout += 1
        #             cent_dict_count.remove((cxx,cyy))
        #      elif (423< cyy <426 ) and (740< cxx < 1295):
        #              carsin = carsin + 1
        #              cent_dict_count.remove((cxx,cyy))       #### india2.MOV
        # 
        # 
        # 
        ############################ DASHBOARD ###########################
        
        frame = add_area(frame,res_logo,dashboard_width)
         


        # cv2.rectangle(frame, (5, 4), (550, 300), (0,0,0), cv2.FILLED)             
     
        cv2.putText(frame, "Elapsed time: " + str(hr) + " seconds", (width + 19, 257 + 95), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255), 2) 

        cv2.putText(frame, "Vehicle in: " + str(carsin) + " (down)", (width + 17, 257 +  150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.putText(frame, "Vehicle out: " + str(carsout) + " (up)", (width + 19, 257 + 190), cv2.FONT_HERSHEY_SIMPLEX, 1,  (0, 255, 0), 2)

        

        ### avg density       
        
        avg_den_in = round((carsin / framesx),2)
        avg_den_out = round((carsout / framesx),2)
        
  
        
        cv2.putText(frame, "Avg. density in: " + str(avg_den_in) + " (down)", (width + 19, 257 +  245), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (255,0,0), 2)
        
        cv2.putText(frame, "Avg. density out: " + str(avg_den_out) + " (up)", (width + 19, 257 +  285), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0,255, 0), 2)                                                    ############# for client1.mp4
        

    #     cv2.rectangle(frame, (5, 4), (300, 150), (0,0,0), cv2.FILLED)
    #     # cv2.rectangle(frame, (5, 4), (250, 150), (0,0,0))               
     
          
    #     cv2.putText(frame, "Vehicle out: " + str(carsout) + " (up)", (9, 80), cv2.FONT_HERSHEY_SIMPLEX,0.5,  (0, 255, 0), 2)

    #     cv2.putText(frame, "Vehicle in: " + str(carsin) + " (down)", (7, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    #     ### avg density       
        
    #     avg_den_in = round((carsin / framesx),2)
    #     avg_den_out = round((carsout / framesx),2)
        
  
        
    #     cv2.putText(frame, "Avg. density in: " + str(avg_den_in) + " (down)", (9,110), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
    #                     (255,0,0), 2)
        
    #     cv2.putText(frame, "Avg. density out: " + str(avg_den_out) + " (up)", (9,140), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
    #                     (0,255, 0), 2)
        
        
    #     #tracking time
    #     # if framesx in frame_time:
    #     #     hr = frame_time.index(framesx) +1
    # #         print('HR',hr)

            
    #     cv2.putText(frame, "Elapsed time: " + str(hr) + " seconds", (9,25), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
    #                     (255,255,255), 2)                   ################# for indian2.MOV video



        count_df = count_df.append({'time':hr,'vehicle_count_in':carsin,'vehicle_count_out':carsout},ignore_index=True)  



        ############# PLOTTING HISTOGRAM  #################

        hrx=hr
        if hrx in hr_diff:
            hr_df_diff=hr_df_diff.append({"time_diff":str(hrx-5)+"-"+str(hrx),
                                            "vehicle_in":((count_df.loc[count_df['time'] == hrx,'vehicle_count_in'].iloc[0])-(count_df.loc[count_df['time'] == hrx-5,'vehicle_count_in'].iloc[0])),
                                            "vehicle_out":((count_df.loc[count_df['time'] == hrx,'vehicle_count_out'].iloc[0])-(count_df.loc[count_df['time'] == hrx-5,'vehicle_count_out'].iloc[0]))},ignore_index=True)

        # print(hr_df_diff)

        
        if len(hr_df_diff)>=5:
            frame = plot_graphx(hr_df_diff,"traffic",frame, width +19 ,620)
        #     frame = plot_graphx(hr_df_diff,"count_diff_out",frame,20,650)  #####df,y_name,frame,x_offset=400,y_offset=170

        # if len(hr_df_diff)>=5:
        #     frame = plot_graphx(hr_df_diff,"traffic",frame,5,150)
        #              ## for indian2.MOV video


            
            
        

        
        framesx +=1 #frame increment
               



        ############################ ***** ######################################3


        
        # objects = ct.update(rects)
        
        # for (objectID, centroid) in objects.items():
        #     if objectID not in cent_dict:

        


        # # if enable info flag then print details about each track
        #     if FLAGS.info:
        #         print("Tracker ID: {}, Class: {},  BBox Coords (xmin, ymin, xmax, ymax): {}".format(str(track.track_id), class_name, (int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3]))))

        # calculate frames per second of running detections
        fps = 1.0 / (time.time() - start_time)
        print("FPS: %.2f" % fps)
        result = np.asarray(frame)
        result = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        if not FLAGS.dont_show:
            cv2.imshow("Output Video", result)
        
        # if output flag is set, save video file
        if FLAGS.output:
            out.write(result)
        if cv2.waitKey(1) & 0xFF == ord('q'): break
    cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        app.run(main)
    except SystemExit:
        pass


##### python object_tracker.py --video ./data/video/client1.mp4 --output ./outputs/demo.avi --model yolov4