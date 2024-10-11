#!/usr/bin/efrom flask import Flask, abort, jsonify, request, make_response
from flask import Flask, abort, jsonify, make_response, request
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

class Plants(Resource):
    def get(self):
        """Returns a list of all plants."""
        plants = Plant.query.all()
        return jsonify([plant.to_dict() for plant in plants])

    def post(self):
        """Allows users to create Plant records through the "/plants" POST route."""
        data = request.get_json()
        if not data:
            abort(400, message="Request body must be json")
        try:
            new_plant = Plant(
                name=data['name'],
                image=data['image'],
                price=data['price']
            )
            db.session.add(new_plant)
            db.session.commit()
            response = make_response(jsonify(new_plant.to_dict()), 201)
            return response
        except KeyError as e:
            abort(400, message=f"missing required field: {str(e)}")

class PlantByID(Resource):
    def get(self, id):
        """Returns a single Plant object at "/plants/<int:id>"."""
        plant = Plant.query.get(id)
        if not plant:
            abort(404, message=f"plant with {id} not found")
        return jsonify(plant.to_dict())

api.add_resource(Plants, '/plants')
api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
