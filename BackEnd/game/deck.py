import random

from game.card import _CardBase
from game.card import *


class Deck():
    def __init__(self):
        self.deck:list[_CardBase] = []
        self.card_add_deck()
        self.shuffle()
        self.reincarnation_card = self.deck.pop()
    
    def card_add_deck(self):
        self._sub_card_add_deck()
        self._sub_card_add_deck()
        self.deck.append(CardEmperor()) #山札に1枚だけのカード
        self.deck.append(CardHero()) #山札に1枚だけのカード

    def _sub_card_add_deck(self): #山札に二枚入るカードを入れる。
        self.deck.append(CardYouth())
        self.deck.append(CardSoldier())
        self.deck.append(CardDiviner())
        self.deck.append(CardMaiden())
        self.deck.append(CardReaper())
        self.deck.append(CardNoble())
        self.deck.append(CardSage())
        self.deck.append(CardSpirit())

    def shuffle(self):
        random.shuffle(self.deck)

    def draw(self):
        return self.deck.pop() if self.deck else None
    
    def reincarnation_draw(self):
        res = self.reincarnation_card
        self.reincarnation_card = None
        return res
