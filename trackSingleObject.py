import cv2
import sys
from helper_data import tract_dict, tracker_types
from tracker_api import *

#tract_dict - is a dictionary of all videos to process with preconfigured bounding box pixel coordinates
#tracker_types - list of all the OpenCV APIs we want to test and have an object initiator below






if __name__ == '__main__' :

    # Set up tracker.
    # Loop thru all the videos & corresponding corner pixels
    for tract in tract_dict:

        # Loop thru all the OpenCV trackers
        for tracker_type in tracker_types:

            # Then create a tracker object for which ever tracker is choosen 
            tracker = tracker_creater(tracker_type)

            # Read and create video writer object
            out, video = read_write_video(tract, tracker_type, tracker)


            # Continuously read and update video frame
            while True:
                # Read a new frame
                ok, frame = video.read()
                if not ok:
                    break

                # Update tracker
                ok, bbox = tracker.update(frame)

                # Update video frame with new perdicted bounding box
                frame = draw_on_frame(ok, bbox, frame, tracker_type)    


                outframe = cv2.resize(frame, (640,360))
                out.write(outframe)

                # Exit if ESC pressed
                k = cv2.waitKey(1) & 0xff
                if k == 27 : break
            out.release()
