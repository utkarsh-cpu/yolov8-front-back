# yolov8-front-back
# Ultralytics YOLOv8 Object Detection Microservice

This repository demonstrates an **end-to-end object detection pipeline** using **Ultralytics YOLOv8** in a **microservices** architecture. It includes two main services:

1. **AI Backend**: Performs object detection on uploaded images using [Ultralytics YOLOv8](https://docs.ultralytics.com/) (the `yolov8n.pt` model by default). Returns structured JSON detections **plus** a base64-encoded annotated image.
2. **UI Frontend**: A Flask-based service that hosts a simple web page with a file upload form, shows **upload progress**, and displays **both** the detection data (in JSON) and the annotated bounding-box image.

We use **Docker** and **docker-compose** to orchestrate these services.

---

## Table of Contents
1. [Features](#features)  
2. [Architecture Overview](#architecture-overview)  
3. [Folder Structure](#folder-structure)  
4. [Prerequisites](#prerequisites)  
5. [Setup & Running](#setup--running)  
6. [Usage & Testing](#usage--testing)  
7. [Configuration](#configuration)  
8. [How It Works](#how-it-works)  
9. [Troubleshooting](#troubleshooting)  
10. [References](#references)

---

## Features

- **Two microservices**:  
  - A **UI** service in Flask with an **HTML** frontend (upload form + progress bar).  
  - An **AI** service using **Ultralytics YOLOv8** (e.g., `yolov8n.pt`).  
- **JSON + base64 response**: For each uploaded image, the AI backend returns detections **and** an annotated image encoded as a base64 string.
- **Dockerized**: Each service has its own **Dockerfile**, orchestrated by **docker-compose**.
- **Progress bar** on the UI: Visual feedback during upload.
- **Automatic bounding box** display: Decodes the annotated image in the browser, showing detection results.

---

## Architecture Overview

1. The **user** opens `http://localhost:5000/` (UI frontend).
2. The **UI** service hosts an **HTML page** with a file upload form (JavaScript handles the upload, showing a progress bar).
3. The **UI** service receives the uploaded file at `/upload`, then **forwards** it to the **AI** service (`POST /detect`).
4. The **AI** service uses **Ultralytics YOLOv8** to detect objects, draws bounding boxes, **encodes** the annotated image as base64, and returns a JSON response:
   ```json
   {
       "detections": [...],
       "annotated_image": "<base64>"
   }
5. The **UI** service relays that JSON back to the browser.
6. **Browser** displays the JSON detection data and **annotated** image.

---

## Folder Structure

```bash
object_detection_microservice/
├── ai_backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── inference.py
├── ui_backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app.py
│   └── templates/
│       └── index.html
└── docker-compose.yml
```

### Explanation of Folder Structure

- **`ai_backend/`**:
  - **`inference.py`**: Flask service using YOLOv8 for object detection.
  - **`Dockerfile`**: Container configuration for AI service.
  - **`requirements.txt`**: Python dependencies for the AI service.
- **`ui_backend/`**:
  - **`app.py`**: Flask service hosting the frontend and proxying requests to the AI backend.
  - **`templates/index.html`**: HTML page with an upload form, progress bar, and annotated image preview.
  - **`Dockerfile`**: Container configuration for UI service.
  - **`requirements.txt`**: Python dependencies for UI service.
- **`docker-compose.yml`**: Orchestrates both services into a single application.

---

## Prerequisites

- **Docker** (version 20+ recommended)  
- **docker-compose** (v1.29+ or Docker Engine with Compose plugin)  
- **Internet connection** to pull the YOLOv8 model (or pre-download YOLO weights if needed).

---

## Setup & Running

1. Clone or download this repository.  
2. Navigate to the root directory `object_detection_microservice/`.  
3. Build and start containers:

   ```bash
   docker-compose build
   docker-compose up
   ```
   
4.	Wait for both containers (ui_backend and ai_backend) to start.
5.	Open your browser at http://localhost:5002/.

---

## Usage & Testing

1.	Visit http://localhost:5000/ to see an upload form with a progress bar.
2.	Select an image file (JPEG/PNG) and click Upload & Detect.
3.	The progress bar updates as the image uploads.
4.	Upon success, the page displays:
	•	JSON Detections (bounding boxes, classes, confidences).
	•	Annotated Image with bounding boxes (base64-encoded).

# UI Logs
```bash
  docker-compose logs -f ui_backend
```
# AI Logs
```bash
  docker-compose logs -f ai_backend
```



