# 🚨 Accident Prevention System in Hilly Region Using Deep Learning

(YOLOv8 + Arduino + Email Alerts + OLED + LCD + Ultrasonic)

This project integrates **AI-based vehicle/animal detection**, **Arduino alert hardware**, **accident monitoring**, **ultrasonic distance measurement**, and **automatic email notifications** into a single intelligent road‑safety system.

It combines the functionalities of:

* **Arduino-based Alert Display System** (OLED, LCD, LEDs, Ultrasonic)
* **Python YOLOv8 Detection + Accident Detection + Email Alert System**

---

 System Overview

This smart safety system:

* Detects vehicles (car, truck, bus, motorcycle) and animals using **YOLOv8**.
* Sends real-time signals to **Arduino** to display alerts.
* Displays distance measurement continuously using **ultrasonic sensor** on OLED.
* Shows warnings on **LCD** with LED indicators.
* Detects accidents via bounding‑box overlap persistence.
* Captures snapshot and emails immediately with **GPS location link**.

---

 Components Used

 **Hardware**

* Arduino UNO/Nano
* Ultrasonic Sensor HC‑SR04
* OLED Display (SSD1306, 128×64)
* LCD 16×2 (I2C)
* LEDs (RED, GREEN, ANIMAL ALERT)
* External USB Webcam
* Connecting Wires & Power

 **Software / Libraries**

* Python 3
* OpenCV
* ultralytics (YOLOv8)
* PySerial
* Requests
* smtplib (Email handling)
* Arduino IDE
* Adafruit SSD1306 Library
* LiquidCrystal_I2C Library

---

 Python Dependencies (requirements.txt)

```
opencv-python
ultralytics
pyserial
requests
numpy
Pillow
```

---

 Arduino Connections & Operation

 **Ultrasonic Sensor**

| Component | Pin |
| --------- | --- |
| TRIG      | D9  |
| ECHO      | D10 |

 **LEDs**

| LED        | Pin |
| ---------- | --- |
| Red LED    | D3  |
| Green LED  | D4  |
| Animal LED | D5  |

 **Displays**

* OLED (I2C) → SDA, SCL
* LCD (I2C, address: 0x27) → SDA, SCL

 **Arduino Receives Serial Commands**

| Object     | Serial Value |
| ---------- | ------------ |
| Motorcycle | `1`          |
| Car        | `2`          |
| Truck/Bus  | `3`          |
| Animal     | `4`          |
| None       | `0`          |

Arduino then updates:

* LCD alerts
* LEDs (Red/Green/Animal)
* OLED for distance

---

 Arduino Features

 Real-time Distance Measurement

Using HC‑SR04, distance is displayed on OLED:

* Big bold text for visibility.
* Continuously refreshed.

 Warning Alerts on LCD

Based on serial input from Python:

* "BIKE AHEAD"
* "CAR AHEAD"
* "TRUCK AHEAD"
* "ANIMAL AHEAD"
* Default message: **“STAY ALERT & STAY SAFE”**

 LEDs Indicate Status

* **RED** → Vehicle danger
* **YELLOW** → Animal alert
* **GREEN** → Safe state

---

 Python (YOLOv8) Features

 Vehicle & Animal Detection

Detects only relevant classes:

* motorcycle
* car
* truck
* bus
* animals (dog, cow, elephant, tiger, deer, etc.)

 Sends Corresponding Code to Arduino

Automatically maps detection → Arduino signal.

 Accident Detection Logic

A collision is assumed when:

1. Two bounding boxes **overlap**
2. And overlap continues for **> 3 seconds**

Then:

* Accident snapshot saved
* Accident email sent
* Red flashing message shown on Python window

---

 Email Alert System

When accident detected:

* Takes snapshot
* Gets approximate GPS from `ipinfo.io`
* Sends email with:

  * **Google Maps link**
  * **Image attachment**
  * **Accident message**

Email Subject:

```
🚨 Accident Detected
```

---

 Project Structure

```
├── accident_snapshots/        # Stores captured accident images
├── python_code.py             # YOLO + Email + Accident logic
├── arduino_code.ino           # OLED + LCD + LED alert system
├── requirements.txt
└── README.md
```

---

 How the Entire System Works

 **1. Python YOLO System**

* Detects objects
* Identifies vehicle/animal type
* Sends serial code to Arduino
* Detects accidents
* Sends emails when needed

 **2. Arduino System**

* Reads serial value
* Updates LCD/OLED/LEDs accordingly
* Displays distance continuously
* Shows warnings instantly

Together, both modules create a **complete smart road-safety solution**.

---

 Testing Procedure

1. Connect external webcam
2. Run Python file:

```
python python_code.py
```

3. Verify Arduino display updates
4. Simulate two vehicles overlapping
5. Check if accident alert is triggered
6. Verify email with:

   * Image
   * GPS link

---

