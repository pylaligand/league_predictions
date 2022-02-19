class Team(object):
    def __init__(self, name, rating):
        self.name = name
        self.rating = rating

    def __str__(self):
        return '%s@%s' % (self.name, self.rating)


class Game(object):
    def __init__(self, player_1, player_2, score_1, score_2):
        self.player_1 = player_1
        self.player_2 = player_2
        self.score_1 = score_1
        self.score_2 = score_2


class Gameday(object):
    def __init__(self, games):
        self.games = games
