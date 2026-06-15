import pandas as pd
from datetime import datetime

SELECTED_FEATURES = [
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

def generate_features(data: dict) -> list:
    """
    Accepts a dict of raw user values and returns
    a list of feature values in SELECTED_FEATURES order.
    """
    public_repos    = data.get("public_repos", 0)
    followers       = data.get("followers", 0)
    following       = data.get("following", 0)
    total_stars     = data.get("total_stars", 0)
    total_forks     = data.get("total_forks", 0)
    max_repo_stars  = data.get("max_repo_stars", 0)
    account_age_days = data.get("account_age_days", 1)

    account_age_years = max(account_age_days / 365, 0.01)

    repos_per_year   = public_repos / account_age_years
    stars_per_repo   = total_stars  / (public_repos + 1)
    forks_per_repo   = total_forks  / (public_repos + 1)
    has_no_repos     = int(public_repos == 0)
    is_popular       = int(followers > 100)
    has_popular_repo = int(max_repo_stars > 100)
    engagement_score = followers + following + public_repos + total_stars
    reputation_score = followers + total_stars + total_forks
    creator_score    = (public_repos * 2) + total_stars

    return [
        repos_per_year,
        stars_per_repo,
        forks_per_repo,
        has_no_repos,
        is_popular,
        has_popular_repo,
        engagement_score,
        reputation_score,
        creator_score
    ]