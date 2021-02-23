# import the necessary packages, more files will be imported later
import apriltag
import argparse
import cv2
import requests
import sys



def readTag(image):
    id = None
    #convert img to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # define the AprilTags detector options and then detect the AprilTags
    # in the input image
    print("[INFO] detecting AprilTags...")
    options = apriltag.DetectorOptions(families="tag36h11")
    detector = apriltag.Detector(options)
    results = detector.detect(gray)
    print("[INFO] {} total AprilTags detected".format(len(results)))

    # loop over the AprilTag detection results
    for r in results:
        # extract the bounding box (x, y)-coordinates for the AprilTag
        # and convert each of the (x, y)-coordinate pairs to integers
        (ptA, ptB, ptC, ptD) = r.corners
        ptB = (int(ptB[0]), int(ptB[1]))
        ptC = (int(ptC[0]), int(ptC[1]))
        ptD = (int(ptD[0]), int(ptD[1]))
        ptA = (int(ptA[0]), int(ptA[1]))

        # draw the bounding box of the AprilTag detection
        cv2.line(image, ptA, ptB, (0, 255, 0), 2)
        cv2.line(image, ptB, ptC, (0, 255, 0), 2)
        cv2.line(image, ptC, ptD, (0, 255, 0), 2)
        cv2.line(image, ptD, ptA, (0, 255, 0), 2)

        # draw the center (x, y)-coordinates of the AprilTag
        (cX, cY) = (int(r.center[0]), int(r.center[1]))
        cv2.circle(image, (cX, cY), 5, (0, 0, 255), -1)

        # draw the tag family on the image
        tagFamily = r.tag_family.decode("utf-8")
        id = r.tag_id
        cv2.putText(image, tagFamily, (ptA[0], ptA[1] - 15),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        print("[INFO] tag family: {}".format(tagFamily))

    # show the output image after AprilTag detection
    cv2.imshow("Image", image)
    #cv2.waitKey(0) # uncomment this line (and comment below) to update frame with key press
    #Press q to turn of video, have to hold it so that it picks it up during the loop
    if cv2.waitKey(1)==ord('q'):
        cam.release()
        cv2.destroyAllWindows()
        
    #return id of read tags
    return id
    
                    


#This turns the cam format to a legible one.
# flipmethod = 0 leaves camera as is, flipmethod = 2 flips horizontal axis
camSet='nvarguscamerasrc sensor-id=0 ! video/x-raw(memory:NVMM), width=3264, height=2464, framerate=21/1, format=NV12 ! nvvidconv flip-method=2 ! video/x-raw, width=800, height=600, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink'
cam = cv2.VideoCapture(camSet)
x=5
while True:
    _, frame = cam.read()
    #cv2.moveWindow('my_cam', 0,0)
    id = readTag(frame)
    print("tag ID", id)
    #Currently only recognizes tags 0-3
    if id == 0:
        #If file not imported, attempt to import the proper file, if it doesn't work, download and import it. Finally, run
        if 'example_download' not in sys.modules:
            try:
                import example_download
            except ImportError:
                #raw of github urls
                url = "https://raw.githubusercontent.com/jwolf0/download/main/downloadfile.py"
                r = requests.get(url)
                with open("example_download.py",'wb') as f:
                    f.write(r.content)
                import example_download
                
        print(example_download.exfunc())

    elif id ==1:
        try:
            import example_download_1
        except ImportError:
            url = "https://raw.githubusercontent.com/jwolf0/download/main/example_download_1.py"
            r = requests.get(url)
            with open("example_download_1.py", 'wb') as f:
                f.write(r.content)
            import example_download_1
        for i in range(5):
            x = example_download_1.multiply_by_two(x)
        print(x)
        x=5

    elif id == 2:
        pass
    elif id ==3:
        pass
