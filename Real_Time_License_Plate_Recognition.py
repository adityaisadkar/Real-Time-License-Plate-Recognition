# Importing Necessary Libraries
import cv2
import numpy as np
import imutils
import pytesseract
import streamlit as st
import pandas as pd
from fuzzywuzzy import fuzz
from twilio.rest import Client
import requests

# Optional: Update Tesseract path if not in PATH
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def detect_plate_color(image):
    # Convert the image to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define the range for yellow color
    yellow_lower = np.array([20, 100, 100])
    yellow_upper = np.array([30, 255, 255])

    # Define the range for green color
    green_lower = np.array([40, 100, 100])
    green_upper = np.array([80, 255, 255])

    # Define the range for black color
    black_lower = np.array([0, 0, 0])
    black_upper = np.array([180, 255, 30])

    # Define the range for blue color (including light blue)
    blue_lower = np.array([90, 50, 50])
    blue_upper = np.array([140, 255, 255])

    # Define the range for white/grey color
    white_lower = np.array([0, 0, 180])
    white_upper = np.array([180, 20, 255])

    # Define the range for red color (including both ends of the hue spectrum)
    red_lower1 = np.array([0, 100, 100])
    red_upper1 = np.array([10, 255, 255])
    red_lower2 = np.array([160, 100, 100])
    red_upper2 = np.array([180, 255, 255])

    # Create masks for each color
    yellow_mask = cv2.inRange(hsv, yellow_lower, yellow_upper)
    green_mask = cv2.inRange(hsv, green_lower, green_upper)
    black_mask = cv2.inRange(hsv, black_lower, black_upper)
    blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
    white_mask = cv2.inRange(hsv, white_lower, white_upper)
    red_mask1 = cv2.inRange(hsv, red_lower1, red_upper1)
    red_mask2 = cv2.inRange(hsv, red_lower2, red_upper2)
    red_mask = cv2.bitwise_or(red_mask1, red_mask2)

    # Combine red and white masks to detect red with white
    red_with_white_mask = cv2.bitwise_or(red_mask, white_mask)

    # Calculate the area of the detected colors
    yellow_area = cv2.countNonZero(yellow_mask)
    green_area = cv2.countNonZero(green_mask)
    black_area = cv2.countNonZero(black_mask)
    blue_area = cv2.countNonZero(blue_mask)
    white_area = cv2.countNonZero(white_mask)
    red_area = cv2.countNonZero(red_mask)
    red_with_white_area = cv2.countNonZero(red_with_white_mask)

    # Determine the dominant color
    areas = {
        "Yellow (Taxi)": yellow_area,
        "Green (Electric Vehicle)": green_area,
        "Black (Rental Vehicle)": black_area,
        "Blue (Diplomat Vehicle)": blue_area,
        "White (Private Vehicle)": white_area,
        "Red (Temporary registration vehical)": red_area,
        "Red (Temporary registration vehical)": red_with_white_area
    }
    color_detected = max(areas, key=areas.get)

    if areas[color_detected] == 0:
        color_detected = "No Color Detected"

    return color_detected

def extract_license_plate_text(image):
    img = np.array(image)  # Convert PIL image to numpy array
    img = imutils.resize(img, width=600)  # Resize for faster processing
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)  # Faster noise reduction

    # Edge detection using Canny
    edged = cv2.Canny(blurred, 50, 200)

    keypoints = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(keypoints)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]  # Sort contours

    location = None
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 10, True)
        if len(approx) == 4:
            location = approx
            break

    if location is None:
        return "License plate not found", img, None

    mask = np.zeros(gray.shape, np.uint8)
    new_image = cv2.drawContours(mask, [location], 0, 255, -1)
    new_image = cv2.bitwise_and(img, img, mask=mask)

    (x, y) = np.where(mask == 255)
    (x1, y1) = (np.min(x), np.min(y))
    (x2, y2) = (np.max(x), np.max(y))
    cropped_image_gray = gray[x1: x2 + 1, y1: y2 + 1]
    cropped_image_color = img[x1: x2 + 1, y1: y2 + 1]

    # Tesseract Configuration for Speed
    config = "--oem 3 --psm 6"
    result = pytesseract.image_to_string(cropped_image_gray, config=config, lang="eng")

    return result, new_image, cropped_image_color

def get_current_location(api_key):
    url = f"https://us1.locationiq.com/v1/reverse.php?key={api_key}&lat=19.8776&lon=75.3423&format=json"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            location = {
                "address": data.get("display_name"),
                "latitude": data.get("lat"),
                "longitude": data.get("lon")
            }
            return location
        else:
            print("Error:", data.get("error"))
            return None
    except Exception as e:
        print("An error occurred:", e)
        return None

# Replace 'YOUR_API_KEY' with your actual LocationIQ API key
# Use this Site https://www.twilio.com/en-us to get details 
api_key = 'YOUR_API_KEY'
location = get_current_location(api_key)

