# OpenCV Object Tracking Algorithms

[![N|Solid](https://i.ibb.co/Yppkvtr/obj-tracking-apis-comp1.gif)](https://github.com/devindatt/object-detection-apis/blob/master/Assets/_obj_tracking_apis_comp1.gif)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

This is an analysis to compare SIX of OpenCV top Object Detecting APIs listedbelow: 

Algorithms OpenCV 4.1.0

1) BOOSTING
2) Multiple Instance Learning ( MIL )
3) Kernelized Correlation Filters (KCF)
4) MedidanFlow
5) MOSSE
6) CSRT

##### Note:
I didn't analyze the these API's for the following reasons:
**TLD** - too many false positives, and tracking was poor in real file applications
**GOTURN** - has some implementation troubles within OpenCV & Python



#
#

#### Occlusion 

- **CSRT** works better when the bounding box is larger and ‘looser'
- **KCF** works better when the bounding box is smaller and tighter
- problems: if object path is not linear (I.e. going in a circle) or appearance is changing

    ##### Partial:
    - **CSRT** is very stable and accurate but slow
	- **KCF** & **MOSSE** get unreliable when occluded for large time
	
    ##### Full: 
	- **CSRT, MOSSE & KCF** can recover when image is fully occluded
	- **MedidanFlow** only good if application has low change of occlusions 

    ##### Scaling:
	- **CSRT & MedidanFlow** good can handle when object is scaling, boxes can scales up or down
	- ALL trackers - can deal with small changes or deformations in object when tracking


### Summary:

If application needs high accuracy, stability, but not speed ==> use **CSRT**

If Speed is ***critical***:
	- If speed is needed then accuracy ==> use **KCF & MOSSE**
	- If you need to handle large occlusion or scale variations ==> just use **KCF**
	- If object has linear motion and large variations in scale (ie. tracking cars) ==> use **MedidanFlow**


### Installation:

Assumptions:
    - You have OpenCV v4 installed
    - The source video files are in the '/video' directory
    - Output files will be put in the '/out_videos' directory
    
Open your favorite Terminal and run these commands.

First Tab:
```sh
$ python trackSingleObject.py
```
### Analysis Video Links:
Video 1: https://youtu.be/kC6wLmi3uJ4 (rotating coloured balls)
Video 2: https://youtu.be/YNuFLO_XpSY (surfer)
Video 3: https://youtu.be/-ER9L-xuJWU (hockey players)
Video 4: https://youtu.be/W6quLX6axWo (cyclist)
Video 5: https://youtu.be/El4rbiTH5KI (van moving away)

