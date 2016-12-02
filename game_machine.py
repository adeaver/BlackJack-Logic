from spi_client import SPIClient
from game_control import Game
import time

class GameMachine():

    def __init__(self, game, spi_client):
        self.TRANSITIONS = [[1, -1, -1, -1, -1], [-1, 0, -1, -1, -1], [-1, -1, 3, 1, -1], [-1, -1, -1, -1, 1], [-1, -1, -1, -1, -1]]
        #self.TRANSITIONS = [[1, -1, -1, -1, -1], [-1, 0, -1, -1, -1], [-1, -1, 4, -1, -1], [-1, -1, -1, -1, 1], [-1, -1, -1, -1, -1]] # for testing, this should just deal
        self.current_state = 2
        self.OUTPUT = [1, 2, 3, 5]
        self.INPUT = ["1", "2", "3", "4", "5"]
        self.n = game.get_num_players()
        self.round = game.get_num_players()
        self.dealt = 0
        self.game = game
        self.spi = spi_client
        self.current_output = 0

    def play_game(self):
        self.spi.write_state(0)

        while self.current_state != 4:
            if self.current_output != -1:
                if self.current_state == 0:
                    # deal cards
                    self.deal_cards()
                else:
                    # handle rotating, playing, and hitting
                    self.current_output = self.send_command()

                self.update_state()
                print "CURRENT STATE: " + str(self.current_state)
            else:
                self.current_output = self.spi.read_state()

        #self.spi.send_state("eeee") # end the game
        print "Game over!"

    def deal_cards(self):
        for i in range(0, self.game.get_deal_amount()):
            print "Dealing card"
            self.current_output = self.send_command()

        self.n -= 1 # decrement the amount of players left to deal to

    def send_command(self):
        time.sleep(.2)
        self.spi.write_state(self.OUTPUT[self.current_state])
        return self.spi.read_state()
        #self.current_output = self.OUTPUT[self.current_state]

    def update_state(self):
        if(self.current_state == 1):
            if self.n == 0:
                self.TRANSITIONS[1][1] = 2

        i = self.current_output-1
        print "i = " + str(i)	
        if i == -1:
            self.current_state = -1
        else:
            self.current_state = self.TRANSITIONS[self.current_state][i]

        if(self.current_state == 2):
            self.dealt += 1

            if(self.dealt == self.round):
                self.current_state == 4

    def get_index_for_output(self):
        for i in range(len(self.INPUT)):
            if(self.INPUT[i] in self.current_output):
                return i
        return -1
