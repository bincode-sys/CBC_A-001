from flask_restful import Resource, reqparse
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class InsertDB(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('week', type=int, required=True, help="Week number is required")
        self.parser.add_argument('college', type=str, required=True, help="College name is required")
        self.parser.add_argument('transport', type=float, required=True, help="Transport mileage is required")
        self.parser.add_argument('fuel', type=str, required=True, help="Fuel type is required")
        self.parser.add_argument('energy', type=float, required=True, help="Energy usage is required")
        self.parser.add_argument('diet', type=str, required=True, help="Diet type is required")
        self.parser.add_argument('emissions', type=dict, required=True, help="Emissions data is required")

    def post(self):
        args = self.parser.parse_args()
        week = args['week']
        college = args['college']
        transport = args['transport']
        fuel = args['fuel']
        energy = args['energy']
        diet = args['diet']
        emissions = args['emissions']

        # Validate emissions structure
        if not isinstance(emissions, dict) or 'total' not in emissions or 'breakdown' not in emissions:
            return {'message': 'Emissions data must include total and breakdown'}, 400

        # Generate backend suggestions using model.py
        from model import predict_reduction_suggestions
        backend_suggestions = predict_reduction_suggestions(emissions, transport, energy)

        # Prepare the document to insert into MongoDB
        document = {
            'week': week,
            'college': college,
            'transport': transport,
            'fuel': fuel,
            'energy': energy,
            'diet': diet,
            'emissions': emissions,
            'suggestions': emissions.get('suggestions', []) + backend_suggestions  # Combine frontend and backend suggestions
        }

        # Insert or update in MongoDB
        try:
            mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
            client = MongoClient(mongo_uri)
            
            # Test connection
            client.server_info()
            
            db = client['carbon']
            collection = db['footprints']
            
            # Use upsert to insert or update based on week and college
            collection.update_one(
                {'week': week, 'college': college},
                {'$set': document},
                upsert=True
            )
            
            client.close()
            # Return the emissions data as the response
            return {
                'totalEmissions': emissions['total'],
                'breakdown': emissions['breakdown'],
                'suggestions': document['suggestions']  # Include combined suggestions in response
            }, 200
        except Exception as e:
            return {'message': f'Error inserting data: {str(e)}'}, 500
        finally:
            if 'client' in locals():
                client.close()