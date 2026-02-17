from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.card import _CardBase

class Table():
    def __init__(self):
        self._out_card_list_one:list[_CardBase] = [] #分ける必要はまだ見いだせてないけど、描画系の時に分けてると楽だと思う。
        self._out_card_list_two:list[_CardBase] = []
        self.hidden_removal_card:list[_CardBase] = [] #プレイヤーには見せない情報
    
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

