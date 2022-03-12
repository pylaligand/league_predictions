#!/usr/bin/python

import argparse

from parsing import load_season


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    args = parser.parse_args()

    with open(args.file, 'r') as input_file:
        lines = [l.strip() for l in input_file.readlines()]

    season = load_season(lines)
    print(season)


if __name__ == "__main__":
    main()
