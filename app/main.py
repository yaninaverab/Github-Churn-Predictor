from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from features import generate_features, SELECTED_FEATURES

app = FastAPI(title="GitHub Churn Predictor API")

model = joblib.load("model.pkl")


class UserFeatures(BaseModel):
    public_repos: int
    followers: int
    following: int
    total_stars: int
    total_forks: int
    max_repo_stars: int
    account_age_days: int


@app.post("/predict")
def predict_churn(user: UserFeatures):
    features = generate_features(user.model_dump())
    X = np.array([features])
    pred = model.predict(X)[0]
    prob = model.predict_proba(X)[0][1]
    return {
        "churned": bool(pred),
        "churn_probability": round(float(prob), 3)
    }


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/features")
def list_features():
    return {"expected_features": SELECTED_FEATURES}