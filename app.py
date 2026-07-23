
from flask import Flask, render_template, request, redirect
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
import os
import json
from datetime import datetime

app = Flask(__name__)

# ================= LOAD MODEL =================

model = tf.keras.models.load_model("plant_model.h5")

class_names = [
    "aloe_vera", "amruthaballi","arali","ashoka","ashwagandha","bamboo","beans","betal","bhrami","castor",
     "coriender", "curry_leaf","ganike","guava","henna","hibiscus","honge","insulin","jackfruit","jasmine",
     "lemon", "mango", "mint", "neem","nithyapushpa","nooni","papaya","pomogranate","pumpkin","raktachandini",
     "rose","sapota","seethapala","spinach","tamarind","tomato","tulsi","wood_sorel"
]

# ================= LOAD PLANT INFO =================

with open("plant_info.json", "r", encoding="utf-8") as f:
    plant_info = json.load(f)



# ================= STORAGE =================

HISTORY_FILE = "prediction_history.json"

def load_history():

    if os.path.exists(HISTORY_FILE):

        with open(HISTORY_FILE, "r") as file:
            return json.load(file)

    return []

def save_history(history):

    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)

history = load_history()

# ================= HOME =================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")


# ================= REAL ACCURACY ADMIN =================

@app.route("/admin")
def admin():

    total = len(history)

    evaluated = [
        h for h in history
        if h.get("status") in ["Correct", "Wrong"]
    ]

    correct = sum(
        1 for h in evaluated
        if h["status"] == "Correct"
    )

    evaluated_total = len(evaluated)

    accuracy = round(
        (correct / evaluated_total) * 100,
        2
    ) if evaluated_total > 0 else 0

    wrong = evaluated_total - correct

    return render_template(
        "admin.html",
        history=history,
        total=total,
        correct=correct,
        wrong=wrong,
        accuracy=accuracy
    )


# ================= VERIFY PREDICTION =================

@app.route("/verify/<int:index>/<result>")
def verify(index, result):

    if result == "correct":

        history[index]["status"] = "Correct"

        history[index]["actual_species"] = history[index]["predicted_species"]

    else:

        history[index]["status"] = "Wrong"

    save_history(history)

    return redirect("/admin")






# ================= PREDICTION =================

@app.route("/predict", methods=["POST"])
def predict():

    file = request.files["image"]

    os.makedirs("static/uploads", exist_ok=True)

    filepath = os.path.join("static/uploads", file.filename)
    file.save(filepath)

    img = image.load_img(filepath, target_size=(224, 224))

    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0

    prediction = model.predict(img_array)

    # FIXED: correct indentation + safe formatting
    predicted_class = class_names[np.argmax(prediction)].strip().lower()
    confidence = round(float(np.max(prediction)) * 100, 2)

    # DEFAULT INFO (prevents crash if key missing)
    default_info = {
        "scientific_name": "Unknown",
        "common_name": predicted_class,
        "image": "/static/images/default.png",
        "medicinal_use": ["No data available"],
        "region": ["Unknown"]
    }

   
    info = plant_info.get(predicted_class, default_info)

   
# Initially unknown until admin verifies

    actual_species = ""

    status = "Pending"

    # ================= STORE HISTORY =================

    prediction_record = {

        "image": filepath.replace("\\", "/"),

        "predicted_species": predicted_class,

        "actual_species": actual_species,

        "confidence": confidence,

        "status": status,

        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    }

    history.append(prediction_record)

    save_history(history)

    return render_template(
        "result.html",
        common_name=info["common_name"],
        info=info,
        confidence=confidence,
        image=filepath
    )


 
# ================= REGION PAGE =================

@app.route("/region/<plant>")
def region(plant):

    plant_key = plant.strip().lower().replace(" ", "_")

    default_info = {
        "region": ["No region data available"]
    }

    info = plant_info.get(plant_key, default_info)

    return render_template(
        "region.html",
        plant=plant.replace("_", " ").title(),
        region=info["region"]
    )


# ================= MEDICINAL PAGE =================

@app.route('/medicinal/<plant>')
def medicinal(plant):

    with open('plant_info.json', 'r') as file:
        data = json.load(file)

    info = data.get(plant)

    return render_template(
        'medicinal.html',
        info=info,
        plant_name=info["common_name"]
    )

# ================= RUN =================

if __name__ == "__main__":
    app.run(debug=True)