import os 
import json

from dotenv import load_dotenv
from typing import TYPE_CHECKING
from sanic import Sanic, response, Request, Websocket

from util.webSoketManager import WebScketAllRoundManager as WSARM
from util.OAuth2Manager import DiscordCertificationManager as DCM



if TYPE_CHECKING:
    from game.card import _CardBase
    from game.table import Table
    from game.table import Deck

env = load_dotenv(".env")
ws_manager = WSARM()
oa_manager = DCM(
    client_id=os.getenv("DISCORD_CLIENT_ID"),
    client_secret=os.getenv("DISCORD_CLIENT_SECRET"),
    redirect_uri=os.getenv("DISCORD_REDIRECT_URI")
)
app = Sanic("XenoApp")

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
            pass

    except Exception:
        pass
    finally:
        # 接続が切れたら自動削除
        await ws_manager.remove_connection(room_id, user_id)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, dev=True)