import unittest

from algo import GameSimulator
from elo import EloEngine
from parsing import load_season


class TestElgo(unittest.TestCase):
    def test_one_gameday(self):
        data = [
            "day1,,,",
            "A,1,B,2",
        ]
        season = load_season(data, validate=False)
        engine = EloEngine(start=1000, k=20, min=100)
        simulator = GameSimulator(season, engine)
        simulator.simulate()
        self.assertEqual(simulator.get_team("A").rating, 990)
        self.assertEqual(simulator.get_team("B").rating, 1010)

    def test_two_gamedays(self):
        data = [
            "day1,,,",
            "A,1,B,2",
            "day2,,,",
            "B,3,A,1",
        ]
        season = load_season(data, validate=False)
        engine = EloEngine(start=1000, k=20, min=100)
        simulator = GameSimulator(season, engine)
        simulator.simulate()
        self.assertEqual(simulator.get_team("A").rating, 980)
        self.assertEqual(simulator.get_team("B").rating, 1019)

    def test_three_gamedays(self):
        data = [
            "day1,,,",
            "A,1,B,2",
            "day2,,,",
            "B,3,A,1",
            "day3,,,",
            "A,4,B,0",
        ]
        season = load_season(data, validate=False)
        engine = EloEngine(start=1000, k=20, min=100)
        simulator = GameSimulator(season, engine)
        simulator.simulate()
        self.assertEqual(simulator.get_team("A").rating, 991)
        self.assertEqual(simulator.get_team("B").rating, 1007)
