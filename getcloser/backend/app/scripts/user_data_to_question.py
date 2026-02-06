import csv
import json

input_file = "input.csv"
output_file = "output.csv"

rows = []
id_counter = 1

with open(input_file, newline="", encoding="utf-8-sig") as f:
    reader = csv.DictReader(f)

    for row in reader:
        user_id = row["idx"]
        if user_id == "idx":
            # Skip duplicated header row in data.
            continue

        # category 1: 관심사 키워드 (JSON 리스트)
        raw_interest_keywords = (row.get("interest_keywords") or "").strip()
        if raw_interest_keywords:
            try:
                interests = json.loads(raw_interest_keywords)
            except json.JSONDecodeError:
                # Fallback for non-JSON input like "a,b,c"
                interests = [value.strip() for value in raw_interest_keywords.split(",") if value.strip()]
        else:
            interests = []
        for interest in interests:
            rows.append([
                id_counter,
                user_id,
                1,
                interest
            ])
            id_counter += 1

        # category 2: 계절
        rows.append([
            id_counter,
            user_id,
            2,
            row["favorite_season"]
        ])
        id_counter += 1

        # category 3: MBTI
        rows.append([
            id_counter,
            user_id,
            3,
            row["mbti"]
        ])
        id_counter += 1

# CSV 저장
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "user_id", "category", "answer"])
    writer.writerows(rows)
