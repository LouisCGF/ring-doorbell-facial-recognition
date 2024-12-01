import asyncio
import json
from pathlib import Path
from ring_doorbell import Auth, Ring, AuthenticationError, Requires2FAError

async def otpCallback():
    return input("2FA code: ")

class RingIntegration:
    def __init__(self, user_agent="RingIntegration-1.0"):
        self.user_agent = user_agent
        self.cache_file = Path(self.user_agent + ".token.cache")
        self.auth = None
        self.ring = None

    def token_updated(self, token):
        self.cache_file.write_text(json.dumps(token)) # <- Save the updated token to the cache.

    async def authenticate(self, username, password):
        # Authenticate with the Ring API, handling 2FA if enabled.
        if self.cache_file.is_file():
            self.auth = Auth(self.user_agent, json.loads(self.cache_file.read_text()), self.token_updated) # <- Use cached token
            self.ring = Ring(self.auth)
            try:
                await self.ring.async_create_session()
            except AuthenticationError:
                await self.__do_auth(username, password)
        else:
            await self.__do_auth(username, password)

        await self.ring.async_update_data()

    async def __do_auth(self, username, password):
        self.auth = Auth(self.user_agent, None, self.token_updated)
        try:
            await self.auth.async_fetch_token(username, password)
        except Requires2FAError:
            await self.auth.async_fetch_token(username, password, await otpCallback())
        self.ring = Ring(self.auth)

    def __getDevices(self):
        return self.ring.devices()

    def getDevice(self, device):
        devices = self.__getDevices()
        return devices[f"{device}"][0] if f"{device}" in devices and devices[f"{device}"] else None
