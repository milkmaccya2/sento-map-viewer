#!/usr/bin/env python3
"""
sento-visits.csv と sento-ranking-with-urls.csv を結合して
Webアプリ用の sento-data.json を生成する。
"""

import csv
import json
import re
import sys
from collections import defaultdict

VISITS_CSV = "/Users/yokoyama/sento-visits.csv"
RANKING_CSV = "/Users/yokoyama/sento-ranking-with-urls.csv"
OUTPUT_JSON = "/Users/yokoyama/git/sento-map/public/sento-data.json"


def parse_latlng(s: str):
    """'35.123°, 139.456°' -> (35.123, 139.456)"""
    m = re.findall(r"([\d.]+)°", s)
    if len(m) == 2:
        return float(m[0]), float(m[1])
    return None


def main():
    # 1. ranking CSV から施設情報を読む (name -> {name_ja, url, rank})
    ranking = {}
    with open(RANKING_CSV, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            ranking[row["name"]] = {
                "name_ja": row["name_ja"],
                "url": row["url"] if row["url"] != "N/A" else None,
                "rank": int(row["rank"]),
            }

    # 2. visits CSV から訪問日・座標を集約
    facilities: dict[str, dict] = defaultdict(lambda: {
        "dates": [],
        "lat": None,
        "lng": None,
        "address": "",
    })

    with open(VISITS_CSV, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            visit_name = row["name"]
            # ranking の名前と完全一致 or 前方一致でマッチ
            name = None
            visit_clean = visit_name.replace('"', '').replace("'", "")
            if visit_name in ranking:
                name = visit_name
            else:
                for rname in ranking:
                    rname_clean = rname.replace('"', '').replace("'", "")
                    if (visit_clean.startswith(rname_clean)
                            or rname_clean.startswith(visit_clean)):
                        name = rname
                        break
            if name is None:
                continue
            fac = facilities[name]
            fac["dates"].append(row["date"])
            if fac["lat"] is None:
                coords = parse_latlng(row["latLng"])
                if coords:
                    fac["lat"], fac["lng"] = coords
            if not fac["address"]:
                fac["address"] = row["address"]

    # 3. JSON 生成
    result = []
    for name, info in ranking.items():
        fac = facilities.get(name)
        if not fac or fac["lat"] is None:
            print(f"WARNING: no visit data for {name} ({info['name_ja']})", file=sys.stderr)
            continue

        dates = sorted(fac["dates"])
        # 年ごとの訪問回数
        by_year: dict[str, int] = defaultdict(int)
        for d in dates:
            by_year[d[:4]] += 1

        result.append({
            "name": name,
            "name_ja": info["name_ja"],
            "rank": info["rank"],
            "lat": fac["lat"],
            "lng": fac["lng"],
            "address": fac["address"],
            "url": info["url"],
            "total_visits": len(dates),
            "first_visit": dates[0] if dates else None,
            "last_visit": dates[-1] if dates else None,
            "visits_by_year": dict(sorted(by_year.items())),
            "visit_dates": dates,
        })

    result.sort(key=lambda x: x["rank"])

    import os
    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"Generated {OUTPUT_JSON} with {len(result)} facilities")


if __name__ == "__main__":
    main()
