import cv2
import pytesseract
import numpy as np

#This will change depending on the wifi you are connected to
url = 'http://10.50.172.63:8080/video'
cap = cv2.VideoCapture(url)

cv2.namedWindow('Card Scanner', cv2.WINDOW_NORMAL)
print("Please line up your card with the boxes")
print("To Register Cost Press 'c'")
print("To Register Power Press 'p'")
print("To Register Color Press 't'")
print("To Close out Press 'q'")
while True:
    
    ret, frame = cap.read()
    if not ret:
        print(" Failed to grab frame")
        break
    
    
    cost_frame = cv2.rectangle(frame, (75, 75), (150, 150), (255, 0, 0), 2)
    power_frame = cv2.rectangle(frame, (500, 75), (675, 150), (255, 0, 0), 2)
    color_frame = cv2.rectangle(frame, (100, 975), (680, 850), (255, 0, 0), 2)
    cv2.imshow('Card Scanner', frame)
    
    key = cv2.waitKey(1)
    
    if key == ord('t'):
        color_location = frame[850:975, 100:680]
        
        hsv = cv2.cvtColor(color_location, cv2.COLOR_BGR2HSV)
        
        # Reshape and get average color
        avg_hsv = hsv.reshape(-1, 3).mean(axis=0)
        h, s, v = avg_hsv
        
        # Classify based on average hue
        detected_color = "Unknown"
        
        if s < 50 and v < 75:
            detected_color = "Black"
        elif 90 < h <= 135:
            detected_color = "Blue"
        elif 35 < h <= 85:
            detected_color = "Green"
        elif 15 < h <= 35:
            detected_color = "Yellow"
        elif (h <= 10 or h >= 160):
            detected_color = "Red"
        elif 135 < h <= 160:
            detected_color = "Purple"

        print(f"Detected Dominant Color: {detected_color}")
        
    
    #Power Calculation
    if key == ord('p'):
        power_location = frame[75:150, 500:675]
        
        gray = cv2.cvtColor(power_location, cv2.COLOR_BGR2GRAY)
        
        cv2.imshow("Power Processed", gray)
        
        # OCR: Try to read digits only
        power_text = pytesseract.image_to_string(gray, config='--psm 6 -c tessedit_char_whitelist=0123456789')
        power_text = power_text.strip()
        
        print(f"Detected Power:{power_text}")
        
    
    #Cost Calculation
    if key == ord('c'):
        cost_text = ''
        cost_location = frame[75:150, 75:150]
        
        # Preprocess for OCR: HSV (Hue, Saturation, Value)
        hsv = cv2.cvtColor(cost_location, cv2.COLOR_BGR2HSV)
        
        # Black Cost
        low_Black = (0,0,0)
        high_Black = (180,255,60)
        
        mask = cv2.inRange(hsv, low_Black, high_Black)
          
        #This will flip White and Black colors 
        inverted = cv2.bitwise_not(mask)
        
        #What the camera sees for black cost
        cv2.imshow('Black Text Mask 1', inverted)
        
        #What the camera sees for white Cost
        cv2.imshow('White Text Mask', mask)
            
        cost_text = pytesseract.image_to_string(mask, config='--psm 6 -c tessedit_char_whitelist=0123456789')
        cost_text = cost_text.strip()
        if cost_text != '':
            print(f"Black Detected Cost: {cost_text}")
        
        if cost_text == '': 
            
            gray = cv2.cvtColor(cost_location, cv2.COLOR_BGR2GRAY)
            
            cv2.imshow("Processed Region", gray)

            # OCR: Try to read digits only
            cost_text = pytesseract.image_to_string(gray, config='--psm 8 -c tessedit_char_whitelist=0123456789')
            cost_text = cost_text.strip()
        
            print(f"Detected White Cost:'{cost_text}'")
    
        
    if key == ord('q'):
        break
    
    

cap.release()
cv2.destroyAllWindows()

