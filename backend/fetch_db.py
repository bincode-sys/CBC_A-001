from flask_restful import Resource
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from pymongo.errors import ConnectionFailure

# Load environment variables
load_dotenv()

class FetchDB(Resource):
    def get(self):
        try:
            # MongoDB connection
            mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
            client = MongoClient(mongo_uri)
            
            # Test connection
            client.server_info()  # Raises ConnectionFailure if connection fails
            
            db = client['carbon']
            collection = db['footprints']

            # Fetch all documents from the collection
            data = list(collection.find({}, {'_id': 0}))  # Exclude the '_id' field
            
            client.close()  # Close the connection
            return data, 200
        except ConnectionFailure as e:
            return {'message': f'Failed to connect to MongoDB: {str(e)}'}, 500
        except Exception as e:
            return {'message': f'Error fetching data: {str(e)}'}, 500
        finally:
            if 'client' in locals():
                client.close()