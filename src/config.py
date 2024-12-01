from dotenv import load_dotenv
import os

load_dotenv()

RING_USERNAME = os.getenv("RING_USERNAME")
RING_PASSWORD = os.getenv("RING_PASSWORD")
KNOWN_FACES_DIR = "data/faces/"
LOG_DIR = "data/logs/"
