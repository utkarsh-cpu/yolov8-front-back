# yolov8-front-back
Ultralytics YOLOv8 Object Detection Microservice

This repository demonstrates an end-to-end object detection pipeline using Ultralytics YOLOv8 in a microservices architecture. It includes two main services:
	1.	AI Backend: Performs object detection on uploaded images using the Ultralytics YOLOv8 model, then returns structured JSON detections plus an annotated image (base64-encoded).
	2.	UI Frontend: A Flask-based service that hosts a simple web page with a file upload form, displays upload progress, and upon completion, shows both the JSON detection results and the annotated bounding-box image.

We use Docker and docker-compose to orchestrate these services.

Table of Contents
	1.	Features
	2.	Architecture Overview
	3.	Folder Structure
	4.	Prerequisites
	5.	Setup & Running
	6.	Usage & Testing
	7.	Configuration
	8.	How It Works
	9.	Troubleshooting
	10.	References

Features
	•	Two microservices:
	•	A UI service in Flask with a web-based upload form and progress bar.
	•	An AI service using Ultralytics YOLOv8 (YOLOv8n for CPU-friendly inference).
	•	JSON + base64 response: For each uploaded image, the AI service returns a JSON object containing detections and a base64-encoded annotated image with bounding boxes.
	•	Dockerized: Each service has its own Dockerfile, orchestrated by docker-compose.
	•	Progress bar: Users can track the progress of their image upload from the browser.
	•	Automatic bounding box display: The UI decodes the base64-encoded annotated image and shows it directly in the browser, along with detection data.

Architecture Overview
	1.	User opens http://localhost:5000/ (the UI service).
	2.	UI service presents an HTML form to upload an image.
	•	AJAX handles the upload, displaying a progress bar.
	3.	UI service receives the file at /upload, forwards it to the AI service (POST /detect).
	4.	AI service uses Ultralytics YOLOv8 to run inference:
	•	It detects objects, draws bounding boxes, and encodes the result to base64.
	•	Returns JSON = { "detections": [...], "annotated_image": "<base64 string>" }.
	5.	UI passes that JSON response back to the browser.
	6.	Browser displays the JSON detection output and the bounding-box image.

Folder Structure

object_detection_microservice/
│
├── ai_backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── inference.py
│
├── ui_backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app.py
│   └── templates/
│       └── index.html
│
└── docker-compose.yml

	•	ai_backend
	•	inference.py: Flask service using YOLOv8.
	•	Dockerfile: Container configuration for AI service.
	•	requirements.txt: AI service Python dependencies.
	•	ui_backend
	•	app.py: Flask service hosting the frontend and proxying requests to AI backend.
	•	templates/index.html: The HTML page with an upload form, progress bar, and annotated image preview.
	•	Dockerfile: Container configuration for UI service.
	•	requirements.txt: UI service Python dependencies.
	•	docker-compose.yml: Orchestrates both services.

Prerequisites
	•	Docker (version 20+ recommended)
	•	docker-compose (v1.29+ or Docker Engine with Compose plugin)
	•	Internet connection to pull the YOLOv8 model (or pre-download YOLO weights if needed)

Setup & Running
	1.	Clone or download this repository.
	2.	Navigate to the root directory object_detection_microservice/.
	3.	Build and start containers:

docker-compose build
docker-compose up


	4.	Wait for both containers (ui_backend and ai_backend) to start.
	5.	Open your browser at http://localhost:5000/.

Usage & Testing
	1.	At http://localhost:5000/, you’ll see an upload form with a progress bar.
	2.	Select an image file (JPEG/PNG) and click Upload & Detect.
	3.	The progress bar will update as the image uploads.
	4.	Upon success, the page will display:
	•	JSON detections (bounding boxes, classes, confidences).
	•	An annotated image with bounding boxes drawn (base64-encoded).
	5.	Check Logs:
	•	docker-compose logs -f ui_backend
	•	docker-compose logs -f ai_backend

Configuration
	•	YOLO Model: By default, the AI service loads yolov8n.pt (the nano model). Adjust this in inference.py if you want a different YOLOv8 variant.
	•	Confidence Threshold: In inference.py, the call model.predict(source=np_image, imgsz=640, conf=0.25) sets the confidence threshold to 0.25. Tweak this as needed.
	•	Ports:
	•	UI: Mapped to host’s port 5000.
	•	AI: Mapped to host’s port 5001.
Adjust docker-compose.yml as desired.

How It Works
	1.	UI (ui_backend):
	•	Serves index.html at root (/) via Flask’s render_template.
	•	Implements /upload endpoint:
	•	Receives the uploaded file.
	•	Uses requests to forward that file to AI_BACKEND_URL (defaults to http://ai_backend:5001/detect).
	•	Returns the JSON response (detections + annotated image) to the browser.
	2.	AI (ai_backend):
	•	Flask endpoint /detect expects a file under 'image'.
	•	Uses Ultralytics YOLOv8 to run inference:
	•	model = YOLO('yolov8n.pt')
	•	result = model.predict(...)
	•	Extracts bounding boxes, confidences, classes, etc.
	•	Draws bounding boxes on the image via OpenCV (cv2.rectangle, cv2.putText).
	•	Encodes the annotated image as base64.
	•	Returns a single JSON:

{ 
  "detections": [...], 
  "annotated_image": "<base64>" 
}


	3.	Browser decodes the base64 string and renders it as an <img>.

Troubleshooting
	•	Connection Refused: Make sure Docker containers are running (docker-compose up) and no firewall blocks ports 5000/5001.
	•	Model Download Issues: If ultralytics can’t download the YOLOv8 weights automatically, either place the weights manually or ensure you have an internet connection.
	•	Performance: YOLOv8n on CPU might be slow for large images. Consider using a smaller image size or upgrading to GPU-based Docker if available.
	•	Memory Errors: Large images or insufficient system RAM might cause memory issues. Resize or optimize images if needed.

References
	•	Ultralytics YOLOv8 Documentation
	•	Flask Documentation
	•	Docker Documentation
	•	OpenCV
	•	Pillow

Enjoy your end-to-end Ultralytics YOLOv8 microservice with a simple web-based UI!

If you have any questions or issues, please open an issue or contact the repository maintainer.
