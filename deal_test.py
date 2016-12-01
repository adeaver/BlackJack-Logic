from game_control import *
from game_machine import *
from spi_client import *

client = SPIClient()
machine = GameMachine(game, client)
machine.play_game()
