import json
import asyncio

class WebScketAllRoundManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            #部屋の情報 {room_id:{"players":{user_id:ws},"audiences":{user_id:ws}}}
            cls._instance.rooms = {}
            cls._instance.lock = asyncio.Lock()
        return cls._instance
    
    # def __init__(self): #入力支援用の記述終わったらコメントアウトする。
    #     self.rooms = {}
    #     self.lock = asyncio.Lock()

    def check_num_room_id(self,room_id:int):
        if 1000000 <= room_id or room_id <= 99999:
            return True
        return False

    def check_collision_room_id(self,room_id:int):
        if room_id in self.rooms.keys():
            return True
        return False

    async def add_connection(self, room_id:int,user_id,ws,GameSystem,mode="player"):
        if self.check_num_room_id(room_id):
            print(f"[WS] Error: Invalid Room ID {room_id}")
            return False
        async with self.lock:
            if room_id not in self.rooms:
                self.rooms[room_id] = {"players":{},"audiences":{},"GameSystem":GameSystem} #念のため観戦者のIDも保存する。
            if mode == "player":
                if len(self.rooms[room_id]["players"]) < 2:
                    self.rooms[room_id]["players"][user_id] = ws
                    print(f"[WS] Player AddConnection {user_id} joined Room {room_id}")
                    return True
                else:
                    mode = "audiences"
            if mode != "player":
                self.rooms[room_id]["audiences"][user_id] = ws
                print(f"[WS] Audiences AddConnection {user_id} joined Room {room_id}")
                return True

    async def broadcast(self,room_id,payload):
        if room_id not in self.rooms:
            return
        message = json.dumps(payload)
        room = self.rooms[room_id]

        all_client = list(room["players"].values()) + list(room["audiences"].values())
        if not all_client:
            del self.rooms[room_id]
            return
        
        await asyncio.gather(
            *[self._safe_send(ws,message) for ws in all_client]
        )
    
    async def _safe_send(self,ws, message):
        try:
            await ws.send(message)
        except Exception:
            pass

    async def send(self,room_id,user_id,mess:dict):
        room = self.rooms.get(room_id,None)
        if room is None:return
        ws = room["players"][user_id] or room["audiences"][user_id]
        if ws:
            message = json.dumps(mess)
            await self._safe_send(ws,message)

    async def remove_connection(self,room_id,user_id):
        async with self.lock:
            if room_id in self.rooms:
                if user_id in self.rooms[room_id]["players"]:
                    del self.rooms[room_id]["players"][user_id]
                    print(f"[WS] Player RemoveConnection {user_id} logout Room {room_id}")
                
                if user_id in self.rooms[room_id]["audiences"]:
                    del self.rooms[room_id]["audiences"][user_id]
                    print(f"[WS] audience RemoveConnection {user_id} logout Room {room_id}")

                if not self.rooms[room_id]["players"] and not self.rooms[room_id]["audiences"]:
                    del self.rooms[room_id]
                    print(f"[WS] Room {room_id} deleted (empty)")