from __future__ import division

import math
import random

from algo import RatingEngine


class EloEngine(RatingEngine):
    def __init__(self, start, k, min):
        super(RatingEngine, self).__init__()
        self.start = start
        self.k = k
        self.min = min

    def initialize(self, teams):
        for team in teams:
            team.rating = self.start

    def update(self, team_1, team_2, game):
        expectation_1 = 1 / (math.pow(10,
                                      (team_2.rating - team_1.rating) / 400) +
                             1)
        if game.played():
            if game.score_1 == game.score_2:
                result_1 = 0.5
                result_2 = 0.5
            elif game.score_1 > game.score_2:
                result_1 = 1
                result_2 = 0
            else:
                result_1 = 0
                result_2 = 1
        else:
            score = random.random()
            if score <= expectation_1:
                result_1 = 1
                result_2 = 0
            else:
                result_1 = 0
                result_2 = 1
        team_1.rating = math.trunc(team_1.rating + self.k *
                                   (result_1 - expectation_1))
        team_2.rating = math.trunc(team_2.rating + self.k *
                                   (result_2 - (1 - expectation_1)))
        team_1.points = team_1.points + (1 if result_1 == 0.5 else result_1 *
                                         3)
        team_2.points = team_2.points + (1 if result_2 == 0.5 else result_2 *
                                         3)
