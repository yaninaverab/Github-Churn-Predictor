# GitHub Churn Predictor

![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-green)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-Random%20Forest-orange)
![Docker](https://img.shields.io/badge/Docker-Containerized-blue)
![License](https://img.shields.io/badge/License-MIT-lightgrey)

## Overview

GitHub Churn Predictor is an end-to-end machine learning project that predicts whether a GitHub user is likely to become inactive based on repository activity, engagement, popularity, and contribution metrics.

Originally developed as part of a university Data Science assignment, the project was expanded into a portfolio-ready machine learning system that covers the complete workflow from data collection and feature engineering to model deployment through a REST API.

### Key Features

* Custom data collection using the GitHub API
* Dataset built from approximately 1,200 GitHub users
* Feature engineering and behavioral analysis
* Random Forest classification model
* Target leakage detection and removal
* FastAPI prediction service
* Dockerized deployment
* Cross-validation performance evaluation

## System Architecture

```text
GitHub API
     │
     ▼
Data Collection Scripts
     │
     ▼
Raw Dataset
     │
     ▼
Feature Engineering
     │
     ▼
Training Dataset
     │
     ▼
Random Forest Model
     │
     ▼
FastAPI REST API
     │
     ▼
Predictions
```

## Dataset

The dataset was created using two custom Python scrapers that interact with the GitHub API.

Approximately 1,200 GitHub users were collected along with repository statistics and account metadata.

### Raw Data

```text
data/raw/
├── github_users.csv
├── github_users1.csv
├── repo_stats.csv
└── final_users.csv
```

### Processed Data

```text
data/processed/
└── features_dataset.csv
```

The processed dataset contains engineered features used for model training and evaluation.

## Churn Definition

A user is labeled as churned when:

```python
days_since_activity > 180
```

This definition was used only to generate the target variable.

The feature itself was intentionally excluded from training to prevent target leakage.

## Feature Engineering

The final model uses the following engineered features:

| Feature          | Description                                            |
| ---------------- | ------------------------------------------------------ |
| repos_per_year   | Repository creation rate                               |
| stars_per_repo   | Average stars received per repository                  |
| forks_per_repo   | Average forks received per repository                  |
| has_no_repos     | Indicates whether a user has no repositories           |
| is_popular       | Indicates whether a user has more than 100 followers   |
| has_popular_repo | Indicates whether a repository has more than 100 stars |
| engagement_score | Combined activity and engagement metric                |
| reputation_score | Combined popularity metric                             |
| creator_score    | Repository creation and contribution metric            |

## Leakage Detection

During exploratory analysis, the feature `days_since_activity` showed a strong correlation with the target variable.

Because churn was defined directly from this value, including it would allow the model to learn the label definition instead of learning behavioral patterns.

To ensure a realistic predictive model, this feature was removed from the final training pipeline.

This decision and supporting analysis are documented in the project notebook.

## Model

The final model is a Random Forest Classifier:

```python
RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)
```

The dataset was split using:

```python
train_test_split(
    test_size=0.20,
    stratify=y,
    random_state=42
)
```

## Performance

### Classification Report

| Class       | Precision | Recall | F1-Score |
| ----------- | --------- | ------ | -------- |
| Active (0)  | 0.79      | 0.86   | 0.82     |
| Churned (1) | 0.58      | 0.46   | 0.51     |

### Overall Accuracy

```text
74%
```

### 5-Fold Cross Validation

| Metric    | Score         |
| --------- | ------------- |
| Accuracy  | 0.748 ± 0.029 |
| Precision | 0.610 ± 0.069 |
| Recall    | 0.478 ± 0.043 |
| F1 Score  | 0.534 ± 0.046 |

## Project Structure

```text
project/
│
├── app/
│   ├── main.py
│   ├── model.py
│   ├── features.py
│   ├── scrapper.py
│   ├── extrainfoscrapper.py
│   └── model.pkl
│
├── data/
│   ├── raw/
│   │   ├── github_users.csv
│   │   ├── github_users1.csv
│   │   ├── repo_stats.csv
│   │   └── final_users.csv
│   │
│   └── processed/
│       └── features_dataset.csv
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## API Usage

### Endpoint

```http
POST /predict
```

### Example Request

```json
{
  "public_repos": 15,
  "followers": 80,
  "following": 40,
  "total_stars": 50,
  "total_forks": 10,
  "max_repo_stars": 50,
  "account_age_days": 1500
}
```

### Example Response

```json
{
  "churned": false,
  "churn_probability": 0.42
}
```

## Running Locally

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Swagger documentation:

```text
http://localhost:8000/docs
```

## Running with Docker

```bash
docker-compose up --build
```

## Technologies

* Python
* Pandas
* NumPy
* Scikit-Learn
* FastAPI
* Uvicorn
* Docker
* GitHub API

## Future Work

* Increase dataset size
* Evaluate Gradient Boosting and XGBoost
* Add SHAP explainability
* Deploy to the cloud
* Create a web dashboard
* Automate data collection pipelines

## Author

Yanina Vera

GitHub: https://github.com/yaninaverab

LinkedIn: https://www.linkedin.com/in/yanina-vera-56947240a/
