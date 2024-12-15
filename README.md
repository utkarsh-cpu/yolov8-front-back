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
