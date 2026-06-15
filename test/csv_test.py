import pandas as pd

df = pd.read_csv("data/raw/final_users.csv")

print(df.shape)
print()
print(df.isnull().sum())