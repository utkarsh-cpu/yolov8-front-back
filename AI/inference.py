import base64
from flask import Flask, request, jsonify, make_response
import os
import cv2
import numpy as np
from ultralytics import YOLO
import torch
from PIL import Image
import io
print(torch.backends.mps.is_available())
app = Flask(__name__)

# Initialize YOLO model (CPU mode)
# You can choose a model like 'yolov8n.pt', 'yolov8s.pt', etc.
model_path = os.environ.get('MODEL_PATH', 'yolov8n.pt')
model = YOLO(model_path)  # Will load the YOLOv8n model weights from local or auto-download


@app.route('/', methods=['GET'])
def home():
    return "YOLO is up."


@app.route('/detect', methods=['POST'])
def detect():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_bytes = request.files['image'].read()
    pil_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    np_image = np.array(pil_image)

    # Perform inference
    results = model.predict(source=np_image, imgsz=640, conf=0.25)
    result = results[0]  # single image result

    detections = []
    boxes = result.boxes  # bounding boxes
    class_names = result.names

    for box in boxes:
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        conf = float(box.conf[0].item())
        cls = int(box.cls[0].item())
        label = class_names[cls]

        detections.append({
            "class_id": cls,
            "label": label,
            "confidence": round(conf, 3),
            "bbox": [round(x1, 2), round(y1, 2), round(x2, 2), round(y2, 2)]
        })

    # Draw bounding boxes on the original image
    annotated_image = np_image.copy()
    for det in detections:
        x1, y1, x2, y2 = map(int, det["bbox"])
        cv2.rectangle(annotated_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            annotated_image,
            f"{det['label']} {det['confidence']:.2f}",
            (x1, max(y1 - 5, 0)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

    # Encode annotated image to base64
    _, buffer = cv2.imencode('.jpg', annotated_image)
    annotated_b64 = base64.b64encode(buffer).decode('utf-8')

    # Return a single JSON response with detections + base64 image
    response_data = {
        "detections": detections,
        "annotated_image": annotated_b64
    }
    return jsonify(response_data)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)