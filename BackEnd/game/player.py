from __future__ import annotations
from typing import TYPE_CHECKING
from game.errors import *

if TYPE_CHECKING:
    from game.card import _CardBase
    from game.table import Table
    from game.table import Deck
    from game.communication import Communication

class Player():
    def __init__(self,name:str,id:int,comm:Communication):
        self._name = name
        self._discord_id = id
        self._sage_bool:bool = False
        self._shield_bool:bool = False
        self._right_card:_CardBase|None = None
        self._left_card:_CardBase|None = None
        self.comm:Communication = comm

    @property
    def id(self):
        return self._discord_id

    async def draw_card(self,deck:Deck,card:_CardBase|None=None):
        self.auto_swap()
        if self._left_card is None:
            if card is None:
                self._left_card = deck.draw()
            else:
                self._left_card = card
            self.comm.card_draw(self._left_card)
            return self._left_card
        else:
            raise CardNotFoundError()

    async def put_card(self,right:bool,opponent:Player,table:Table,deck:Deck):
        if right:
            tf = await self._right_card.card_process(self,opponent,table,deck)
            self._right_card = None
        else:
            tf = await self._left_card.card_process(self,opponent,table,deck)
            self._left_card = None
        if tf is None :
            raise CardActionError()
        await self.auto_swap()
        return tf

    @property
    def have_card(self):
        if self._left_card is not None  and self._right_card is None:
            return self._left_card
        elif self._right_card is not None and self._left_card is None:
            return self._right_card
        else:
            raise CardHaveOver()

    async def swap_card(self):
        self._right_card, self._left_card = self._left_card, self._right_card
        await self.comm.corr_swap()

    async def auto_swap(self):
        if self._left_card is not None and self._right_card is None:
            await self.swap_card()

