import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    config = {
        "mongo_uri": os.getenv("MONGO_URI", "mongodb://localhost:27017/"),
        "port": int(os.getenv("PORT", 5000))
    }
    if not config["mongo_uri"]:
        raise ValueError("MONGO_URI is required but not set in environment variables")
    return config

def validate_input(week, transport, energy):
    if not all(isinstance(x, (int, float)) for x in [week, transport, energy]):
        raise TypeError("All inputs must be numeric")
    return week > 0 and transport >= 0 and energy >= 0