import unittest

from parsing import load_season


class TestParsing(unittest.TestCase):
    def assertGame(self, game, team_1, score_1, team_2, score_2):
        self.assertTrue(game.played())
        self.assertEqual(game.team_1, team_1)
        self.assertEqual(game.score_1, score_1)
        self.assertEqual(game.team_2, team_2)
        self.assertEqual(game.score_2, score_2)

    def test_parse_one(self):
        data = [
            "day1,,,",
            "A,1,B,2",
            "C,3,D,4",
            "E,0,F,0",
        ]
        season = load_season(data, validate=False)
        self.assertEqual(len(season.gamedays), 1)
        self.assertEqual(len(season.gamedays[0].games), 3)
        self.assertGame(season.gamedays[0].games[0], "A", 1, "B", 2)
        self.assertGame(season.gamedays[0].games[1], "C", 3, "D", 4)
        self.assertGame(season.gamedays[0].games[2], "E", 0, "F", 0)

    def test_parse_two(self):
        data = [
            "day1,,,",
            "A,1,B,2",
            "C,3,D,4",
            "day2,,,",
            "B,1,C,2",
            "D,3,A,4",
        ]
        season = load_season(data, validate=False)
        self.assertEqual(len(season.gamedays), 2)
        self.assertEqual(len(season.gamedays[0].games), 2)
        self.assertGame(season.gamedays[0].games[0], "A", 1, "B", 2)
        self.assertGame(season.gamedays[0].games[1], "C", 3, "D", 4)
        self.assertEqual(len(season.gamedays[1].games), 2)
        self.assertGame(season.gamedays[1].games[0], "B", 1, "C", 2)
        self.assertGame(season.gamedays[1].games[1], "D", 3, "A", 4)

    def test_parse_comma(self):
        data = [
            "day1,,,",
            "A,1,B,2",
            ",,,",
            "day2,,,",
            "B,1,A,1",
        ]
        season = load_season(data, validate=False)
        self.assertEqual(len(season.gamedays), 2)
        self.assertEqual(len(season.gamedays[0].games), 1)
        self.assertGame(season.gamedays[0].games[0], "A", 1, "B", 2)
        self.assertEqual(len(season.gamedays[1].games), 1)
        self.assertGame(season.gamedays[1].games[0], "B", 1, "A", 1)

    def test_parse_no_scores(self):
        data = [
            "day1,,,",
            "A,,B,",
            "C,,D,",
            "E,,F,",
        ]
        season = load_season(data, validate=False)
        self.assertEqual(len(season.gamedays), 1)
        self.assertEqual(len(season.gamedays[0].games), 3)
        for game in season.gamedays[0].games:
            self.assertFalse(game.played())

    def test_validate(self):
        data = [
            "day1,,,",
            "A,1,B,1",
            "day2,,,",
            "B,2,A,1",
        ]
        season = load_season(data)
