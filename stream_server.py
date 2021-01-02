'''-------------------------------------------------------------------
@Name: stream_server.py
@Description: This file gets the image from the Google Glass camera as
	well as the positions obtained through track.py file.
	It also represents the images in OpenCV and the ellipse with positions
	and recs the session and stores it on the database and the filesystem
@Author: Rubén Muñoz Solera
-----------------------------------------------------------------------'''
import argparse
from Tkinter import *
import Image
import ImageTk
from PIL.ImageTk import *
import Tkinter
import wearscript
import base64
import cStringIO
import cv2
import cv
import numpy as np
import time
import dbEyeTracker as dbEye
import os
import datetime


def main():
    def callback(ws, **kw):

        global save_data
        save_data = False

        '''
        This method gets the mouse's click in order to save the data or not.
        '''
        def my_mouse_callback(event, x, y, flags, param):
            global save_data
            print "Estoy dentro de la funcion del click"
            if event == cv.CV_EVENT_LBUTTONDBLCLK:  # here event is left mouse button double-clicked
                save_data = not save_data

    	'''
        This method gets the mouse's click in order to save the data or not.
        '''
        def get_image(chan, timestamp, image):
            print('Image[%s] Time[%f] Bytes[%d]' % (chan, timestamp, len(image))) #gets the image parameters from subscribe's method
            global refresh
            global image_dec

            if refresh:
                img_stream_str = cStringIO.StringIO(base64.b64decode(image)) #Decode de image codified in base64 and store it on img_stream_str
                img_array = np.asarray(bytearray(img_stream_str.read()), dtype=np.uint8) #obtain the bytes from the image decodified
                image_dec = cv2.imdecode(img_array, cv2.CV_LOAD_IMAGE_COLOR)#Load the image
                image_dec = cv2.resize(image_dec, (640, 360))#resize to the window's size
                
        '''
        This method includes the position's logic  and the data obtained through the subscribe method at the bottom of this file.
        '''
        def get_sensors(chan, names, result):
            print('Sensors[%s] Names[%r] Samples[%r]' % (chan, names, result))
            x = xreal = y = yreal = yref = ratio = area = radius = time1 = time2 = 0.0 #Variable declaration
            xtemp = 0
            ytemp = 0
            global image_dec, db, path, key_session
            eyeTrackerValues = result['Pupil Eyetracker'][0][0] #Positions X, Y
            x = eyeTrackerValues[0] # X
            y = eyeTrackerValues[1] # Y
            ratio = eyeTrackerValues[2] # ratio
            area = eyeTrackerValues[3] # area
            radius = eyeTrackerValues[4] # radius
            time1 = result['Pupil Eyetracker'][0][1] #Time 1
            time2 = result['Pupil Eyetracker'][0][2] #Time 2
            xint = int(round(x))
            yint = int(round(y))
            '''### X Position Logic ###'''
            xmax = kw.get('xmax') # gets the xmax parameter
            xmin = kw.get('xmin') # gets the xmin parameter
            ymax = kw.get('ymax') # gets the ymax parameter
            ymin = kw.get('ymin') # gets the ymax parameter

            #Calculate the position on the window
            xdiff = xmax - xmin
            ydiff = ymax - ymin
            xtemp = xmax - xint
            ytemp = yint - ymin

            # X limitations
            if xtemp <= 0:
                xtemp = 1
            elif xtemp >= xdiff:
                xtemp = xdiff
            xreal = (xtemp * 640) / xdiff

            '''### Y Position Logic ###'''
            # Y limitations
            if ytemp <= 0:
                ytemp = 1
            elif ytemp >= ydiff:
                ytemp = ydiff
            yreal = (ytemp * 360) / ydiff # Position Calculated
            print("x: [%d]" % (x))
            print("y: [%d]" % (y))
            print("xreal: [%d]" % (xreal))
            print("yreal: [%d]" % (yreal))

            myclone = cv2.copyMakeBorder(image_dec, 0, 0, 0, 0, cv2.BORDER_DEFAULT) #Clone the image to replace the old one each time a position is gotten
            image_view = myclone
            xresult = int(round(xreal))
            yresult = int(round(yreal))
            cv2.ellipse(image_view, (xresult, yresult), (50, 20), 0, 0, 360, (0, 255, 0), -1) #It draws the ellipse
          	
          	#The following shows the strings with the eye positions
            font = cv2.FONT_ITALIC
            texrx = str(int(x))
            texry = str(int(y))
            textxf = str(xresult)
            textyf = str(yresult)
            cv2.putText(image_view, 'Final X: ' + textxf, (10, 320), font, 0.6, (255, 255, 255), 2)
            cv2.putText(image_view, 'Final Y: ' + textyf, (10, 350), font, 0.6, (255, 255, 255), 2)
            cv2.putText(image_view, 'Pos X: ' + texrx, (150, 320), font, 0.6, (255, 255, 255), 2)
            cv2.putText(image_view, 'Pos Y: ' + texry, (150, 350), font, 0.6, (255, 255, 255), 2)

            #If save_data = True insert into the database the eye parameters as well as the image on the filesystem.
            #Besides, draw the REC figure on the window
            if (save_data):
                imagepath = datetime.datetime.now().strftime("%Y%m%d%H%M%S.jpg")
                cv2.imwrite(path + '/%s' % (imagepath,), image_view)
                inserted_data = dbEye.insert_eye_data(db, xresult, yresult, radius, ratio, key_session, path, imagepath,
                                                      640, 360, 0)
                cv2.circle(image_view, (565, 15), 10, (0, 0, 255), -1)
                cv2.putText(image_view, 'REC', (580, 20), font, 0.6, (255, 255, 255), 2)

            cv2.namedWindow("Descodificada")
            cv2.setMouseCallback("Descodificada", my_mouse_callback)
            print "Double click selected"

            #SHOW THE MAIN WINDOW
            cv2.imshow("Descodificada", image_view)
            time.sleep(0.5)
            #Wait enought till getting the next position
            key = cv2.waitKey(400)
            if key == 27:
                refresh = False
            elif key == 13:
                refresh = True

         #The subscribe methods that gets the image and position from publish ones.
        ws.subscribe('image', get_image)
        ws.subscribe('sensors', get_sensors)
        print "INIT"
        ws.handler_loop()
        print "END"

    parser = argparse.ArgumentParser()
    parser.add_argument('--xmax', type=int, default=500)
    parser.add_argument('--xmin', type=int, default=200)
    parser.add_argument('--ymax', type=int, default=330)
    parser.add_argument('--ymin', type=int, default=160)
    wearscript.parse(callback, parser)


key_session = 0
white = (255, 255, 255) #Create a white panel where the image goes
image_dec = Image.new("RGB", [640, 360], white) #Insert image into the white panel

db = dbEye.connect("127.0.0.1", 3306) #Create the database connection to insert the data

session_id = dbEye.create_session_id() #Create the id for this session
path = "/home/ruben/Desarrollo/eyetracker/images/" + session_id #Path declaration

#If not path create make a new one.
if not os.path.exists(path):
    os.mkdir(path)
inserted = dbEye.insert_session_id(db, session_id, path) #Call to the insert method in session DB
if (inserted):
    key_session = dbEye.get_my_session_id(db, session_id)

print "session_id: [%s] - key_session: [%d]" % (session_id, key_session)
refresh = True
if __name__ == '__main__':
    main()
