# 🌿 Plant Species Identification System

## Overview
A Flask-based web application that identifies medicinal plant species using a Convolutional Neural Network (CNN). Users can upload a plant image, and the system predicts the species with a confidence score and displays detailed plant information.

## Features
- Plant species prediction using a trained CNN model
- Upload plant images through a web interface
- Displays:
  - Common Name
  - Scientific Name
  -Region Found
  - Medicinal Uses
  - Confidence Score
- Admin dashboard for monitoring prediction history and model performance

## Technologies Used
- Python
- Flask
- TensorFlow / Keras
- HTML
- CSS
- JavaScript
- JSON

## Project Structure

```
app.py
plant_model.h5
templates/
static/
plant_info.json
class_indices.json
prediction_history.json
requirements.txt
README.md
```

## Installation

```bash
pip install -r requirements.txt
python app.py
```

## Author

**Soundarya Achalakar**