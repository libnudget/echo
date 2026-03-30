#!/usr/bin/env python3

import json
import os
import re


issue_number = int(os.environ["ISSUE_NUMBER"])
issue_title = os.environ["ISSUE_TITLE"]
issue_body = os.environ.get("ISSUE_BODY", "")
stopwords = re.compile(os.environ["STOPWORDS"], re.IGNORECASE)
result_limit = int(os.environ.get("RESULT_LIMIT", "10"))

with open(os.environ["ISSUES_FILE"], encoding="utf-8") as fh:
    issues = json.load(fh)


def tokenize(text: str) -> set[str]:
    terms = re.findall(r"[A-Za-z0-9]+", (text or "").lower())
    return {
        term for term in terms if len(term) >= 4 and not stopwords.match(term)
    }


source_title_terms = tokenize(issue_title)
source_all_terms = tokenize(f"{issue_title}\n{issue_body}")

results = []
for item in issues:
    if item["number"] == issue_number:
        continue

    target_title_terms = tokenize(item.get("title", ""))
    target_all_terms = tokenize(f'{item.get("title", "")}\n{item.get("body", "")}')

    title_overlap = source_title_terms & target_title_terms
    body_overlap = source_all_terms & target_all_terms
    score = len(title_overlap) * 3 + len(body_overlap)

    if issue_title.strip().lower() == item.get("title", "").strip().lower():
        score += 10

    if score <= 0:
        continue

    results.append(
        {
            "number": item["number"],
            "title": item["title"],
            "state": item["state"],
            "url": item["url"],
            "score": score,
        }
    )

results.sort(key=lambda item: (-item["score"], item["number"]))

with open(os.environ["RESULTS_FILE"], "w", encoding="utf-8") as fh:
    json.dump(results[:result_limit], fh)
