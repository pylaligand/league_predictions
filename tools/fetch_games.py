#!/usr/bin/env python

import argparse
import json
import sys
import urllib.request as http


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--competition", required=True)
    parser.add_argument("--phase", required=True)
    parser.add_argument("--poule", required=True)
    args = parser.parse_args()

    server = "https://api-dofa.fff.fr"
    url = f"{server}/api/compets/{args.competition}/phases/{args.phase}/poules/{args.poule}/matchs"
    while True:
        data = json.loads(http.urlopen(url).read().decode())

        for match in data["hydra:member"]:
            journee = match["poule_journee"]["name"]
            home_team = match["home"]["short_name"]
            away_team = match["away"]["short_name"]
            home_score = match["home_score"] if match["home_score"] != None else "?"
            away_score = match["away_score"] if match["away_score"] != None else "?"
            print(f"[{journee}] {home_team} vs. {away_team} {home_score}-{away_score}")

        view = data["hydra:view"]
        if view["@id"] == view["hydra:last"]:
            break
        url = f"{server}{view['hydra:next']}"

    return 0


if __name__ == "__main__":
    sys.exit(main())
