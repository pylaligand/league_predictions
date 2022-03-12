import csv

from objects import Game, Gameday, Season, Team


def _get_teams(gameday):
    result = set()
    for game in gameday.games:
        result.add(game.team_1)
        result.add(game.team_2)
    return result


def _check_team(team, all_teams, games):
    other_teams = all_teams - {team}
    home_opponents = [g.team_2 for g in games if g.team_1 == team]
    return len(home_opponents) == len(other_teams) and set(
        t for t in home_opponents) == other_teams


def _validate(season):
    if not season.gamedays:
        return
    teams = _get_teams(season.gamedays[0])
    # Each team plays the right number of games.
    if len(season.gamedays) != 2 * (len(teams) - 1):
        raise Exception('Season has incorrect duration')
    # Each game day features each team exactly once.
    for gameday in season.gamedays[1:]:
        if _get_teams(gameday) != teams:
            raise Exception('Gameday %s has wrong teams' % gameday)
    # Each team plays each other team twice, once at home and once away.
    all_games = [g for gd in season.gamedays for g in gd.games]
    for team in teams:
        _check_team(team, teams, all_games)
    return season


def load_season(data, validate=True):
    result = Season()
    current_gameday = 0
    for row in csv.reader(data):
        if not row[0]:
            continue
        if row[0].startswith('day'):
            if current_gameday:
                result.add_gameday(current_gameday)
            current_gameday = Gameday(row[0])
            continue
        try:
            game = Game(row[0], int(row[1]), row[2], int(row[3]))
        except:
            game = Game(row[0], -1, row[2], -1)
        current_gameday.add_game(game)
    if current_gameday:
        result.add_gameday(current_gameday)
    return _validate(result) if validate else result
