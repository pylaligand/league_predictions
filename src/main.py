#!/usr/bin/python

import argparse

from algo import GameSimulator
from elo import EloEngine
from parsing import load_season


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    args = parser.parse_args()

    with open(args.file, 'r') as input_file:
        lines = [l.strip() for l in input_file.readlines()]

    season = load_season(lines)
    engine = EloEngine(start=1000, k=20, min=100)
    simulator = GameSimulator(season, engine)
    simulator.simulate()
    ranked_teams = sorted(simulator.teams(),
                          key=lambda t: t.points,
                          reverse=True)
    for t in ranked_teams:
        print('{:10s} {:3d}'.format(t.name, t.points))


if __name__ == "__main__":
    main()
