from game_control import *
from game_machine import *
from serial_client import *

client = SerialClient()
machine = GameMachine(game, client)
machine.play_game()
