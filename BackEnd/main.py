from typing import TYPE_CHECKING
from sanic import Sanic, response, Request, Websocket
from util.webSoketManager import WebScketAllRoundManager as WSARM

import json

if TYPE_CHECKING:
    from game.card import _CardBase
    from game.table import Table
    from game.deck import Deck

app = Sanic("XenoApp")
ws_manager = WSARM()

# プロキシ経由で届くリクエストを処理
@app.get("/api/status")
async def get_status(request):
    return response.json({
        "status": "online",
        "message": "Sanic backend is running!"
    })

@app.websocket("/api/webSoket")
async def get_websocet(request: Request, ws: Websocket):
    user_id = request.args.get("user_id")
    room_id = request.args.get("room_id")
    mode = request.args.get("mode", "player")

    # マネージャーに登録
    await ws_manager.add_connection(room_id, user_id, ws, mode)

    try:
        while True:
            raw_data = await ws.recv()
            data = json.loads(raw_data)

            # 例: 試合が決着した時
            if data.get("type") == "game_over" and mode == "player":
                # winner_idを受け取る想定
                winner_id = data.get("winner_id")
                
                # DB更新ロジック (Tortoise)
                # me = await user.get(user_id=user_id)
                # if user_id == winner_id: await me.win()
                # else: await me.lose()

                # 部屋の全員に結果を通知
                payload = {
                    "type": "result",
                    "winner": winner_id,
                    "new_rate": 1005, # me.rate
                    "rank": "霊峰"      # me.rank_class
                }
                await ws_manager.broadcast(room_id, payload)

    except Exception:
        pass
    finally:
        # 接続が切れたら自動削除
        await ws_manager.remove_connection(room_id, user_id)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, dev=True)