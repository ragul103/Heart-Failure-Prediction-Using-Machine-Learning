from flask import Flask, render_template, request, redirect, url_for
import joblib
import pandas as pd

app = Flask(__name__)

model = joblib.load("heart_model.pkl")
scaler = joblib.load("scaler.pkl")

FEATURES = [
    "age",
    "sex",
    "ejection_fraction",
    "serum_creatinine",
    "serum_sodium",
    "high_blood_pressure"
]


@app.route("/")
def home():
    data = app.config.pop("PREDICTION_DATA", None)
    return render_template("index.html", **(data or {}))



@app.route("/predict", methods=["POST"])
def predict():
    patient_name = request.form["patient_name"]

    data = [float(request.form[f]) for f in FEATURES]
    df = pd.DataFrame([data], columns=FEATURES)
    scaled = scaler.transform(df)

    pred = model.predict(scaled)[0]
    prob = model.predict_proba(scaled)[0][1] * 100

    result = "High Risk of Death" if pred == 1 else "Low Risk (Survival)"

    # store result temporarily
    app.config["PREDICTION_DATA"] = {
        "patient_name": patient_name,
        "prediction": result,
        "probability": f"{prob:.2f}%"
    }

    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
