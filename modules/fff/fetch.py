import json
import urllib.request as http
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List

from ..objects import Game, Gameday, Season, Team

_SERVER = "https://api-dofa.fff.fr"


@dataclass
class _DataPoint(object):
    journee: int
    date: datetime
    game: Game


def _get_journee_timestamp(datapoints: List[_DataPoint]) -> float:
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


def fetch_season(competition: str, phase: str, poule: str) -> Season:
    games: List[_DataPoint] = []
    url = f"{_SERVER}/api/compets/{competition}/phases/{phase}/poules/{poule}/matchs"

    while True:
        data = json.loads(http.urlopen(url).read().decode())

        for match in data["hydra:member"]:
            games.append(
                _DataPoint(
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
        url = f"{_SERVER}{view['hydra:next']}"

    journees = set(map(lambda dp: dp.journee, games))
    journees_with_ts = {
        j: _get_journee_timestamp(dp for dp in games if dp.journee is j)
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

    return season
