#!/usr/bin/env python

import argparse
import json
import sys
import urllib.request as http
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List

from src.objects import Game, Gameday, Season, Team


@dataclass
class DataPoint(object):
    journee: int
    date: datetime
    game: Game


def get_journee_timestamp(datapoints: List[DataPoint]) -> float:
    counts: Dict[datetime, int] = {}
    for dp in datapoints:
        if dp.date:
            counts[dp.date] = counts.setdefault(dp.date, 0) + 1
    result = None
    max_count = -1
    for date, count in counts.items():
        if count > max_count:
            result = date
            max_count = count
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--competition", required=True)
    parser.add_argument("--phase", required=True)
    parser.add_argument("--poule", required=True)
    args = parser.parse_args()

    games: List[DataPoint] = []

    server = "https://api-dofa.fff.fr"
    url = f"{server}/api/compets/{args.competition}/phases/{args.phase}/poules/{args.poule}/matchs"
    while True:
        data = json.loads(http.urlopen(url).read().decode())

        for match in data["hydra:member"]:
            games.append(
                DataPoint(
                    journee=int(match["poule_journee"]["name"]),
                    date=(
                        datetime.fromisoformat(match["date"]) if match["date"] else None
                    ),
                    game=Game(
                        team_1=Team(match["home"]["short_name"]),
                        team_2=Team(match["away"]["short_name"]),
                        score_1=int(
                            match["home_score"] if match["home_score"] != None else -1
                        ),
                        score_2=int(
                            match["away_score"] if match["away_score"] != None else -1
                        ),
                    ),
                )
            )

        view = data["hydra:view"]
        if view["@id"] == view["hydra:last"]:
            break
        url = f"{server}{view['hydra:next']}"

    journees = set(map(lambda dp: dp.journee, games))
    journees_with_ts = {
        j: get_journee_timestamp(dp for dp in games if dp.journee is j)
        for j in journees
    }

    season = Season()
    for index, (journee, timestamp) in enumerate(
        sorted(
            journees_with_ts.items(),
            key=lambda p: p[1],
        )
    ):
        gameday = Gameday(index + 1, timestamp.date())
        for dp in games:
            if dp.journee is not journee:
                continue
            gameday.add_game(dp.game)
        season.add_gameday(gameday)

    for gameday in season:
        print("------------------")
        print(gameday)
        for game in gameday:
            print(game)

    return 0


if __name__ == "__main__":
    sys.exit(main())
