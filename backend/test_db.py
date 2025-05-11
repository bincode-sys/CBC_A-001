from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")

def insert_entry(entry):
    if not isinstance(entry, dict) or "week" not in entry or "college" not in entry:
        raise ValueError("Entry must be a dictionary with 'week' and 'college' fields")

    client = MongoClient(MONGO_URI)
    try:
        db = client["carbon"]
        collection = db["footprints"]
        collection.update_one(
            {"week": entry["week"], "college": entry["college"]},
            {"$set": entry},
            upsert=True
        )
        return True
    except Exception as e:
        print(f"Error inserting entry: {e}")
        raise
    finally:
        client.close()