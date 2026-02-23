from util.webSoketManager import WebScketAllRoundManager as WSARM
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game.card import _CardBase
    from game.table import Table


class Communication:
    def __init__(self, room_id: int, player_id: str, table: Table, is_player_one: bool):
        if self.check_ids(room_id, player_id):
            raise ValueError()
        self.wsarm = WSARM()
        self.room_id = room_id
        self.player_id = player_id
        self.table = table
        self.is_player_one = is_player_one
        self.update_trash_cards()

    def update_trash_cards(self):
        self.self_trash_cards, self.oppo_trash_cards = self.table.out_card_number_lists(
            is_player_one=self.is_player_one
        )

    def check_num(self, card, permission_none: bool = False) -> bool:
        if card is None and permission_none:
            return True
        if isinstance(card, int) and 1 <= card <= 10:
            return True
        else:
            return False

    def check_ids(self, room_id, player_id) -> bool:
        if (
            isinstance(room_id, int)
            and self.wsarm.check_collision(room_id)
            and isinstance(player_id, str)
        ):
            return True
        else:
            return False

    async def send_webSocket(self, message):
        await self.wsarm.send(
            room_id=self.room_id, user_id=self.player_id, mess=message
        )

    async def put_action1(
        self, seccond: bool, opp_left: int | None, opp_right: int | None
    ):
        mess = {
            "type": "put_action1",
            "room_id": self.room_id,
            "player_id": self.player_id,  # str
            "second": seccond,  # bool 出されたカードが1枚目か、2枚目か。
            "opponent_left_card": opp_left,  # int|None 1-10
            "opponent_right_card": opp_right,  # int|None 1-10
        }
        await self.send_webSocket(mess)
        return True

    async def select_action1(self, trash_card: int):
        if not self.check_num(trash_card):
            return False
        self.update_trash_cards()
        mess = {  # 市民が公開処刑を行った時の処理
            "type": "select_action1",
            "room_id": self.room_id,  # int
            "player_id": self.player_id,  # str
            "trash_card": trash_card,  # int 1-10
            "self_trash_card": self.self_trash_cards,  # 自分が捨てたカード
            "opponent_trash_card": self.oppo_trash_cards,  # 相手が捨てたカード
        }
        await self.send_webSocket(mess)
        return True

    async def put_action2(self):
        mess = {  # 狩人が出された時のdict -> backEnd的には、res_action2を待つ。
            "type": "put_action2",  # str
            "room_id": self.room_id,  # int
            "player_id": self.player_id,  # str
        }
        await self.send_webSocket(mess)
        return True

    async def select_action2(self, success):
        self.update_trash_cards()
        mess = {  # 狩人が処刑を行った時の処理
            "type": "select_action2",
            "room_id": self.room_id,  # int
            "player_id": self.player_id,  # str
            "success": success,  # bool
            "self_trash_card": self.self_trash_cards,  # 自分が捨てたカード
            "opponent_trash_card": self.oppo_trash_cards,  # 相手が捨てたカード
        }
        await self.send_webSocket(mess)
        return True

    async def put_action3(self, oppo_num: int):
        if not self.check_num(oppo_num):
            return False
        self.update_trash_cards()
        mess = {  # 占師が出された時のdict
            "type": "put_action3",  # str
            "room_id": self.room_id,  # int
            "player_id": self.player_id,  # str
            "opponent_number": oppo_num,  # int 1-10
            "self_trash_card": self.self_trash_cards,  # 自分が捨てたカード
            "opponent_trash_card": self.oppo_trash_cards,  # 相手が捨てたカード
        }
        await self.send_webSocket(mess)
        return True

    async def put_action4(self):
        self.update_trash_cards()
        mess = {  # 乙女が出された時のdict
            "type": "put_action4",  # str
            "room_id": self.room_id,  # int
            "player_id": self.player_id,  # str
            "self_trash_card": self.self_trash_cards,  # 自分が捨てたカード
            "opponent_trash_card": self.oppo_trash_cards,  # 相手が捨てたカード
        }
        await self.send_webSocket(mess)
        return True

    async def next_action4(self):
        mess = {  # 乙女が出されて、次のターンの時のdict
            "type": "put_action4_next",  # str
            "room_id": self.room_id,  # int
            "player_id": self.player_id,  # str
        }
        await self.send_webSocket(mess)
        return True

    async def put_action5(self):
        mess = {  # 死神が出された時のdict -> backEnd的には、res_aciton5を待つ
            "type": "put_action5",  # str
            "room_id": self.room_id,  # int
            "player_id": self.player_id,  # str
        }
        await self.send_webSocket(mess)
        return True

    async def select_action5(self):
        self.update_trash_cards()
        mess = {  # 死神が除外を行った時の処理
            "type": "select_action5",
            "room_id": self.room_id,  # int
            "player_id": self.player_id,  # str
            "self_trash_card": self.self_trash_cards,  # 自分が捨てたカード
            "opponent_trash_card": self.oppo_trash_cards,  # 相手が捨てたカード
        }
        await self.send_webSocket(mess)
        return True

    async def put_action6(self, seccond: bool, self_card: int, oppo_card: int):
        if not self.check_num(self_card):
            return False
        if not self.check_num(oppo_card):
            return False
        self.update_trash_cards()
        mess = {  # 貴族が出された時のdict
            "type": "put_action6",  # str
            "room_id": self.room_id,  # int
            "player_id": self.player_id,  # str
            "second": seccond,  # bool 出されたカードが1枚目か、2枚目か。
            "self_card": self_card,  # int 1-10
            "opponent_card": oppo_card,  # int 1-10
            "self_trash_card": self.self_trash_cards,  # 自分が捨てたカード
            "opponent_trash_card": self.oppo_trash_cards,  # 相手が捨てたカード
        }
        await self.send_webSocket(mess)
        return True

    async def put_action7(self):
        self.update_trash_cards()
        mess = {  # 賢者が出された時のdict
            "type": "put_action7",  # str
            "room_id": self.room_id,  # int
            "player_id": self.player_id,  # str
            "self_trash_card": self.self_trash_cards,  # 自分が捨てたカード
            "opponent_trash_card": self.oppo_trash_cards,  # 相手が捨てたカード
        }
        await self.send_webSocket(mess)
        return True

    async def next_action7(self, card1st: int, card2nd: int, card3th: int):
        if not self.check_num(card1st):
            return False
        if not self.check_num(card2nd):
            return False
        if not self.check_num(card3th):
            return False
        mess = {  # 賢者が出されて、次のターンの時のdict
            "type": "put_action7_next",  # str
            "room_id": self.room_id,  # int
            "player_id": self.player_id,  # str
            "first_card": card1st,  # int 1-10
            "second_card": card2nd,  # int 1-10
            "third_card": card3th,  # int 1-10
        }
        await self.send_webSocket(mess)
        return True

    async def put_action8(self, get_card: int):
        if not self.check_num(get_card):
            return False
        self.update_trash_cards()
        mess = {  # 精霊が出された時のdict
            "type": "put_action8",  # str
            "room_id": self.room_id,  # int
            "player_id": self.player_id,  # str
            "get_card": get_card,  # int 1-10
            "self_trash_card": self.self_trash_cards,  # 自分が捨てたカード
            "opponent_trash_card": self.oppo_trash_cards,  # 相手が捨てたカード
        }
        await self.send_webSocket(mess)
        return True

    async def put_action9(self, opp_left: int | None, opp_right: int | None):
        if not self.check_num(opp_left, True):
            return False
        if not self.check_num(opp_right, True):
            return False
        mess = {  # 皇帝が出された時のdict -> backEnd的には、res_aciton9を待つ
            "type": "put_action9",  # str
            "room_id": self.room_id,  # int
            "player_id": self.player_id,  # str
            "opponent_left_card": opp_left,  # int|None 1-10
            "opponent_right_card": opp_right,  # int|None 1-10
        }
        await self.send_webSocket(mess)
        return True

    async def select_action9(self, trash_card: int):
        if not self.check_num(trash_card):
            return False
        self.update_trash_cards()
        mess = {  # 皇帝が公開処刑を行った時の処理
            "type": "select_action9",
            "room_id": self.room_id,  # int
            "player_id": self.player_id,  # str
            "trash_card": trash_card,  # int 1-10
            "self_trash_card": self.self_trash_cards,  # 自分が捨てたカード
            "opponent_trash_card": self.oppo_trash_cards,  # 相手が捨てたカード
        }
        await self.send_webSocket(mess)
        return True

    async def reincarnation(self, reincariton_player):
        mess = {  # 英雄が転生したときの通信
            "type": "reincarnation",
            "room_id": self.room_id,  # int
            "player_id": reincariton_player,  # str 転生したプレイヤー
        }
        await self.send_webSocket(mess)
        return True

    async def card_draw(self, draw_card):
        if not self.check_num(draw_card):
            return False
        mess = {
            "type": "card_draw",
            "room_id": self.room_id,  # int
            "player_id": self.player_id,  # str
            "draw_card": draw_card,  # int 1-10
        }
        await self.send_webSocket(mess)
        return True

    async def opp_card_draw(
        self,
    ):
        mess = {
            "type": "opponent_card_draw",
            "room_id": self.room_id,  # int
            "player_id": self.player_id,  # str
        }
        await self.send_webSocket(mess)
        return True

    async def opp_card_put(
        self,
    ):
        mess = {
            "type": "opponent_card_put",
            "room_id": self.room_id,  # int
            "player_id": self.player_id,  # str
        }
        await self.send_webSocket(mess)
        return True

    async def corr_swap(self):
        # corr_* レスポンスとして、受け取りましたよ。を返すとき。
        mess = {
            "type": "corr_swap",
            "room_id": self.room_id,  # int
            "player_id": self.player_id,  # str
        }
        await self.send_webSocket(mess)
        return True

    async def judge_win(self):
        # 　judge_* は終了コードとしての意味も持つ。
        mess = {
            "type": "judge_win",
            "room_id": self.room_id,
            "player_id": self.player_id,
        }
        await self.send_webSocket(mess)
        return True

    async def judge_lose(self):
        mess = {
            "type": "judge_lose",
            "room_id": self.room_id,
            "player_id": self.player_id,
        }
        await self.send_webSocket(mess)
        return True

    async def judge_draw(self):
        mess = {
            "type": "judge_draw",
            "room_id": self.room_id,
            "player_id": self.player_id,
        }
        await self.send_webSocket(mess)
        return True
