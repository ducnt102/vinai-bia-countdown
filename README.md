Idea:

In the game of billiards, each person has 30 seconds to make their move.
Utilize OpenCV to detect the billiard balls stopping their motion and initiate a countdown for that turn.
Employ OpenCV for testing on a pre-existing video of a billiards table at VINAI.
Video test source:
https://youtu.be/gwCeGsTyMOA
Source code:
Derived code from the repository jitendrasb24/Motion-Detection-OpenCV.git
Process:
Capture images from the camera, identify the four corners of the table.
Only detect motions that resemble square-shaped balls and are within the table area.
The front-end (FE) retrieves data from the back-end (BE) to display the time and perform prompts when the time reaches the 10-second and 5-second milestones.
The back-end (BE) employs Flask and stores the variable count_down, executing functions such as add and reset through an API.
The OpenCV code utilizes ball detection logic and calls the API to interact with the back-end.
