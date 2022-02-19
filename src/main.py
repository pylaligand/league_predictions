#!/usr/bin/python

import argparse

from parsing import parse_gamedays


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('file')
    args = parser.parse_args()

    with open(args.file, 'r') as input_file:
        lines = [l.strip() for l in input_file.readlines()]

    gamedays = parse_gamedays(lines)
    print(gamedays)


if __name__ == "__main__":
    main()
