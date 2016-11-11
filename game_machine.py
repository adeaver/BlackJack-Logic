from serial_client import SerialClient
from game_control import Game

class GameMachine():

    def __init__(self, game, serial_client):
        #self.TRANSITIONS = [[1, -1, -1, -1, -1], [-1, 0, -1, -1, -1], [-1, -1, 3, 1, -1], [-1, -1, -1, -1, 1]]
        self.TRANSITIONS = [[1, -1, -1, -1, -1], [-1, 0, -1, -1, -1], [-1, -1, -1, -1, -1], [-1, -1, -1, -1, 1]] # for testing, this should just deal
        self.current_state = 0
        self.current_input = "1111"
        self.OUTPUT = ["1111", "2222", "3333", "5555"]
        self.INPUT = ["1", "2", "3", "4", "5"]
        self.n = game.get_num_players()
        self.game = game
        self.serial = serial_client

    def play_game(self):
        while self.current_state != -1:
            if self.current_state == 0:
                # deal cards
                self.deal_cards()
            else:
                # handle rotating, playing, and hitting
                self.send_command()

            self.update_state()
            print self.current_state

        self.serial.send_state("eeee") # end the game
        print "Game over!"

    def deal_cards(self):
        for i in range(0, self.game.get_deal_amount()):
            self.send_command()

        self.n -= 1 # decrement the amount of players left to deal to

    def send_command(self):
        self.serial.send_state(self.OUTPUT[self.current_state])
        self.current_output = self.serial.receive_state()
        #self.current_output = self.OUTPUT[self.current_state]

    def update_state(self):
        if(self.current_state == 1):
            if self.n == 0:
                self.TRANSITIONS[1][1] = 2

        i = self.get_index_for_output()

        if i == -1:
            self.current_state = -1
        else:
            self.current_state = self.TRANSITIONS[self.current_state][i]

    def get_index_for_output(self):
        for i in range(len(self.INPUT)):
            if(self.INPUT[i] in self.current_output):
                return i
        return -1