import asyncio
from ringIntegration import RingIntegration
from config import RING_USERNAME, RING_PASSWORD
import os

async def main():
    if not RING_USERNAME or not RING_PASSWORD:
        print("Please set the RING_USERNAME and RING_PASSWORD environment variables.")
        return

    ringIntegration = RingIntegration()
    try:
        await ringIntegration.authenticate(RING_USERNAME, RING_PASSWORD)

        doorbell = ringIntegration.getDevice(device="doorbots")
        chime = ringIntegration.getDevice(device="chimes")
        if doorbell and chime:
            print(f"Connected to doorbell: {doorbell.name}")
            print(f"Connected to chime: {chime.name}")
            events = await doorbell.async_history(kind='motion')
            print(events)
        else:
            print("No doorbell or chime found.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if ringIntegration.auth:
            await ringIntegration.auth.async_close()

if __name__ == "__main__":
    asyncio.run(main())
