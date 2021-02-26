import cv2
import time

cap = cv2.VideoCapture(0)
ballrange1 = (20,100,100)
ballrange2 = (30, 255, 255)

while(True):
    isTrue, frame = cap.read()
    frame=cv2.resize(frame,(frame.shape[1]//2,frame.shape[0]//2))
    cv2.imshow('original',frame)    


    #process the frame
    process = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    process = cv2.GaussianBlur(process,(3,3),cv2.BORDER_CONSTANT)
    process = cv2.inRange(process, ballrange1, ballrange2)
    process = cv2.erode(process, None, iterations=2)
    process = cv2.dilate(process, None, iterations=2)
    #time.sleep(0.1)
    #cv2.imshow('frame1',process)
    cv2.imshow('frame2',process)
    
# find contours
	# (x, y) center of the ball
    cnts, h = cv2.findContours(process.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    center = None
    if len(cnts) > 0:
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
		# circle
        if radius > 20:
            cv2.circle(frame, (int(x), int(y)), int(radius),(0, 0, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 0), -1)
            #print(radius)
            cv2.putText(frame, "Estimated distance:{}".format(5*300/radius), (50,100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), thickness=4)
            
    cv2.imshow('original',frame)

    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        break
# Done
cap.release()
cv2.destroyAllWindows()