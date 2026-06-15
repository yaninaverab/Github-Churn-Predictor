import pandas as pd

df = pd.read_csv(
    "data/processed/features_dataset.csv"
)

print(df["churn"].value_counts())

print()

print(df["churn"].value_counts(normalize=True))