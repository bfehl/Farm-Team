# import the necessary packages
from collections import deque
import serial
import numpy as np
import argparse
import cv2
import imutils
import time


# define the lower and upper boundaries
# ball in the HSV color space, then initialize the
# list of tracked points




lower = (76, 63, 83)
upper = (101, 168, 176)
buffer = 20
pts = deque(maxlen=buffer)

#save real object rad. for distance calc3
#real_radius = 2.5in/2
#we need in px
real_radius = 240/2


#start cam & give time to warm up
camSet='nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM), width=3264, height=2464, framerate=21/1, format=NV12 ! nvvidconv flip-method=2 ! video/x-raw, width=800, height=600, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam = cv2.VideoCapture(camSet)
time.sleep(2)


#start serial comms
robot = serial.Serial('/dev/ttyUSB0', 9600)
drive_state = 0


#create functions to handle movement
'''
0=stop
1=forward
2=left
3=right
4=reverse
'''

def stop():
    global drive_state, robot
    if drive_state !=0:
        try:
            robot.write(b'0')
            drive_state = 0
        except Exception as e: print(e)

def forward():
    global drive_state, robot
    if drive_state!=1:
        try:
            robot.write(b'1')
            drive_state=1
        except Exception as e: print(e)

def left ():
    global drive_state, robot
    if drive_state!=2:
        try:
            robot.write(b'2')
            drive_state=2
        except Exception as e: print(e)

def right():
    global drive_state, robot
    if drive_state!=3:
        try: 
            robot.write(b'3')
            drive_state = 3
        except Exception as e: print(e)

def reverse():
    global drive_state, robot
    if drive_state!=4:
        try:
            robot.write(b'4')
            drive_state=4
        except Exception as e: print(e)







counter = 0
while True:
    _, frame = cam.read()

    # resize the frame, blur it, and convert it to the HSV
	# color space
    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "blue", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
	# (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None


    
    	# only proceed if at least one contour was found
    if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        #calculate and print distance
        
        '''
        1in = 96px
        at 8inches, ball interperated radius is 65px. 8inch = 768px
        cam_interpreted_size = real_size*focal_len/dist
        cam_interpreted * dist / realsize = focal_len
        focal_len = (65 * 768)/real_radius
        I exeperimentally got 416px
        '''

        focal_len = 416
        dist = (real_radius * focal_len)/radius
        inches = dist/96
        #print(inches, "inches") #This is super rough since the enclosing circle isnt always perfect, but I dont think theres really a fix for that


        # only proceed if the radius meets a minimum size
        if radius >= 4:
			# draw the circle and centroid on the frame
			# then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
            
            '''
            Drive based off of distance, and where in the screen reigon the ball is
            waits until at least 10 loops have been completed so that theres actually
            time to perform inputs
            '''

            #screen width = 600
            #if x is in center 3/5, go forward
            if inches <= 12:
                stop()
                print("ball captured")

            elif x >= 120 and x <= 480:
                forward()
                print("forward")
                    
            #if to left 5th, turn left
            elif x < 120:
                left()
                print('left')

            #if to the right, turn right
            elif x > 480:
                right()
                print('right')

            print(drive_state)

        #if radius <
        else:
            #if no ball, stop
            stop()
            print('STOP radius doesnt exist')


	# update the points queue
    pts.appendleft(center)

    	# loop over the set of tracked points
    for i in range(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
        if pts[i - 1] is None or pts[i] is None:
            continue
		# otherwise, compute the thickness of the line and
		# draw the connecting lines
        thickness = int(np.sqrt(buffer / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

	# show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF



    #press q to quit
    if cv2.waitKey(1)==ord('q'):
        robot.write(b'0')
        cam.release()
        cv2.destroyAllWindows()
        
