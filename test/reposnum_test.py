import pandas as pd

df = pd.read_csv("data/raw/final_users.csv")

print(
    (df["public_repos"] != df["total_repositories_found"]).sum()
)

#OUTPUT WAS 297

#to test if the mismatch is due to missing data or an actual discrepancy, we can look at the mismatched rows
mismatch = df[
    df["public_repos"] != df["total_repositories_found"]
]

print(mismatch[
    [
        "username",
        "public_repos",
        "total_repositories_found"
    ]
].head(20))