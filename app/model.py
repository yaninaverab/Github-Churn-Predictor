import pandas as pd
import joblib

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# ==========================================
# LOAD DATA
# ==========================================

df = pd.read_csv(
    "data/processed/features_dataset.csv"
)

# ==========================================
# FEATURES SELECTED
# days_since_activity is intentionally excluded.
# Although RFE selected it, it directly encodes
# the churn label (churn = days_since_activity > 180),
# which constitutes target leakage. The model would
# achieve perfect accuracy by reading back the label
# definition rather than learning real behavior.
# ==========================================

selected_features = [
    "repos_per_year",
    "stars_per_repo",
    "forks_per_repo",
    "has_no_repos",
    "is_popular",
    "has_popular_repo",
    "engagement_score",
    "reputation_score",
    "creator_score"
]

X = df[selected_features]
y = df["churn"]

# ==========================================
# TRAIN TEST SPLIT
# ==========================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ==========================================
# RANDOM FOREST
# class_weight="balanced" compensates for the
# 70/30 active/churned split in the dataset.
# ==========================================

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42,
    class_weight="balanced"
)

model.fit(X_train, y_train)

# ==========================================
# EVALUATION
# ==========================================

predictions = model.predict(X_test)

print(classification_report(y_test, predictions))

# 5-fold cross-validation for a more robust estimate
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

for metric in ["accuracy", "f1", "precision", "recall"]:
    scores = cross_val_score(model, X, y, cv=cv, scoring=metric)
    print(f"CV {metric}: {scores.mean():.3f} ± {scores.std():.3f}")

# ==========================================
# SAVE MODEL
# ==========================================

joblib.dump(model, "app/model.pkl")

print("\nModel saved as app/model.pkl")