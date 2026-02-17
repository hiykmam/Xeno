from __future__ import annotations
from abc import ABC, abstractmethod
from functools import partial
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.card import _CardBase
    from game.table import Table
    from game.deck import Deck

class Player():
    def __init__(self,name:str,id:int):
        self._name = name
        self._discord_id = id
        self._sage_bool:bool = False
        self._shield_bool:bool = False
        self._right_card:_CardBase|None = None
        self._left_card:_CardBase|None = None

    async def draw_card(self,deck:Deck):
        if self._left_card is not None and self._right_card is None:
            self.swap_card()
        if self._left_card is None:
            self._left_card = deck.draw()
        else:
            raise ValueError()
        
    async def out_card(self,left:bool,opponent:Player,table:Table,deck:Deck) -> dict:
        if left:
            return self._left_card.card_process(self,opponent,table,deck)
        else:
            return self._right_card.card_process(self,opponent,table,deck)

    def swap_card(self):
        n = self._right_card
        self._right_card = self._left_card
        self._left_card = n
