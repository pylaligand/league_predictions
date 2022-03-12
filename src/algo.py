class RatedTeam(object):
    def __init__(self, name):
        self.name = name
        self.rating = -1
        self.points = 0

    def __str__(self):
        return '%s(%d, %d)' % (self.name, self.rating, self.points)

    def __repr__(self):
        return self.__str__()


class RatingEngine(object):
    def initialize(self, teams):
        raise Exception('Not implemented!')

    def update(self, team_1, team_2, game):
        raise Exception('Not implemented!')


class DumbRatingEngine(RatingEngine):
    def __init__(self, start, delta, min):
        super(RatingEngine, self).__init__()
        self.start = start
        self.delta = delta
        self.min = min

    def initialize(self, teams):
        for team in teams:
            team.rating = self.start

    def update(self, team_1, team_2, game):
        factor_1 = 1
        if game.played():
            if game.score_1 == game.score_2:
                return
            factor_1 = 1 if game.score_1 > game.score_2 else -1
        else:
            # Whoever has the highest rating wins if we don't have the score.
            if team_1.rating == team_2.rating:
                return
            factor_1 = 1 if team_1.rating > team_2.rating else -1
        team_1.rating = max(self.min, team_1.rating + factor_1 * self.delta)
        team_2.rating = max(self.min, team_2.rating - factor_1 * self.delta)


class GameSimulator(object):
    def __init__(self, season, engine):
        self._season = season
        self._teams = dict((t, RatedTeam(t)) for t in season.teams())
        self._engine = engine
        self._engine.initialize(self._teams.values())

    def simulate(self):
        for gameday in self._season.gamedays:
            self._simulate_gameday(gameday)

    def _simulate_gameday(self, gameday):
        for game in gameday.games:
            self._engine.update(self._teams[game.team_1],
                                self._teams[game.team_2], game)

    def get_team(self, name):
        return self._teams[name]

    def teams(self):
        return self._teams.values()
