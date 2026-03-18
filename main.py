import cv2
import datetime
import pandas as pd
from ultralytics import YOLO
import time
import os

# 1. Initialisation
model = YOLO("yolo11n.pt")
if not os.path.exists("captures"):
    os.makedirs("captures")

cap = cv2.VideoCapture(0)
activity_data = []
last_log_time = 0 
last_capture_time = 0 # Pour éviter de prendre trop de photos d'un coup

print("🚀 Système de surveillance avec Capture d'Écran actif.")

while cap.isOpened():
    success, frame = cap.read()
    if not success: break

    results = model.track(frame, persist=True, verbose=False)

    if results[0].boxes.id is not None:
        current_time = time.time()
        labels = results[0].boxes.cls.cpu().numpy()
        names = model.names
        
        for obj_id in labels:
            object_name = names[int(obj_id)]
            
            # --- LOGIQUE DE CAPTURE POUR PERSONNE ---
            if object_name == "person":
                # On prend une capture max toutes les 5 secondes pour une personne
                if current_time - last_capture_time > 5:
                    timestamp_file = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    file_path = f"captures/personne_{timestamp_file}.jpg"
                    
                    # Sauvegarde de l'image
                    cv2.imwrite(file_path, frame)
                    print(f"📸 Capture enregistrée : {file_path}")
                    last_capture_time = current_time
            # ----------------------------------------

            # Logique classique de logging (toutes les 2 sec)
            if current_time - last_log_time > 2:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                activity_data.append({"Timestamp": timestamp, "Object": object_name})
                last_log_time = current_time

    annotated_frame = results[0].plot()
    cv2.imshow("AI Vision - Capture Mode", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

if activity_data:
    pd.DataFrame(activity_data).to_csv("activity_log.csv", index=False)

cap.release()
cv2.destroyAllWindows()