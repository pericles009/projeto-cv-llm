## 🛒 AI Product Label Analyzer (CV + LLM)
This project is a computer vision system that detects products in real-time using a webcam, captures high-quality crops, and sends them to a backend API for analysis. The backend uses OCR (Optical Character Recognition) and a Large Language Model (Google Gemini) to interpret product labels and extract structured data (Category, Brand, Details).

## 🌐 Live Demo (Public API)

The backend server of this project is deployed on **Hugging Face Spaces**. You can interact with the API directly through the browser without needing to run the server locally.

* **Interactive Documentation (Swagger UI):** [Access API Docs](https://periclesrodrigues01-yolo-gemini-api.hf.space/docs)
* **API Endpoint:** `https://periclesrodrigues01-yolo-gemini-api.hf.space/`

> **Note:** This demo runs on the Hugging Face **Free Tier (CPU)**. Processing times for OCR and LLM analysis might take a few seconds.


## 🚀 Key Features
Real-time Detection: Uses YOLOv8 to detect objects and filter for products, ignoring people.

Intelligent Text Extraction: Implements EasyOCR with grayscale preprocessing to read text from product labels.

Semantic Analysis: Uses Google Gemini (LLM) to parse raw OCR text into structured data: Category, Brand, and Details.

Microservice Architecture: Separated into a capture client and a FastAPI server, containerized with Docker.

## 🛠️ Tech Stack
Client: Python, OpenCV, Ultralytics YOLOv8, Requests.

Server: Python, FastAPI, Uvicorn.

AI/ML: EasyOCR (PyTorch), Google Generative AI (Gemini).

Infrastructure: Docker.
