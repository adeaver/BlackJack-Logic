import json, sys

class GameControl():
    def __init__(self, players):
        self.GAMES = self.read_games()
        self.PLAYERS = players

    def read_games(self):
        try:
            f = open("games.json", "r")
            games = json.loads(f.read())
            f.close()
            return games
        except:
            return []

    def choose_game(self, name):
        for game in self.GAMES:
            if("name" in game.keys()):
                if(game["name"] == name):
                    return Game(game["deal"], game["hit"], game["hit_req"], game["hit_until"], self.PLAYERS)
        return None

class Game():
    def __init__(self, deal, hit, req, until, players):
        self.deal = deal
        self.hit = hit
        self.req = req
        self.until = until
        self.players = players

        if(self.deal == "divide"):
            self.deal = 52/self.players
    
    def get_deal_amount(self):
        return self.deal

    def get_hit_amount(self):
        return self.hit

    def get_num_players(self):
        return self.players

    def is_hit_required(self):
        return self.req

    def can_continue_to_hit(self):
        return self.until == "done"
                    
        
        

control = GameControl(4)
game = control.choose_game("blackjack")

if(game is not None):
    print "Game found"
