from ring_doorbell import Ring, Auth
from oauthlib.oauth2 import MissingTokenError

class RingIntegration:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.auth = Auth("Ring-Integration/1.0", None)
        self.ring = None

    def authenticate(self):
        try:
            self.auth.fetch_token(self.username, self.password)
            self.ring = Ring(self.auth)
            if self.ring.is_connected:
                print("Successfully connected to Ring!")
        except MissingTokenError as e:
            print(f"Authentication failed: {e}")

    def getDoorbell(self):
        if self.ring:
            devices = self.ring.devices()
            return devices["doorbots"][0] if devices["doorbots"] else None
        return None
