#!/usr/bin/env python

import argparse
import sys

import jsonpickle
from google.cloud import storage

from modules.fff.fetch import fetch_season


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--competition", required=True)
    parser.add_argument("--phase", required=True)
    parser.add_argument("--poule", required=True)
    args = parser.parse_args()

    # season = fetch_season(args.competition, args.phase, args.poule)

    # # for gameday in season:
    # #     print("------------------")
    # #     print(gameday)
    # #     for game in gameday:
    # #         print(game)

    # data = jsonpickle.encode(season)
    # new_season = jsonpickle.decode(data)

    # for gameday in new_season:
    #     print("------------------")
    #     print(gameday)
    #     for game in gameday:
    #         print(game)

    client = storage.Client()

    return 0


if __name__ == "__main__":
    sys.exit(main())
