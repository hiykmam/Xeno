import aiohttp

class DiscordCertificationManager:
    _instance = None
    def __new__(cls,client_id: str, client_secret: str, redirect_uri: str):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client_id = client_id
            cls._instance.client_secret = client_secret
            cls._instance.redirect_uri = redirect_uri
            cls._instance.base_url = "https://discord.com/api/v10"
            
        return cls._instance
    
    # def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
    #     self.client_id = client_id
    #     self.client_secret = client_secret
    #     self.redirect_uri = redirect_uri
    #     self.base_url = "https://discord.com/api/v10"

    async def get_user_profile(self, code: str) -> dict[str, str]:
        async with aiohttp.ClientSession() as session:
            token_data = await self._exchange_code(session, code)
            access_token = token_data.get("access_token")

            if not access_token:
                raise PermissionError("アクセストークンの取得に失敗しました。")

            raw_user = await self._fetch_raw_user(session, access_token)

            return {
                "user_id": raw_user.get("id"),
                "display_name": raw_user.get("global_name") or raw_user.get("username")
            }

    async def _exchange_code(self, session: aiohttp.ClientSession, code: str) -> dict[str, any]:
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': self.redirect_uri
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        
        async with session.post(f"{self.base_url}/oauth2/token", data=data, headers=headers) as resp:
            return await resp.json()

    async def _fetch_raw_user(self, session: aiohttp.ClientSession, token: str) -> dict[str, any]:
        headers = {"Authorization": f"Bearer {token}"}
        async with session.get(f"{self.base_url}/users/@me", headers=headers) as resp:
            if resp.status != 200:
                raise Exception(f"Discord API Error: {resp.status}")
            return await resp.json()