import cv2
import sys
from helper_data import tract_dict, tracker_types

#tract_dict - is a dictionary of all videos to process with preconfigured bounding box pixel coordinates
#tracker_types - list of all the OpenCV APIs we want to test and have an object initiator below

#from dataPath import DATA_PATH


# Function to instantiate the OpenCV tracker object based on the name passed
def tracker_creater(api_name):

    # Then create a tracker object for which ever tracker is choosen 
    if api_name == 'BOOSTING':
        api_tracker = cv2.TrackerBoosting_create()
    elif api_name == 'MIL':
        api_tracker = cv2.TrackerMIL_create()
    elif api_name == 'KCF':
        api_tracker = cv2.TrackerKCF_create()
    elif api_name == 'MEDIANFLOW':
        api_tracker = cv2.TrackerMedianFlow_create()
    elif api_name == "CSRT":
        api_tracker = cv2.TrackerCSRT_create()
    elif api_name == "MOSSE":
        api_tracker = cv2.TrackerMOSSE_create()
    else:
        api_tracker = None
        print('Incorrect tracker name')
        print('Available trackers are:')
        for t in tracker_types:
          print(t)    

    return api_tracker      


def get_frames(vid_path):
    


if __name__ == '__main__' :

    # Set up tracker.
    # Choose one tracker

    #
#    tract_dict = {
#        'cycle': [(477, 254, 55, 152), 'videos/cycle.mp4'] ,
#        'ship': [(751, 146, 51, 78), 'videos/drone-ship.mp4'],
#        'hockey': [(129, 47, 74, 85), 'videos/hockey.mp4'],
#        'face2' : [(237, 145, 74, 88), 'videos/face2.mp4'],
#        'meeting_CSRT': [(627, 183, 208, 190), 'videos/meeting.mp4'],    #CSRT
#        'meeting_KCF': [(652, 187, 118, 123), 'videos/meeting.mp4'],      #KCF
#        'surfing': [(97, 329, 118, 293), 'videos/surfing.mp4'],
#        'surf': [(548, 587, 52, 87), 'videos/surf.mp4'],
#        'spinning_red': [(232, 218, 377, 377), 'videos/spinning.mp4'],       #RED
#        'spinning_blue': [(699, 208, 383, 391), 'videos/spinning.mp4'],        #BLUE
#        'car': [(71, 457, 254, 188), 'videos/car.mp4']
#    } 


#    tracker_types = ['BOOSTING', 'MIL','KCF', 'MEDIANFLOW', 'CSRT', 'MOSSE']





    # Loop thru all the videos & corresponding corner pixels
    for tract in tract_dict:



        # Loop thru all the OpenCV trackers
        for tracker_type in tracker_types:

            tracker = tracker_creater(tracker_type)

            # Then create a tracker object for which ever tracker is choosen 
#            if tracker_type == 'BOOSTING':
#                tracker = cv2.TrackerBoosting_create()
#            elif tracker_type == 'MIL':
#                tracker = cv2.TrackerMIL_create()
#            elif tracker_type == 'KCF':
#                tracker = cv2.TrackerKCF_create()
#            elif tracker_type == 'MEDIANFLOW':
#                tracker = cv2.TrackerMedianFlow_create()
#            elif tracker_type == "CSRT":
#                tracker = cv2.TrackerCSRT_create()
#            elif tracker_type == "MOSSE":
#                tracker = cv2.TrackerMOSSE_create()
#            else:
#                tracker = None
#                print('Incorrect tracker name')
#                print('Available trackers are:')
#                for t in tracker_types:
#                  print(t)


            # Read video

            filename = tract_dict[tract][1]

            cap = cv2.VideoCapture(filename)
            video_name = filename.split('/')[-1].split('.')[0]
            video = cv2.VideoCapture(filename)
            frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

            # Exit if video not opened.
            if not video.isOpened():
                print("Could not open video")
                sys.exit()

            # Read first frame.
            ok, frame = video.read()
            if not ok:
                print('Cannot read video file')
                sys.exit()


            # Define an initial bounding box

            bbox = tract_dict[tract][0]


            # Uncomment the line below to select a different bounding box
            # bbox = cv2.selectROI(frame, False)
            print("Initial bounding box : {}".format(bbox))
            # Initialize tracker with first frame and bounding box
            ok = tracker.init(frame, bbox)
            out = cv2.VideoWriter('out_videos/{}_{}_{}.mp4'.format(video_name,tracker_type,bbox),cv2.VideoWriter_fourcc(*'MP4V'), 30, (640,360))

            while True:
                # Read a new frame
                ok, frame = video.read()
                if not ok:
                    break

                # Start timer
                timer = cv2.getTickCount()

                # Update tracker
                ok, bbox = tracker.update(frame)

                # Calculate Frames per second (FPS)
                fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);

                # Draw bounding box
                if ok:
                    # Tracking success
                    p1 = (int(bbox[0]), int(bbox[1]))
                    p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                    cv2.rectangle(frame, p1, p2, (0,255,0), 2, 1)
                else :
                    # Tracking failure
                    cv2.putText(frame, "Tracking failure detected", (20,120), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2, cv2.LINE_AA)

                # Display tracker type on frame
                cv2.putText(frame, tracker_type + " Tracker", (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0),2, cv2.LINE_AA);

                # Display FPS on frame
                cv2.putText(frame, "FPS : " + str(int(fps)), (20,80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA);


                # Display result
#                cv2.imshow("Tracking", frame)

                outframe = cv2.resize(frame, (640,360))
                out.write(outframe)

                # Exit if ESC pressed
                k = cv2.waitKey(1) & 0xff
                if k == 27 : break
            out.release()
