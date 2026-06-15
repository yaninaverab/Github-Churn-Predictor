import os
import time
import requests
import pandas as pd

from dotenv import load_dotenv
from datetime import datetime, timezone

#Load Token
load_dotenv()

token = os.getenv("GITHUB_TOKEN")

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json"
}

#Load User info
users_df = pd.read_csv(
    "data/raw/github_users.csv"
)

#Storage
repo_stats = []

today = datetime.now(timezone.utc)

#Loop through users and collect repository stats
for index, row in users_df.iterrows():

    username = row["username"]

    print(
        f"\n[{index+1}/{len(users_df)}] {username}"
    )

    repos_url = (
        f"https://api.github.com/users/{username}/repos"
    )

    response = requests.get(
        repos_url,
        headers=headers,
        params={
            "per_page": 100
        }
    )

    if response.status_code != 200:

        print(
            f"Failed: {username}"
        )

        continue

    repos = response.json()

    total_repos = len(repos)

    total_stars = 0
    total_forks = 0

    max_repo_stars = 0
    max_repo_forks = 0

    active_repos = 0

    #Process repositories
    for repo in repos:

        stars = repo.get(
            "stargazers_count",
            0
        )

        forks = repo.get(
            "forks_count",
            0
        )

        total_stars += stars
        total_forks += forks

        max_repo_stars = max(
            max_repo_stars,
            stars
        )

        max_repo_forks = max(
            max_repo_forks,
            forks
        )

        updated_at = repo.get(
            "updated_at"
        )

        if updated_at:

            updated_date = datetime.strptime(
                updated_at,
                "%Y-%m-%dT%H:%M:%SZ"
            ).replace(
                tzinfo=timezone.utc
            )

            days_since_update = (
                today - updated_date
            ).days

            if days_since_update <= 180:
                active_repos += 1

    #feature calculations
    if total_repos > 0:

        avg_stars_per_repo = (
            total_stars / total_repos
        )

        avg_forks_per_repo = (
            total_forks / total_repos
        )

        active_repo_ratio = (
            active_repos / total_repos
        )

    else:

        avg_stars_per_repo = 0
        avg_forks_per_repo = 0
        active_repo_ratio = 0

    repo_stats.append({

        "username": username,

        "total_stars": total_stars,
        "avg_stars_per_repo": avg_stars_per_repo,
        "max_repo_stars": max_repo_stars,

        "total_forks": total_forks,
        "avg_forks_per_repo": avg_forks_per_repo,
        "max_repo_forks": max_repo_forks,

        "active_repos": active_repos,
        "total_repositories_found": total_repos,
        "active_repo_ratio": active_repo_ratio
    })

    time.sleep(0.2)

#Save in a .csv

repo_df = pd.DataFrame(
    repo_stats
)

repo_df.to_csv(
    "data/raw/repo_stats.csv",
    index=False
)

print("\n===================================")
print("REPOSITORY SCRAPING COMPLETE")
print("===================================")

print(repo_df.head())