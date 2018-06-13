import database

active_players = (database.load_all())

def query_player(name):
    for player in active_players:
        if player['user_id'] == name.replace('#',''):
            return(player)
        else: return False;
