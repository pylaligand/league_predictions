#!/usr/bin/python

from __future__ import division

import argparse

from algo import GameSimulator
from elo import EloEngine
from parsing import load_season


class Stats(object):
    _KEY_SECOND_POINTS = 0
    _KEY_TARGET_RANK = 1
    _KEY_TARGET_POINTS = 2
    _KEYS = [_KEY_SECOND_POINTS, _KEY_TARGET_RANK, _KEY_TARGET_POINTS]

    def __init__(self, team):
        self._team = team
        self._count = 0
        self._accumulators = {}

    def ingest(self, ranked_teams):
        self._count = self._count + 1
        for key in Stats._KEYS:
            self._accumulators.setdefault(key, []).append(
                self._extract(ranked_teams, key))

    def _extract(self, ranked_teams, key):
        if key == Stats._KEY_SECOND_POINTS:
            return ranked_teams[1].points
        elif key == Stats._KEY_TARGET_RANK:
            if not self._team:
                return 0
            return 1 + next(
                i for i, t in enumerate(ranked_teams) if t.name == self._team)
        elif key == Stats._KEY_TARGET_POINTS:
            if not self._team:
                return 0
            return 1 + next(t.points
                            for t in ranked_teams if t.name == self._team)

    def _compute(self, key):
        values = self._accumulators[key]
        return round(sum(values) / len(values), 2)

    def second_rank_points(self):
        return self._compute(Stats._KEY_SECOND_POINTS)

    def team_rank(self):
        return self._compute(Stats._KEY_TARGET_RANK)

    def team_points(self):
        return self._compute(Stats._KEY_TARGET_POINTS)


def _load_season(file, validate=True):
    with open(file, 'r') as input_file:
        lines = [l.strip() for l in input_file.readlines()]
    return load_season(lines, validate=validate)


def _fix_season(season, predictions):
    for gameday in season.gamedays:
        for game in gameday.games:
            if game.played():
                continue
            if game in predictions:
                game.update_scores(predictions[game])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--season', required=True)
    parser.add_argument('--predictions')
    parser.add_argument('--iterations', type=int, default=10000)
    parser.add_argument('--team')
    args = parser.parse_args()

    season = _load_season(args.season)

    if args.predictions:
        data = _load_season(args.predictions, validate=False)
        predictions = dict((gd, gd) for gd in data.gamedays[0].games)
        _fix_season(season, predictions)

    stats = Stats(args.team)
    for i in range(args.iterations):
        engine = EloEngine(start=1000, k=20, min=100)
        simulator = GameSimulator(season, engine)
        simulator.simulate()
        ranked_teams = sorted(simulator.teams(),
                              key=lambda t: t.points,
                              reverse=True)
        stats.ingest(ranked_teams)

    def _print(stat, value):
        print('{:20s} {:.2f}'.format(stat, value))

    _print('Second place points', stats.second_rank_points())
    if args.team:
        _print('Team rank', stats.team_rank())
        _print('Team points', stats.team_points())


if __name__ == "__main__":
    main()
