import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://user:ZHNhZGFkYWRhc2Rh@localhost:27017/?authSource=admin",
)
MONGO_DATABASE = os.getenv("MONGO_DATABASE", "library")
