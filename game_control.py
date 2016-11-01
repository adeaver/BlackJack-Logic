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

        self.dealt = 0
        self.hitting = 0

        if(self.deal == "divide"):
            self.deal = 52/self.players
    
    def deal_cards(self):
        # THIS SHOULD SEND TO ARDUINO
        self.dealt += 1
        return self.deal

    def hit_player(self):
        hit_again = True

        while hit_again:
            if(self.req):
                # THIS SHOULD SEND TO ARDUINO
                pass
            else:
                # WAIT FOR INPUT
                pass
            
            if(self.until == "dealt"):
                hit_again = False
            else:
                # WAIT FOR INPUT
                hit_again = False # Should be true or false
    
        self.hitting = (self.hitting+1)%self.players
        return
                    
        
        

control = GameControl(4)
game = control.choose_game("blackjack")

if(game is not None):
    print "Game found"
