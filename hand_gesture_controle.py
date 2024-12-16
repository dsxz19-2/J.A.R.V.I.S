import mediapipe
import cv2
import time
import pygame
import win32api, win32con
import math
import imutils
import numpy as np

# Camera modual Datasheet
# https://www.hbvcamera.com/1MP-%20HD-usb-cameras/hbvcam-ov9726-720p-hd-otg-free-driver-pc-webcam-camera-module.html

def click():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.02)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

click_count = 0
click_count_reset = 100

pygame.init()

screen_info = pygame.display.Info()

wCam, hCam = 640*2, 480*2

width = screen_info.current_w
height = screen_info.current_h

pygame.quit()

frameR = 100
smoothening = 7

plocX, plocY = 0, 0
clocX, clocY = 0, 0

hold = False

# Use MediaPipe to draw the hand framework over the top of hands it identifies in Real-Time
drawingModule = mediapipe.solutions.drawing_utils
handsModule = mediapipe.solutions.hands

#Use CV2 Functionality to create a Video stream and add some values
vid = cv2.VideoCapture(0)

old_pos_index = (0, 0)
avg_vibrations = []

distance = 0

# Add confidence values and extra settings to MediaPipe hand tracking. As we are using a live video stream this is not a static
# Image mode, confidence values in regards to overall detection and tracking and we will only let two hands be tracked at the same time
# More hands can be tracked at the same time if desired but will slow down the system
with handsModule.Hands(static_image_mode=False, min_detection_confidence=0.8, min_tracking_confidence=0.8, max_num_hands=2) as hands:
     print("Live!")

#Create an infinite loop which will produce the live feed to our desktop and that will search for hands
     while True:
           ret, frame = vid.read()
           frame = imutils.resize(frame, width=wCam, height=hCam)
           #Unedit the below line if your live feed is produced upsidedown
           frame = cv2.flip(frame, -1)
           frame = cv2.flip(frame, 0)
           
           # Determines the frame size, 640 x 480 offers a nice balance between speed and accurate identification
           # frame1 = cv2.resize(frame, (width, height))
           
           # Produces the hand framework overlay ontop of the hand, you can choose the colour here too)
           results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            # cv2.rectangle(frame, (frameR, frameR), (wCam - frameR, hCam - frameR), (255, 0, 255), 2)
           
           # In case the system sees multiple hands this if statment deals with that and produces another hand overlay
           if results.multi_hand_landmarks != None:
              for handLandmarks in results.multi_hand_landmarks:
                  drawingModule.draw_landmarks(frame, handLandmarks, handsModule.HAND_CONNECTIONS)
                  
                  # Finds the coordinates of the fingers
                  for point in handsModule.HandLandmark:

                    index = handLandmarks.landmark[8]
                    indexC= drawingModule._normalized_to_pixel_coordinates(index.x, index.y, wCam, hCam)
    
                    mid = handLandmarks.landmark[12]
                    midC= drawingModule._normalized_to_pixel_coordinates(mid.x, mid.y, wCam, hCam)

                    thumb = handLandmarks.landmark[4]
                    thumbC= drawingModule._normalized_to_pixel_coordinates(thumb.x, thumb.y, wCam, hCam)

                    if (indexC and midC) != None:
                        distance_i_m = math.sqrt( (indexC[0] - midC[0])**2 + (indexC[1] - midC[1])**2 )
                        if click_count >= click_count_reset:
                            click_count = 0

                        if round(distance_i_m) <= 40 and click_count == 0:
                            print(click_count, "Click!")
                            click()
                            click_count = 1
                    
                    if (indexC and thumbC) != None:
                        distance_i_t = math.sqrt( (indexC[0] - thumbC[0])**2 + (indexC[1] - thumbC[1])**2 )
                        if round(distance_i_t) <= 40 and hold == False:
                            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
                            hold = True
                            print("\n", distance_i_t)
                            print("Hold!")

                        if round(distance_i_t) > 40 and hold == True:
                            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
                            hold = False
                            print("\n", distance_i_t)
                            print("Release!")

                    else:
                        pass

                    # Smooths the tracking by removing slight jitters
                    if indexC != None:
                        vibration_index = math.sqrt( (indexC[0] - old_pos_index[0])**2 + (indexC[1] - old_pos_index[1])**2 )
                        old_pos_index = (indexC[0], indexC[1])

                        if vibration_index <= 1:
                            x = np.interp(indexC[0], (frameR, wCam - frameR), (0, width))   
                            y = np.interp(indexC[1], (frameR, hCam - frameR), (0, height))

                            clocX = plocX + (x - plocX) / smoothening
                            clocY = plocY + (y - plocY) / smoothening

                            win32api.SetCursorPos((int(clocX), int(clocY)))
                            click_count = click_count + 1

                            plocX, plocY = clocX, clocY                                           
            
           # Displays current frame
           cv2.imshow("Frame", frame)
           key = cv2.waitKey(1) & 0xFF
           
           # If the "q" is press on the keyboard it will stop the system
           if key == ord("q"):
              break
           