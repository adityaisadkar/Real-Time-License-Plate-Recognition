# **Real-Time License Plate Recognition System**

## **Table of Contents**
1. [Project Overview](#1.project-overview)  
2. [Features](#features)  
3. [Technologies Used](#technologies-used)  
4. [Installation](#installation)  
5. [Usage](#usage)  
6. [Architecture](#architecture)  
7. [Demo](#demo)  
8. [Contributing](#contributing)  
9. [License](#license)  
10. [Contact](#contact)  

---

### **1. Project Overview**  
This project is a web-based application designed to detect and recognize vehicle license plates from live video feeds. Using advanced computer vision and OCR techniques, it enables real-time license plate detection, recognition, and color-based vehicle categorization.  

Key Applications:  
- Automated toll collection.  
- Law enforcement and security.  
- Real-time traffic monitoring.  

---

### **2. Features**  
- **Real-Time Detection**: Processes live video streams for immediate recognition.  
- **OCR-Based Recognition**: Uses Tesseract OCR for high-accuracy license plate text extraction.  
- **Color Detection**: Identifies plate color to determine vehicle type and usage.  
- **Notification System**: Sends alerts (via Twilio API) for stolen vehicles or documentation updates.  
- **User-Friendly Interface**: Interactive UI for data visualization and management.  

---

### **3. Technologies Used**  
- **Programming Languages**: Python  
- **Libraries & Frameworks**:  
  - OpenCV (Image Processing)  
  - Tesseract OCR (Text Recognition)  
  - Twilio API (Notifications)  
- **Tools**: Flask, NumPy, Matplotlib  
- **Compatible Python Version**: 3.11.5  
  Download Python [here](https://www.python.org/downloads/release/python-3115/).  

---

### **4. Installation**  
Follow these steps to set up the project locally:  

1. Clone the repository:  
   ```bash  
   git clone https://github.com/adityaisadkar/real-time-license-plate-recognition.git
   ```
2. Install dependencies:
   ```bash  
   git clone https://github.com/adityaisadkar/real-time-license-plate-recognition.git
   ```
3. Run the web-application
   ```bash
   streamlit run Real_Time_License_Plate_Recognition.py
   ```

### **Usage**

1.  Launch the application and provide a live video feed as input.
2.  The system detects and extracts license plate text in real time.
3.  Alerts and notifications are sent automatically for pre-configured conditions.

### **Architecture**

-  **Input Layer**: Captures live video or images.
-  **Processing Layer**:
    -  Image preprocessing (grayscale conversion, thresholding)
    -  License plate detection using bounding boxes.
    -  OCR text extraction.
-  **Output Layer**:
    -  Displays detected plate details.
    -  Sends notifications for alerts.

### **Workflow Diagram**
Available in Images folder

### **LICENSE**
This project is licensed under the MIT License.

