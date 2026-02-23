from typing import TYPE_CHECKING
import random
from game.card import *

if TYPE_CHECKING:
    from game.card import _CardBase

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
        return self.deck.pop() if len(self.deck) > 0 else None
    
    def reincarnation_draw(self):
        res = self.reincarnation_card
        self.reincarnation_card = None
        return res
    
    @property
    def possible_sage_draw(self):
        return len(self.deck) >= 3


class Table():
    def __init__(self): #5で捨てられた場合は、out_card_listに0を、hidden_removal_cardに、本来の値を入れる。
        self._out_card_list_one:list[_CardBase] = [] #分ける必要はまだ見いだせてないけど、描画系の時に分けてると楽だと思う。
        self._out_card_list_two:list[_CardBase] = []
        self.hidden_removal_card:list[_CardBase] = [] #プレイヤーには見せない情報
    
    def out_card_number_lists(self,is_player_one:bool=True):
        one = [n.number for n in self._out_card_list_one]
        two = [n.number for n in self._out_card_list_two]
        if is_player_one:
            return one,two
        else:
            return two,one

    @property
    def out_card_list_all(self):
        res:list[_CardBase] = []
        res.extend(self._out_card_list_one)
        res.extend(self._out_card_list_two)
        return res
    
    @property
    def out_card_number_dict(self):
        res = {n: 0 for n in range(1, 11)}
        for card in self.out_card_list_all:
            res[card.number] += 1
        return res

