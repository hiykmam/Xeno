# keyの*opponent_*は、player_idの人、じゃないほうをさす。



# フロントエンドへの期待値
{ #市民2枚目の処刑に関するdict
    "type":"res_action1", #str
    "room_id":0, #int
    "player_id":"", #str
    "select_card":True, #bool 右がTrueで、左がFalse
}
{ #狩人の処刑に関するdict
    "type":"res_action2", #str
    "room_id":0, #int
    "player_id":"", #str
    "select_number":0 #int 1-10
}
{ #死神の選択に関するdict
    "type":"res_action5", #str
    "room_id":0, #int
    "player_id":"", #str
    "select_card":True #bool 右がTrueで、左がFalse
}
{ #賢者の選択に関するdict
    "type":"res_action7", #str
    "room_id":0, #int
    "player_id":"", #str
    "get_card":0, #int 1-10
}
{ #皇帝の処刑に関するdict
    "type":"res_action9", #str
    "room_id":0, #int
    "player_id":"", #str
    "select_card":True #bool 右がTrueで、左がFalse
}
{ #左右の入れ替えdict
    "type":"card_swap", #str
    "room_id":0, #int
    "player_id":"", #str
}
{ #カードの使用dict
    "type":"card_put", #str
    "room_id":0, #int
    "player_id":"", #str
    "put_card":True #bool 右がTrueで、左がFalse
}



#バックエンドからの送信値
{ #市民が出された時のdict  -> 2枚目は、backEnd的には、res_action1を待つ。
    "type":"put_action1", #str
    "room_id":0, #int
    "player_id":"", #str
    "second":False, #bool 出されたカードが1枚目か、2枚目か。
    "opponent_left_card":None, #int|None 1-10
    "opponent_right_card":None, #int|None 1-10
}
{ #市民が公開処刑を行った時の処理
    "type":"select_action1",
    "room_id":0, #int
    "player_id":"", #str
    "trash_card":0, #int 1-10
    "self_trash_card": [], #自分が捨てたカード
    "opponent_trash_card":[], #相手が捨てたカード
}
{ #狩人が出された時のdict -> backEnd的には、res_action2を待つ。
    "type":"put_action2", #str
    "room_id":0, #int
    "player_id":"", #str
}
{ #狩人が処刑を行った時の処理
    "type":"select_action2",
    "room_id":0, #int
    "player_id":"", #str
    "success":False, #bool
    "self_trash_card": [], #自分が捨てたカード
    "opponent_trash_card":[], #相手が捨てたカード
}

{ #占師が出された時のdict
    "type":"put_action3", #str
    "room_id":0, #int
    "player_id":"", #str
    "opponent_number":0, #int 1-10
    "self_trash_card": [], #自分が捨てたカード
    "opponent_trash_card":[], #相手が捨てたカード
}

{ #乙女が出された時のdict
    "type":"put_action4", #str
    "room_id":0, #int
    "player_id":"", #str
    "self_trash_card": [], #自分が捨てたカード
    "opponent_trash_card":[], #相手が捨てたカード
}
{ #乙女が出されて、次のターンの時のdict
    "type":"put_action4_next", #str
    "room_id":0, #int
    "player_id":"", #str
}
{ #死神が出された時のdict -> backEnd的には、res_aciton5を待つ
    "type":"put_action5", #str
    "room_id":0, #int
    "player_id":"", #str
}
{ #死神が除外を行った時の処理
    "type":"select_action1",
    "room_id":0, #int
    "player_id":"", #str
    "self_trash_card": [], #自分が捨てたカード
    "opponent_trash_card":[], #相手が捨てたカード
}
{ #貴族が出された時のdict
    "type":"put_action6", #str
    "room_id":0, #int
    "player_id":"", #str
    "second":False, #bool 出されたカードが1枚目か、2枚目か。
    "self_card":0, #int 1-10
    "opponent_card":0, #int 1-10
    "self_trash_card": [], #自分が捨てたカード
    "opponent_trash_card":[], #相手が捨てたカード
}
{ #賢者が出された時のdict
    "type":"put_action7", #str
    "room_id":0, #int
    "player_id":"", #str
    "self_trash_card": [], #自分が捨てたカード
    "opponent_trash_card":[], #相手が捨てたカード
}
{ #賢者が出されて、次のターンの時のdict
    "type":"put_action7_next", #str
    "room_id":0, #int
    "player_id":"", #str
    "first_card":0 ,#int 1-10
    "second_card":0 ,#int 1-10
    "third_card":0 ,#int 1-10
}
{ #精霊が出された時のdict
    "type":"put_action8", #str
    "room_id":0, #int
    "player_id":"", #str
    "get_card":0, #int 1-10
    "self_trash_card": [], #自分が捨てたカード
    "opponent_trash_card":[], #相手が捨てたカード
}
{ #皇帝が出された時のdict -> backEnd的には、res_aciton9を待つ
    "type":"put_action9", #str
    "room_id":0, #int
    "player_id":"", #str
}
{ #皇帝が公開処刑を行った時の処理
    "type":"select_action1",
    "room_id":0, #int
    "player_id":"", #str
    "trash_card":0, #int 1-10
    "self_trash_card": [], #自分が捨てたカード
    "opponent_trash_card":[], #相手が捨てたカード
}

{ #英雄が転生したときの通信
    "type":"reincarnation",
    "room_id":0, #int
    "player_id":"", #str 転生したプレイヤー
}


{
    "type":"card_draw",
    "room_id":0, #int
    "player_id":"", #str
    "draw_card":0 #int 1-10
}

{
    "type":"opponent_card_draw",
    "room_id":0, #int
    "player_id":"", #str
}

{
    "type":"opponent_card_put",
    "room_id":0, #int
    "player_id":"", #str
}


# corr_* レスポンスとして、受け取りましたよ。を返すとき。
{
    "type":"corr_swap",
    "room_id":0, #int
    "player_id":"", #str

}


#　judge_* は終了コードとしての意味も持つ。
{
    "type":"judge_win",
    "room_id":0,
    "player_id":"",
}

{
    "type":"judge_lose",
    "room_id":0,
    "player_id":"",
}

{
    "type":"judge_draw",
    "room_id":0,
    "player_id":"",
}