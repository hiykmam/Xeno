from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import json

if TYPE_CHECKING:
    from game.player import Player
    from game.table import Table
    from game.table import Deck


class _CardBase(ABC): #カード処理の基底クラス
    def __init__(self,num,name):
        self._num = num
        self._name = name

    @property
    def number(self): #自分の数字を返せるようにする。
        return self._num
    
    @property
    def name(self): #自分の名前を返せるようにする。
        return self._name

    @abstractmethod
    def card_process(self, owner:Player, opponent:Player, table:Table,deck:Deck) -> dict: #場に出された時の処理。
        pass


    def to_show_dict(self):
        return {
            "Number":self._num,
            "Name":self._name,
            "hidden":False
        }

class CardBack(_CardBase):
    def __init__(self):
        super().__init__(name="裏面",num=0)
    
    async def card_process(self, owner, opponent, table, deck):
        pass

class CardYouth(_CardBase): #少年 2枚目の登場で革命(9番と同じ効果)を起こす。(英雄公開された場合転生)
    def __init__(self):
        super().__init__(name="少年",num=1)

    async def card_process(self, owner, opponent, table, deck):
        if table.out_card_number_dict[1] == 2:
            opponent.draw_card(deck)

class CardSoldier(_CardBase): #兵士 相手の持っているカードを当てると倒すことが出来る(英雄が当てられた場合転生)
    def __init__(self):
        super().__init__(name="兵士",num=2)

    async def card_process(self, owner, opponent, table, deck):
        pass

class CardDiviner(_CardBase): #占師 相手の持っているカードを見ることが出来る。
    def __init__(self):
        super().__init__(name="占師",num=3)

    async def card_process(self, owner, opponent, table, deck):
        opponent._have_card
        return f"{opponent._name}さんが現在持っているカードは{opponent._have_card.number}/{opponent._have_card.name}です。"

class CardMaiden(_CardBase): #乙女 相手の効果を全て無効化する。
    def __init__(self):
        super().__init__(name="乙女",num=4)

    def card_process(self, owner, opponent, table, deck):
        return super().card_process(owner, opponent, table, deck)

class CardReaper(_CardBase): #死神 カードを一枚引かせ伏せたまま除外をする。(英雄除外で転生)
    def __init__(self):
        super().__init__(name="死神",num=5)

    def card_process(self, owner, opponent, table, deck):
        return super().card_process(owner, opponent, table, deck)

class CardNoble(_CardBase): #貴族 1枚目 お互いのカードを開示する。 2枚目 お互いの持っているカード決闘を行う。
    def __init__(self):
        super().__init__(name="貴族",num=6)

    def card_process(self, owner, opponent, table, deck):
        return super().card_process(owner, opponent, table, deck)

class CardSage(_CardBase): #賢者 カードを三枚引き、好きなカードを受け取る。 残り二枚を好きな順番で山札の上に置く
    def __init__(self):
        super().__init__(name="賢者",num=7)

    def card_process(self, owner, opponent, table, deck):
        return super().card_process(owner, opponent, table, deck)

class CardSpirit(_CardBase): #精霊 相手とカードを交換する。
    def __init__(self):
        super().__init__(name="精霊",num=8)

    def card_process(self, owner, opponent, table, deck):
        return super().card_process(owner, opponent, table, deck)

class CardEmperor(_CardBase): #貴族 相手にカードを引かせ、どちらも公開したうえで捨てるほうを決める。(相手が英雄を持っていた場合英雄は転生出来ない。)
    def __init__(self):
        super().__init__(name="皇帝",num=9)

    def card_process(self, owner, opponent, table, deck):
        return super().card_process(owner, opponent, table, deck)

class CardHero(_CardBase): #英雄 カードを場に出すことが出来ない。(皇帝以外で捨てられた場合転生を行う。)
    def __init__(self):
        super().__init__(name="英雄",num=10)

    def card_process(self, owner, opponent, table, deck):
        return super().card_process(owner, opponent, table, deck)