import cv2
import mediapipe as mp
import pyautogui

# Capturing Video from camera
cap = cv2.VideoCapture(0)
hand_detector = mp.solutions.hands.Hands()
drawing_utils = mp.solutions.drawing_utils
# TO know the Screen Size for pointer to be in center
screen_width, screen_height = pyautogui.size()
index_y = 0
while True:
    #  Detect the Hand
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = hand_detector.process(rgb_frame)
    hands = output.multi_hand_landmarks
    
    # Drawing the the hand when the hand is detected 
    if hands:
        for hand in hands:
            # drawaing the hand
            drawing_utils.draw_landmarks(frame, hand)
            # Separate the index finger (landmark 8) so that we can use that as a mouse pointer
            landmarks = hand.landmark
            for id, landmark in enumerate(landmarks):
                x = int(landmark.x*frame_width)
                y = int(landmark.y*frame_height)
                # Drawing the circle on index fingers
                if id == 8:
                    cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255))
                    index_x = screen_width/frame_width*x
                    index_y = screen_height/frame_height*y
                # Drawing the circle on thumb fingers
                if id == 4:
                    cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 255, 255))
                    thumb_x = screen_width/frame_width*x
                    thumb_y = screen_height/frame_height*y
                    print('outside', abs(index_y - thumb_y))
                    
                    # For Click
                    if abs(index_y - thumb_y) < 20:
                        pyautogui.click()
                        pyautogui.sleep(1)
                    # For movement
                    elif abs(index_y - thumb_y) < 100:
                        pyautogui.moveTo(index_x, index_y)
    #Window title
    cv2.imshow('Virtual Mouse', frame)
    # Close button
    cv2.waitKey(1)