def send_sms_notification(text, recipient_number):
    # Twilio credentials
    account_sid = "YOUR_ACCOUNT_SSID"
    auth_token = "YOUR_AUTH_TOKEN"
    client = Client(account_sid, auth_token)

    # Send SMS notification
    message = client.messages.create(
        body=text,
        from_="YOUR_NUMBER",  # Your Twilio number
        to="+91" + str(recipient_number),  # The recipient's phone number
    )

    if message.sid:
        st.success("SMS notification sent successfully.")

def main():
    
    # Inject custom CSS for the background, text color, and button styling
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url('https://c4.wallpaperflare.com/wallpaper/771/657/298/wallpaper-of-road-wallpaper-preview.jpg');
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        .text-box {
            background-color: rgba(255, 255, 255, 0.8); /* Semi-transparent white */
            padding: 20px;
            border-radius: 10px;
            color: black; /* Set all text color to black */
            text-align: center; /* Center align text */
            font-size: 25px; /* Change this value to adjust font size */
        }
        h1, h2 {
            color: black; /* Black color for headings */
            text-align: center; /* Center align headings */
        }
        .stButton button {
            background-color: black !important; /* Custom color for the button */
            color: white !important;  /* White text on the button */
            font-size: 20px !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<div class='text-box'><h1>Real-time License Plate Detection</h1></div>", unsafe_allow_html=True)
    st.markdown("<div class='text-box'><h2>Live Webcam Feed with License Plate Detection</h2></div>", unsafe_allow_html=True)

    run_detection = st.button("Start Webcam Capture and Detection")

    if run_detection:
        st.write("Starting detection...")

        # Create a placeholder for the text and video display
        text_placeholder = st.empty()
        video_placeholder = st.empty()

        # Start video capture
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            st.error("Error: Could not open webcam.")
            return

        def preprocess_plate_text(plate_text):
            cleaned_text = "".join(e for e in plate_text if e.isalnum()).upper().strip()
            return cleaned_text

        def check_license_plate_in_csv(plate_text, cropped_image, similarity_threshold=80):
            cleaned_plate = preprocess_plate_text(plate_text)
            df = pd.read_csv("License_plate_user_details.csv")

            for index, row in df.iterrows():
                stored_plate = preprocess_plate_text(row["Number_Plate"])
                similarity = fuzz.ratio(cleaned_plate, stored_plate)

                if similarity >= similarity_threshold:
                    st.markdown("<div class='text-box'><p>Match found with similarity {}</p></div>".format(similarity), unsafe_allow_html=True)
                    for col in df.columns:
                        st.markdown("<div class='text-box'><p>{}: {}</p></div>".format(col, row[col]), unsafe_allow_html=True)

                    messages = []
                                       
                    if row["PUC"] == "No":
                        messages.append("Complete your PUC here: https://puc.parivahan.gov.in/puc/\n\n")

                    if row["Challan"] == "No":
                        messages.append("Pay your pending challan here: https://echallan.parivahan.gov.in/index/accused-challan\n\n")

                    if row["Insurance_Valid"] == "No":
                        messages.append("Renew your insurance policy here: https://www.policybazaar.com\n\n")

                    if messages:
                        additional_message = " ".join(messages)

                        # Print the location before sending the message
                        if location:
                            st.markdown("<div class='text-box'><p><strong>Address:</strong> {}</p></div>".format(location['address']), unsafe_allow_html=True)
                            st.markdown("<div class='text-box'><p><strong>Latitude:</strong> {}</p></div>".format(location['latitude']), unsafe_allow_html=True)
                            st.markdown("<div class='text-box'><p><strong>Longitude:</strong> {}</p></div>".format(location['longitude']), unsafe_allow_html=True)

                        send_sms_notification(
                            f"Matched License Plate: {stored_plate}.\n\nCurrent Location: {location['address']}.\n{additional_message}",
                            row["Contact_Number"]
                        )

                    color_detected = detect_plate_color(cropped_image)
                    st.markdown("<div class='text-box'><p><strong>Detected Plate Color:</strong> {}</p></div>".format(color_detected), unsafe_allow_html=True)

                    return True

            return False

        match_found = False
        while not match_found:
            ret, frame = cap.read()
            if not ret:
                st.error("Error: Could not read frame.")
                break
            
            text, processed_image, cropped_image = extract_license_plate_text(frame)
            video_placeholder.image(processed_image, channels="BGR", caption="Live Feed with Detected License Plate", use_column_width=True)
            text_placeholder.markdown("<div class='text-box'><p>Detected License Plate Text: {}</p></div>".format(text), unsafe_allow_html=True)

            match_found = check_license_plate_in_csv(text, cropped_image)

        cap.release()
        if match_found:
            if st.button("Restart Detection"):
                st.experimental_rerun()

if __name__ == "__main__":
    main()
