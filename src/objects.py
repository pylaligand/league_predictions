class Team(object):
    def __init__(self, name, rating):
        self.name = name
        self.rating = rating

    def __str__(self):
        return '%s@%s' % (self.name, self.rating)


class Game(object):
    def __init__(self, team_1, score_1, team_2, score_2):
        self.team_1 = team_1
        self.score_1 = score_1
        self.team_2 = team_2
        self.score_2 = score_2

    def played(self):
        return self.score_1 >= 0 and self.score_2 >= 0

    def __str__(self):
        if self.played():
            return '%s(%d) v %s(%d)' % (self.team_1, self.score_1, self.team_2,
                                        self.score_2)
        else:
            return '%s v %s' % (self.team_1, self.team_2)

    def __repr__(self):
        return self.__str__()


class Gameday(object):
    def __init__(self, name):
        self.name = name
        self.games = []

    def add_game(self, game):
        self.games.append(game)

    def __str__(self):
        return self.name


class Season(object):
    def __init__(self):
        self.gamedays = []

    def __iter__(self):
        return self.gamedays

    def __str__(self):
        return 'Season{%d}' % len(self.gamedays)

    def add_gameday(self, gameday):
        self.gamedays.append(gameday)
