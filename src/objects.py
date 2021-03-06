class Team(object):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __eq__(self, other):
        return self.name == other.name

    def __hash__(self):
        return hash((self.name))


class Game(object):
    def __init__(self, team_1, score_1, team_2, score_2):
        self.team_1 = team_1
        self.score_1 = score_1
        self.team_2 = team_2
        self.score_2 = score_2

    def played(self):
        return self.score_1 >= 0 and self.score_2 >= 0

    def update_scores(self, other):
        self.score_1 = other.score_1
        self.score_2 = other.score_2

    def __eq__(self, other):
        return self.team_1 == other.team_1 and self.team_2 == other.team_2

    def __hash__(self):
        return hash((self.team_1, self.team_2))

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

    def teams(self):
        result = {}
        for g in self.gamedays[0].games:
            result[g.team_1] = Team(g.team_1)
            result[g.team_2] = Team(g.team_2)
        return result
