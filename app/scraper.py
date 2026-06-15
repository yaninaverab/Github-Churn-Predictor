import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv

# ==========================================
# LOAD TOKEN
# ==========================================

load_dotenv()

token = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json"
}

# ==========================================
# SEARCH GROUPS
# ==========================================

search_groups = [
    "followers:1..20",
    "followers:21..100",
    "followers:101..1000",
    "followers:>1000"
]

# ==========================================
# STORAGE
# ==========================================

all_users = []

# ==========================================
# COLLECT USERS
# ==========================================

for search_query in search_groups:

    print(f"\nSearching group: {search_query}")

    for page in range(1, 4):  # 3 pages x 100 users

        search_url = "https://api.github.com/search/users"

        params = {
            "q": search_query,
            "per_page": 100,
            "page": page
        }

        response = requests.get(
            search_url,
            headers=headers,
            params=params
        )

        if response.status_code != 200:
            print("Search failed:", response.status_code)
            continue

        users = response.json()["items"]

        print(
            f"Page {page}: Found {len(users)} users"
        )

        # ==========================================
        # GET FULL PROFILE FOR EACH USER
        # ==========================================

        for user in users:

            username = user["login"]

            profile_url = (
                f"https://api.github.com/users/{username}"
            )

            profile_response = requests.get(
                profile_url,
                headers=headers
            )

            if profile_response.status_code != 200:
                print("Failed:", username)
                continue

            profile = profile_response.json()

            all_users.append({
                "username": profile.get("login"),
                "followers": profile.get("followers", 0),
                "following": profile.get("following", 0),
                "public_repos": profile.get("public_repos", 0),
                "created_at": profile.get("created_at"),
                "updated_at": profile.get("updated_at")
            })

            print(
                f"Collected: {username}"
            )

            time.sleep(0.2)

# ==========================================
# CREATE DATAFRAME
# ==========================================

df = pd.DataFrame(all_users)

# Remove duplicates
df = df.drop_duplicates(
    subset=["username"]
)

# ==========================================
# SAVE CSV
# ==========================================

output_path = "data/raw/github_users.csv"

df.to_csv(
    output_path,
    index=False
)

print("\n===================================")
print("SCRAPING COMPLETE")
print("===================================")

print("Rows collected:", len(df))

print("\nFirst 5 rows:")
print(df.head())

print(f"\nSaved to: {output_path}")