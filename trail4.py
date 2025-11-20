import cv2
import serial
import time
import os
import datetime
import threading
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import requests
from ultralytics import YOLO

# ==============================
# Email Config
# ==============================
EMAIL_ADDRESS = 'uptoskillssunidhi@gmail.com'
EMAIL_PASSWORD = 'wnpf blvr vcll evnu'  # app password
RECIPIENTS = ['Chiruchiranth001@gmail.com']

SNAPSHOT_DIR = "accident_snapshots"
os.makedirs(SNAPSHOT_DIR, exist_ok=True)

# ==============================
# Initialize YOLOv8
# ==============================
model = YOLO("yolov8s.pt")   # pretrained on COCO (80 classes)

# ==============================
# Initialize Arduino
# ==============================
arduino = serial.Serial("COM4", 9600, timeout=1)
time.sleep(2)  # wait for Arduino

# ==============================
# Helper Functions
# ==============================
def get_location():
    try:
        response = requests.get("https://ipinfo.io")
        data = response.json()
        
        return data.get("loc", "Unknown")
    except:
        return "Unknown"

def save_snapshot(frame):
    filename = os.path.join(
        SNAPSHOT_DIR,
        f"snapshot_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
    )
    cv2.imwrite(filename, frame)
    return filename

def send_email_alert(image_path):
    location = get_location()
    subject = "🚨 Road Accident Detected"
    body = f"""
    Dear Authority/Concerned Person,

    🚨 A potential road accident has been detected.

    📍 Location: https://www.google.com/maps?q={location}

    📸 Snapshot of the accident is attached.

    Please take immediate action.

    Regards,
    Accident Detection AI System
    """

    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = ", ".join(RECIPIENTS)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    with open(image_path, "rb") as img_file:
        image = MIMEBase('application', 'octet-stream')
        image.set_payload(img_file.read())
        encoders.encode_base64(image)
        image.add_header('Content-Disposition',
                         f'attachment; filename="{os.path.basename(image_path)}"')
        msg.attach(image)

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("✅ Email sent.")
    except Exception as e:
        print(f"❌ Email sending failed: {e}")

def is_overlapping(box1, box2):
    x1, y1, x2, y2 = box1
    x3, y3, x4, y4 = box2
    return not (x2 < x3 or x4 < x1 or y2 < y3 or y4 < y1)

# ==============================
# Camera Auto-Detection (External Preferred)
# ==============================
def find_camera():
    preferred_indices = [1, 2, 0, 3, 4]  # external cams usually come before built-in
    for i in preferred_indices:
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)  # CAP_DSHOW fixes Windows camera issues
        if cap.isOpened():
            print(f"✅ Camera found at index {i}")
            cap.release()
            return i
        cap.release()
    raise Exception("❌ No camera found!")

# ==============================
# Main Function
# ==============================
def main():
    cam_index = find_camera()
    cap = cv2.VideoCapture(cam_index, cv2.CAP_DSHOW)
    cap.set(3, 640)
    cap.set(4, 480)

    current_signal = '0'
    collision_start = {}
    accident_active = False

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame, conf=0.3)

        # detection lists
        bike_bboxes, car_bboxes, truck_bboxes, animal_bboxes, human_bboxes = [], [], [], [], []
        detections = []

        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                label = model.names[cls_id]
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                # Bike
                if label in ["bicycle", "motorbike"]:
                    bike_bboxes.append((x1, y1, x2, y2))
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 2)
                    cv2.putText(frame, "Bike", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

                # Car
                elif label == "car":
                    car_bboxes.append((x1, y1, x2, y2))
                    detections.append((x1, y1, x2, y2))
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                    cv2.putText(frame, "Car", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

                # Truck / Bus
                elif label in ["truck", "bus"]:
                    truck_bboxes.append((x1, y1, x2, y2))
                    detections.append((x1, y1, x2, y2))
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, "Truck/Bus", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                # Animals
                elif label in ["elephant", "bear", "zebra", "giraffe", "cow",
                               "horse", "sheep", "dog", "cat"]:
                    animal_bboxes.append((x1, y1, x2, y2))
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                    cv2.putText(frame, "Animal", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

                # Human
                elif label == "person":
                    human_bboxes.append((x1, y1, x2, y2))
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, "Human", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # ==========================
        # Decision Logic for Arduino
        # ==========================
        if len(animal_bboxes) > 0:
            new_signal = '4'
        elif len(truck_bboxes) > 0:
            new_signal = '3'
        elif len(car_bboxes) > 0:
            new_signal = '2'
        elif len(bike_bboxes) > 0:
            new_signal = '1'
        elif len(human_bboxes) > 0:
            new_signal = '0'
        else:
            new_signal = '0'

        if new_signal != current_signal:
            arduino.write(new_signal.encode())
            print(f"➡️ Sent to Arduino: {new_signal}")
            current_signal = new_signal

        # ==========================
        # Accident Detection
        # ==========================
        accident_detected_now = False
        overlap_found = False

        for i in range(len(detections)):
            for j in range(i + 1, len(detections)):
                if is_overlapping(detections[i], detections[j]):
                    overlap_found = True
                    pair_key = f"{i}-{j}"
                    if pair_key not in collision_start:
                        collision_start[pair_key] = time.time()
                    else:
                        elapsed = time.time() - collision_start[pair_key]
                        if elapsed > 3:
                            accident_detected_now = True
                else:
                    pair_key = f"{i}-{j}"
                    if pair_key in collision_start:
                        del collision_start[pair_key]

        if accident_detected_now and not accident_active:
            accident_active = True
            print("🚨 Accident Detected!")
            snapshot_path = save_snapshot(frame)
            threading.Thread(target=send_email_alert,
                             args=(snapshot_path,), daemon=True).start()

        elif not overlap_found and accident_active:
            accident_active = False
            print("✅ Accident cleared.")

        if accident_active:
            cv2.putText(frame, "ACCIDENT DETECTED!", (50, 70),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

        # ==========================
        # Show Frame
        # ==========================
        cv2.imshow("YOLOv8 Detection + Accident System", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
    arduino.close()

if __name__ == "__main__":
    main()
