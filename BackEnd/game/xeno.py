from game.card import *
from game.player import Player
from game.deck import Deck
from game.table import Table
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.card import _CardBase

class Xeno:
    def __init__(self):
        self.table = Table()
        self.deck = Deck()
        self.player_one:Player = None
        self.player_two:Player = None


    def join_player(self,name,id):
        if self.player_one is None:
            self.player_one = Player(name,id)
        if self.player_two is None:
            self.player_two = Player()