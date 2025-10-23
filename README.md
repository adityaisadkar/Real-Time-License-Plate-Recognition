# 🚗 Real-Time License Plate Recognition System

A computer vision–powered Streamlit web app that performs live license plate detection, OCR-based recognition, and vehicle color classification from webcam video feeds — complete with real-time alerts via Twilio SMS notifications.

---

## 📘 Table of Contents

1. [Project Overview](#1-project-overview)
2. [Features](#2-features)
3. [Technologies Used](#3-technologies-used)
4. [Installation](#4-installation)
5. [Configuration](#5-configuration)
6. [Usage](#6-usage)
7. [System Architecture](#7-system-architecture)
8. [Workflow](#8-workflow)
9. [License](#9-license)

---

## 🧩 1. Project Overview

This project is a real-time web application that detects and recognizes vehicle license plates from a live webcam feed using OpenCV and Tesseract OCR.

It also identifies the color of the license plate (e.g., White for private, Yellow for commercial, etc.) and can automatically notify users via SMS (using Twilio API) about registration details, insurance, or challan updates.

### 🎯 Key Use Cases:

- Smart traffic monitoring systems
- Law enforcement and vehicle tracking
- Automated toll collection
- Parking and security automation

---

## ✨ 2. Features

✅ Real-Time Detection – Uses webcam input for instant recognition  
✅ OCR-Based Recognition – Extracts text using Tesseract for high accuracy  
✅ Color Detection – Identifies plate color to infer vehicle category  
✅ SMS Notifications – Twilio integration to send alerts automatically  
✅ Location Integration – Fetches current location using LocationIQ API  
✅ User-Friendly Dashboard – Built with Streamlit for simplicity and interactivity

---

## 🛠️ 3. Technologies Used

| Category               | Tools and Libraries                    |
| ---------------------- | -------------------------------------- |
| Language               | Python 3.11.5                          |
| Core Libraries         | OpenCV, NumPy, imutils, pytesseract    |
| Web Framework          | Streamlit                              |
| APIs                   | Twilio (SMS), LocationIQ (Geolocation) |
| Data Handling          | pandas                                 |
| Matching Logic         | fuzzywuzzy                             |
| Environment Management | python-dotenv                          |

---

## ⚙️ 4. Installation

### Step 1: Clone this repository

```bash
git clone https://github.com/adityaisadkar/real-time-license-plate-recognition.git
cd real-time-license-plate-recognition
```

### Step 2: Create a virtual environment

```bash
python -m venv .venv
```

### Step 3: Activate the environment

- On Windows:
  ```bash
  .venv\Scripts\activate
  ```
- On macOS/Linux:
  ```bash
  source .venv/bin/activate
  ```

### Step 4: Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 5. Configuration

This project uses API keys and credentials for Twilio and LocationIQ.  
To keep them secure, create a `.env` file in your project directory.

### Example `.env` file

```
YOUR_API_KEY=your_locationiq_api_key_here
YOUR_ACCOUNT_SSID=your_twilio_account_sid_here
YOUR_AUTH_TOKEN=your_twilio_auth_token_here
YOUR_Twilio_NUMBER=+1234567890
```

⚠️ Important: Never upload your `.env` file to GitHub.  
Add it to `.gitignore` like this:

```
.env
.venv/
__pycache__/
*.csv
```

---

## ▶️ 6. Usage

1. Place your `License_plate_user_details.csv` in the project root.  
   (Include columns like `Number_Plate`, `Contact_Number`, `PUC`, `Challan`, `Insurance_Valid`.)
   Use images from the `Number_plates` folder for testing and getting results.

2. Run the Streamlit app:

   ```bash
   streamlit run Real_Time_License_Plate_Recognition.py
   ```

3. Click “Start Webcam Capture and Detection” on the app interface.

4. The system will:
   - Detect and extract license plate text
   - Compare it with your dataset
   - Display vehicle details and detected color
   - Send an SMS alert if conditions are met

---

## 🧱 7. System Architecture

```
                   ┌────────────────────────┐
                   │  Webcam / Video Input  │
                   └──────────┬─────────────┘
                              │
                              ▼
                   ┌────────────────────────┐
                   │ Image Preprocessing    │
                   │ (grayscale, blur, edge)│
                   └──────────┬─────────────┘
                              │
                              ▼
                   ┌────────────────────────┐
                   │ License Plate Detection │
                   └──────────┬─────────────┘
                              │
                              ▼
                   ┌────────────────────────┐
                   │ OCR (Tesseract)        │
                   │ Text Extraction        │
                   └──────────┬─────────────┘
                              │
                              ▼
                   ┌────────────────────────┐
                   │ CSV Data Matching       │
                   └──────────┬─────────────┘
                              │
                              ▼
                   ┌────────────────────────┐
                   │ Color and Alert System │
                   │ (Twilio SMS, Location) │
                   └────────────────────────┘
```

---

## 🔄 8. Workflow

1. Capture live video feed from webcam.
2. Detect possible license plate regions using contour detection.
3. Extract text using Tesseract OCR.
4. Match the extracted text with CSV data (using fuzzy matching).
5. Detect the color of the plate to classify vehicle type.
6. Fetch current location via LocationIQ API.
7. If conditions (like expired PUC or insurance) are found → send SMS notification.

---

## 📜 9. License

This project is licensed under the MIT License.  
You are free to use, modify, and distribute this code with attribution.

---

## 💡 Contributors

Aditya Isadkar  
📧 adityaisadkar@gmail.com  
🔗 [GitHub Profile](https://github.com/adityaisadkar)

Aakanksha Kate
📧 aakankshakate29@gmail.com
🔗 [GitHub Profile](https://github.com/Aakanksha-kate-29)

Renuka Rajput
📧 renukarajput742@gmail.com

---

### 🧠 Pro Tip

For better maintainability, you can also add:

- requirements.txt
- .gitignore
- sample_data.csv
- README_images/ folder (for screenshots)
