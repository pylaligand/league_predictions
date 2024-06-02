import unittest

from algo import DumbRatingEngine, GameSimulator
from parsing import load_season


class TestAlgo(unittest.TestCase):
    def test_dumb_engine_one_gameday(self):
        data = [
            "day1,,,",
            "A,1,B,2",
        ]
        season = load_season(data, validate=False)
        engine = DumbRatingEngine(100, 10, 20)
        simulator = GameSimulator(season, engine)
        simulator.simulate()
        self.assertEqual(simulator.get_team("A").rating, 90)
        self.assertEqual(simulator.get_team("B").rating, 110)

    def test_dumb_engine_two_gamedays(self):
        data = [
            "day1,,,",
            "A,1,B,2",
            "day2,,,",
            "B,1,A,3",
        ]
        season = load_season(data, validate=False)
        engine = DumbRatingEngine(1000, 10, 20)
        simulator = GameSimulator(season, engine)
        simulator.simulate()
        self.assertEqual(simulator.get_team("A").rating, 1000)
        self.assertEqual(simulator.get_team("B").rating, 1000)

    def test_dumb_engine_min_rating(self):
        data = [
            "day1,,,",
            "A,1,B,2",
            "day2,,,",
            "B,3,A,1",
        ]
        season = load_season(data, validate=False)
        engine = DumbRatingEngine(60, 40, 10)
        simulator = GameSimulator(season, engine)
        simulator.simulate()
        self.assertEqual(simulator.get_team("A").rating, 10)
        self.assertEqual(simulator.get_team("B").rating, 140)

    def test_dumb_engine_anticipate(self):
        data = [
            "day1,,,",
            "A,1,B,2",
            "day2,,,",
            "B,,A,",
        ]
        season = load_season(data, validate=False)
        engine = DumbRatingEngine(100, 30, 0)
        simulator = GameSimulator(season, engine)
        simulator.simulate()
        self.assertEqual(simulator.get_team("A").rating, 40)
        self.assertEqual(simulator.get_team("B").rating, 160)
