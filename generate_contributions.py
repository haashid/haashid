#!/usr/bin/env python3
"""
Contribution & Green Graph Generator for Muhammad Haashid
---------------------------------------------------------
This script distributes commits naturally across chosen dates so your GitHub
contribution calendar lights up green with authentic density.

Usage:
    python generate_contributions.py --current 260 --target 476 --email haashid.0607@gmail.com
"""

import os
import subprocess
import datetime
import random
import argparse

def generate_commits(current_count=260, target_count=476, author_name="haashid", author_email="haashid.0607@gmail.com", days_back=160):
    commits_needed = target_count - current_count
    if commits_needed <= 0:
        print(f"Target ({target_count}) is already reached or less than current ({current_count}). Nothing to do.")
        return

    print(f"==================================================")
    print(f"GitHub Contribution Graph Generator")
    print(f"Current contributions : {current_count}")
    print(f"Target contributions  : {target_count}")
    print(f"New commits to create : {commits_needed}")
    print(f"Author                : {author_name} <{author_email}>")
    print(f"Date distribution     : Over the past {days_back} days")
    print(f"==================================================")

    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=days_back)

    # Configure local git
    subprocess.run(["git", "config", "user.name", author_name], check=True)
    subprocess.run(["git", "config", "user.email", author_email], check=True)

    # Select candidate days with realistic weekday vs weekend weighting
    current_date = start_date
    candidate_days = []
    while current_date <= end_date:
        weekday = current_date.weekday()
        prob = 0.75 if weekday < 5 else 0.45
        if random.random() < prob:
            candidate_days.append(current_date)
        current_date += datetime.timedelta(days=1)

    # Distribute commits across days
    if len(candidate_days) > commits_needed:
        random.shuffle(candidate_days)
        candidate_days = candidate_days[:commits_needed]
        commits_per_day = {d: 1 for d in candidate_days}
    else:
        commits_per_day = {d: 1 for d in candidate_days}
        remaining = commits_needed - len(candidate_days)
        while remaining > 0:
            d = random.choice(candidate_days)
            if commits_per_day[d] < 5:
                commits_per_day[d] += 1
                remaining -= 1

    sorted_days = sorted(commits_per_day.keys())
    log_file = "contributions.txt"

    commit_messages = [
        "feat(core): optimize distributed telemetry pipeline",
        "perf(edge): improve MQTT sensor payload serialization",
        "refactor(ai): streamline LangGraph decision router",
        "fix(auth): update token refresh validation logic",
        "docs(api): document multi-agent orchestration hooks",
        "chore(deps): bump cryptographic hash utility libraries",
        "feat(ui): refine dashboard responsive breakpoints",
        "test(contract): add unit tests for state channel settlements",
        "perf(cache): implement tiered Redis in-memory cache",
        "feat(iot): add hardware watchdog handler for ESP32",
        "refactor(db): optimize query indexing for audit traces",
        "style: polish markdown code formatting and schema specs",
        "feat(model): integrate multimodal embedding comparisons",
        "fix(network): handle reconnect jitter on websocket stream",
        "build: configure automated CI verification pipeline",
        "feat(analytics): add real-time aggregation metrics",
        "refactor(security): harden role-based permission gates",
        "docs: update project architecture and sequence diagrams"
    ]

    commit_count = 0
    for day in sorted_days:
        num = commits_per_day[day]
        for _ in range(num):
            commit_count += 1
            hour = random.randint(9, 21)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            dt = datetime.datetime.combine(day, datetime.time(hour, minute, second))
            iso_date = dt.strftime("%Y-%m-%dT%H:%M:%S")

            with open(log_file, "a", encoding="utf-8") as f:
                f.write(f"Commit #{commit_count}: {iso_date} - System build update\n")

            subprocess.run(["git", "add", log_file], check=True)
            msg = random.choice(commit_messages)
            env = os.environ.copy()
            env["GIT_AUTHOR_DATE"] = iso_date
            env["GIT_COMMITTER_DATE"] = iso_date

            subprocess.run(
                ["git", "commit", "-m", f"{msg} (#{commit_count})"],
                env=env,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True
            )

    print(f"Done! Created {commit_count} commits successfully.")
    print("Push to GitHub using:")
    print("  git remote add origin https://github.com/haashid/haashid.git")
    print("  git branch -M main")
    print("  git push -u origin main --force")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate natural backdated commits to turn GitHub graph green")
    parser.add_argument("--current", type=int, default=260, help="Current number of contributions")
    parser.add_argument("--target", type=int, default=476, help="Target number of contributions")
    parser.add_argument("--name", type=str, default="haashid", help="Git user.name")
    parser.add_argument("--email", type=str, default="haashid.0607@gmail.com", help="Git user.email (must match verified GitHub email)")
    parser.add_argument("--days", type=int, default=160, help="Number of past days to distribute commits over")
    args = parser.parse_args()

    generate_commits(
        current_count=args.current,
        target_count=args.target,
        author_name=args.name,
        author_email=args.email,
        days_back=args.days
    )
