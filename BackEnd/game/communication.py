from BackEnd.game.player import Player
from BackEnd.game.table import Deck
from util.webSoketManager import WebScketAllRoundManager as WSARM
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.card import _CardBase
    from game.table import Table

class Communication:
    def __init__(self, room_id: int,player: Player,  table: Table, is_player_one: bool):
        self.wsarm = WSARM()
        self.room_id = room_id
        self.player = player
        self.table = table
        self.is_player_one = is_player_one

    async def send_webSocket(self, message):
        await self.wsarm.send(
            room_id=self.room_id, user_id=self.player.id, mess=message
        )

    async def card_info(self,deck:Deck,opp:Player):
        mess = {
            "type": "card_info",
            "room_id": self.room_id,  # int
            "player_id": self.player.id,  # str
            "player_name": self.player._name,  # str
            "opponent_user_id": opp.id, # str
            "opponent_user_name": opp._name, # str
            "card_info_list": deck.card_info_list,  # dict {HEX UUID : int}
            "back_card_id": self.table.back_card.id # HEX UUID
        }
        await self.send_webSocket(mess)
        return True

    async def put_action1(
        self, seccond: bool, opp_left: int | None, opp_right: int | None
    ): #少年が出されたときのdict -> backEnd的には、res_aciton1を待つ
        mess = {
            "type": "put_action1",
            "room_id": self.room_id,
            "player_id": self.player.id,  # str
            "second": seccond,  # bool 出されたカードが1枚目か、2枚目か。
            "opponent_left_card": opp_left,  # HEX UUID|None
            "opponent_right_card": opp_right,  # HEX UUID|None
        }
        await self.send_webSocket(mess)
        return True

    async def select_action1(self, trash_card: str): #少年が公開処刑を行った時の通信
        if not self.check_num(trash_card):
            return False
        self.update_trash_cards()
        mess = {  # 市民が公開処刑を行った時の処理
            "type": "select_action1",
            "room_id": self.room_id,  # int
            "player_id": self.player.id,  # str
            "trash_card": trash_card,  # HEX UUID 自分が捨てさせたカード
        }
        await self.send_webSocket(mess)
        return True

    async def select_action2(self, success):
        self.update_trash_cards()
        mess = {  # 狩人が処刑を行った時の処理
            "type": "select_action2",
            "room_id": self.room_id,  # int
            "player_id": self.player.id,  # str
            "success": success,  # bool
        }
        await self.send_webSocket(mess)
        return True

    async def put_action3(self, oppo_id: str):
        self.update_trash_cards()
        mess = {  # 占師が出された時のdict
            "type": "put_action3",  # str
            "room_id": self.room_id,  # int
            "player_id": self.player.id,  # str
            "opponent_id": oppo_id,  # hex UUID
        }
        await self.send_webSocket(mess)
        return True

    async def guard_action(self):
        mess = {  # 防がれた時に送る通信　1235689番のカードが出された時に、
            "type": "put_action4_next",  # str
            "room_id": self.room_id,  # int
            "player_id": self.player.id,  # str
        }
        await self.send_webSocket(mess)
        return True

    async def put_action5(self,back_card_id:str):
        mess = {  # 死神が出された時のdict -> backEnd的には、res_aciton5を待つ
            "type": "put_action5",  # str
            "room_id": self.room_id,  # int
            "player_id": self.player.id,  # str
            "opponent_left_card": back_card_id,  # HEX UUID|None
            "opponent_right_card": back_card_id,  # HEX UUID|None
        }
        await self.send_webSocket(mess)
        return True

    async def select_action5(self, trash_card: str):
        mess = {  # 死神が除外を行った時の処理
            "type": "select_action5",
            "room_id": self.room_id,  # int
            "player_id": self.player.id,  # str
            "trash_card": trash_card,  # HEX UUID 自分が捨てさせたカード
        }
        await self.send_webSocket(mess)
        return True

    async def put_action6(self, seccond: bool, oppo_card: str):
        mess = {  # 貴族が出された時のdict
            "type": "put_action6",  # str
            "room_id": self.room_id,  # int
            "player_id": self.player.id,  # str
            "second": seccond,  # bool 出されたカードが1枚目か、2枚目か。
            "opponent_id": oppo_card,  # HEX UUID
        }
        await self.send_webSocket(mess)
        return True

    async def three_draw_action(self, card1st: str, card2nd: str, card3th: str):
        mess = {  # 賢者が出されて、次のターンの時のdict
            "type": "put_action7_next",  # str
            "room_id": self.room_id,  # int
            "player_id": self.player.id,  # str
            "first_card": card1st,  # HEX UUID
            "second_card": card2nd,  # HEX UUID
            "third_card": card3th,  # HEX UUID
        }
        await self.send_webSocket(mess)
        return True

    async def put_action8(self, get_card: str):
        self.update_trash_cards()
        mess = {  # 精霊が出された時のdict
            "type": "put_action8",  # str
            "room_id": self.room_id,  # int
            "player_id": self.player.id,  # str
            "get_card": get_card,  # HEX UUID
        }
        await self.send_webSocket(mess)
        return True

    async def put_action9(self, opp_left: str | None, opp_right: str | None):
        if not self.check_num(opp_left, True):
            return False
        if not self.check_num(opp_right, True):
            return False
        mess = {  # 皇帝が出された時のdict -> backEnd的には、res_aciton9を待つ
            "type": "put_action9",  # str
            "room_id": self.room_id,  # int
            "player_id": self.player.id,  # str
            "opponent_left_card": opp_left,  # HEX UUID
            "opponent_right_card": opp_right,  # HEX UUID
        }
        await self.send_webSocket(mess)
        return True

    async def select_action9(self, trash_card: str):
        mess = {  # 皇帝が公開処刑を行った時の処理
            "type": "select_action9",
            "room_id": self.room_id,  # int
            "player_id": self.player.id,  # str
            "trash_card": trash_card,  # HEX UUID
        }
        await self.send_webSocket(mess)
        return True

    async def opp_reincarnation(self):
        mess = {  # 英雄が転生したときの通信
            "type": "opponent_reincarnation",
            "room_id": self.room_id,  # int
            "player_id": self.player.id,  # str
        }
        await self.send_webSocket(mess)
        return True

    async def reincarnation_draw(self, draw_card:str):
        mess = {  # 転生のドローの通信
            "type": "reincarnation_draw",
            "room_id": self.room_id,  # int
            "player_id": self.player.id,  # str
            "draw_card": draw_card,  # HEX UUID
        }
        await self.send_webSocket(mess)
        return True

    async def reincarnation_card_trash(self, trash_card: str):
        mess = {  # 転生時の手札除外
            "type": "reincarnation_card_trash",
            "room_id": self.room_id,  # int
            "player_id": self.player.id,  # str
            "trash_card": trash_card,  # HEX UUID
        }
        await self.send_webSocket(mess)
        return True

    async def card_draw(self, draw_card, is_guard: bool = False):
        if not self.check_num(draw_card):
            return False
        mess = {
            "type": "card_draw",
            "room_id": self.room_id,  # int
            "player_id": self.player.id,  # str
            "draw_card": draw_card,  # int 1-10
            "is_guard": is_guard  # bool
        }
        await self.send_webSocket(mess)
        return True

    async def opp_card_draw(
        self,three_pieces:bool=False,is_guard:bool=False
    ):
        mess = {
            "type": "opponent_card_draw",
            "room_id": self.room_id,  # int
            "player_id": self.player.id,  # str
            "is_three_pieces": three_pieces, #賢者の効果で3枚引いたときは、True
            "is_guard": is_guard  # bool
        }
        await self.send_webSocket(mess)
        return True

    async def opp_card_put(
        self,card_id:str
    ):
        mess = {
            "type": "opponent_card_put",
            "room_id": self.room_id,  # int
            "player_id": self.player.id,  # str
            "use_card_id": card_id # HEX UUID
        }
        await self.send_webSocket(mess)
        return True

    async def opp_swap(self,swap_count:int):
        mess = {
            "type": "opponent_swap",
            "room_id": self.room_id,  # int
            "player_id": self.player.id,  # str
            "swap_count": swap_count
        }
        await self.send_webSocket(mess)
        return True

    async def opp_card_select(self):
        mess = {
            "type": "opponent_card_select",
            "room_id": self.room_id,  # int
            "player_id": self.player.id,  # str
        }
        await self.send_webSocket(mess)
        return True

    async def judge_win(self):
        # 　judge_* は終了コードとしての意味も持つ。
        mess = {
            "type": "judge_win",
            "room_id": self.room_id,
            "player_id": self.player.id,
        }
        await self.send_webSocket(mess)
        return True

    async def judge_lose(self):
        mess = {
            "type": "judge_lose",
            "room_id": self.room_id,
            "player_id": self.player.id,
        }
        await self.send_webSocket(mess)
        return True

    async def judge_draw(self):
        mess = {
            "type": "judge_draw",
            "room_id": self.room_id,
            "player_id": self.player.id,
        }
        await self.send_webSocket(mess)
        return True
