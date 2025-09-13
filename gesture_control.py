import cv2
from cvzone.HandTrackingModule import HandDetector
import pyautogui
import time

# Initialize webcam
cap = cv2.VideoCapture(0)

# Hand detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Cooldown timer to avoid multiple triggers
last_action_time = time.time()

while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)  # Mirror effect

    # Detect hands
    hands, img = detector.findHands(frame)

    if hands:
        hand = hands[0]
        fingers = detector.fingersUp(hand)

        gesture = None

        # Gesture detection
        if fingers == [0, 0, 0, 0, 0]:   # Fist
            gesture = "fist"
        elif fingers == [1, 1, 1, 1, 1]: # Open palm
            gesture = "open"
        elif fingers == [1, 0, 0, 0, 0]: # Only index finger
            gesture = "swipe"

        # Perform action (with 1.5 sec cooldown)
        if gesture and (time.time() - last_action_time) > 1.5:
            if gesture == "open":
                pyautogui.press("right")   # Next slide
                cv2.putText(img, "Next Slide", (50, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            elif gesture == "fist":
                pyautogui.press("left")    # Previous slide
                cv2.putText(img, "Previous Slide", (50, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            elif gesture == "swipe":
                pyautogui.press("f5")      # Start Presentation
                cv2.putText(img, "Start Slideshow", (50, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            last_action_time = time.time()

    cv2.imshow("Gesture-Based Teaching Controls", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
