 Smart Alert System Using Arduino, Ultrasonic Sensor, OLED & LCD

This project implements a real-time **road safety alert system** using Arduino. It integrates an **ultrasonic distance measurement module**, an **OLED display**, a **16x2 I2C LCD**, and **alert LEDs** to notify the user of different types of obstacles such as bikes, cars, trucks, and animals.

---
 **Project Overview**

The system continuously measures distance using an ultrasonic sensor and displays the value on an OLED screen. It also receives classification commands (1–4) via Serial communication, typically from an external detection system (like a Python script or AI module). Based on these commands, the LCD displays alerts and activates corresponding LEDs.

---
 **Components Used**

* **Arduino (UNO/Nano)**
* **Ultrasonic Sensor (HC-SR04)**
* **OLED Display (SSD1306, 128×64, I2C)**
* **LCD Display (16x2 I2C)**
* **LED Indicators:**

  * Red LED – Vehicle Alert
  * Green LED – Safe
  * Yellow/Animal LED – Animal Alert
* **Jumper Wires & Power Supply**

-
-  **Features**

* Real‑time distance monitoring using ultrasonic sensor
* Visual output on OLED
* Alert messages displayed on 16x2 LCD
* LEDs indicating danger or safe state
* Serial‑based object classification:

  * `1` → Bike Ahead
  * `2` → Car Ahead
  * `3` → Truck Ahead
  * `4` → Animal Ahead

---

 **Pin Connections**

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

* **OLED (I2C)** → SDA, SCL
* **LCD (I2C, addr: 0x27)** → SDA, SCL

---

 **Working Logic**

**1️⃣ Distance Measurement (Ultrasonic + OLED)**

* Sends trigger pulse
* Receives echo pulse
* Calculates distance
* Displays distance in cm on OLED

 **2️⃣ Receiving AI Output via Serial**

AI model or external script sends commands:

* `1` → Bike Ahead
* `2` → Car Ahead
* `3` → Truck Ahead
* `4` → Animal Ahead

 **3️⃣ LCD + LED Alerts**

* Shows alert message on LCD
* Activates corresponding LED
* Auto resets back to default "Stay Alert & Stay Safe" screen

---

 **Testing**

* Power the module and observe distance updates on OLED.
* Send commands through Serial Monitor:

  * Type `1` → Bike alert
  * Type `4` → Animal alert
* Ensure LEDs and LCD display respond correctly.

---

**Applications**

* Road safety warning systems
* AI‑based vehicle classification
* Embedded accident prevention systems
* Smart transportation projects

---



If you want, I can also generate a **GitHub‑ready README with badges, wiring diagrams, or flowchart**.
