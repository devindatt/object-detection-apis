import cv2
import sys
from helper_data import tract_dict, tracker_types


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



def err_handling(vid):

    # Exit if video not opened.
    if not vid.isOpened():
        print("Could not open video")
        sys.exit()

    # If video is good then read first frame.
    ok, frame = vid.read()
    if not ok:
        print('Cannot read video file')
        sys.exit()    

    return frame    



def read_write_video(tract_idx, api_name, api_object):
    # Read video

    filename = tract_dict[tract_idx][1]

    cap = cv2.VideoCapture(filename)
    video_name = filename.split('/')[-1].split('.')[0]
    video = cv2.VideoCapture(filename)
#    frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
#    frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Confirm if video object is valid
    frame = err_handling(video)

    # Define an initial bounding box
    bbox = tract_dict[tract_idx][0]

    # Uncomment the line below to select a different bounding box
    # bbox = cv2.selectROI(frame, False)
    print("Initial bounding box : {}".format(bbox))
    # Initialize tracker with first frame and bounding box
    ok = api_object.init(frame, bbox)
    out = cv2.VideoWriter('out_videos2/{}_{}_{}.mp4'.format(video_name,api_name,bbox), cv2.VideoWriter_fourcc(*'MP4V'), 30, (640,360))

    return out, video


def draw_on_frame(stat, pts, frm, api_name):

        # Start timer
    timer = cv2.getTickCount()

    # Calculate Frames per second (FPS)
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);

    # Draw bounding box
    if stat:
        # Tracking success
        p1 = (int(pts[0]), int(pts[1]))
        p2 = (int(pts[0] + pts[2]), int(pts[1] + pts[3]))
        cv2.rectangle(frm, p1, p2, (0,255,0), 2, 1)
    else :
        # Tracking failure
        cv2.putText(frm, "Tracking failure detected", (20,120), cv2.FONT_HERSHEY_SIMPLEX, 1,(0,0,255),2, cv2.LINE_AA)

    # Display tracker type on frame
    cv2.putText(frm, api_name + " Tracker", (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0),2, cv2.LINE_AA);

    # Display FPS on frame
    cv2.putText(frm, "FPS : " + str(int(fps)), (20,80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2, cv2.LINE_AA);


    # Display result
#                cv2.imshow("Tracking", frame)

    return frm
