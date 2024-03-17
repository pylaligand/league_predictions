from __future__ import annotations

from collections.abc import Iterable, Iterator, Sized
from datetime import date
from typing import List


class Team(object):
    name: str

    def __init__(self, name: str):
        self.name = name

    def __str__(self) -> str:
        return self.name

    def __eq__(self, other: Team) -> bool:
        return self.name == other.name

    def __hash__(self) -> int:
        return hash((self.name))


class Game(object):
    # TODO: 1 --> home, 2 --> away
    team_1: Team
    score_1: int
    team_2: Team
    score_2: int

    def __init__(self, team_1: Team, score_1: int, team_2: Team, score_2: int):
        self.team_1 = team_1
        self.score_1 = score_1
        self.team_2 = team_2
        self.score_2 = score_2

    def played(self) -> bool:
        return self.score_1 >= 0 and self.score_2 >= 0

    def update_scores(self, other: Game):
        self.score_1 = other.score_1
        self.score_2 = other.score_2

    def __eq__(self, other: Game) -> bool:
        return self.team_1 == other.team_1 and self.team_2 == other.team_2

    def __hash__(self) -> int:
        return hash((self.team_1, self.team_2))

    def __str__(self) -> str:
        matchup = f"{self.team_1} - {self.team_2}"
        if not self.played():
            return matchup
        return f"{matchup} ({self.score_1}-{self.score_2})"

    def __repr__(self):
        return self.__str__()


class Gameday(Sized, Iterable):
    index: int
    day: date
    games: List[Game]

    def __init__(self, index: int, day: date):
        self.index = index
        self.day = day
        self.games = []

    def __len__(self) -> int:
        return len(self.games)

    def __iter__(self) -> Iterator[Game]:
        return iter(self.games)

    def add_game(self, game: Game):
        self.games.append(game)

    def __str__(self):
        return f"[{self.index} - {self.day}]"


class Season(Sized, Iterable):
    gamedays: List[Gameday]

    def __init__(self):
        self.gamedays = []

    def __len__(self) -> int:
        return len(self.gamedays)

    def __iter__(self) -> Iterator[Gameday]:
        return iter(sorted(self.gamedays, key=lambda g: g.index))

    def __str__(self):
        return f"Season{len(self)}"

    def add_gameday(self, gameday: Gameday):
        self.gamedays.append(gameday)

    def teams(self):
        result = {}
        for g in self.gamedays[0].games:
            result[g.team_1] = Team(g.team_1)
            result[g.team_2] = Team(g.team_2)
        return result
