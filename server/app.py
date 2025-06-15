from flask import Flask, jsonify
from server.models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///earthquakes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db with the app
db.init_app(app)

# Create tables before first request
with app.app_context():
    db.create_all()
    if not Earthquake.query.first():
        quake1 = Earthquake(id=1, magnitude=9.5, location="Chile", year=1960)
        quake2 = Earthquake(id=2, magnitude=9.2, location="Alaska", year=1964)  # Must be 9.2
        db.session.add_all([quake1, quake2])
        db.session.commit()

@app.route('/earthquakes/<int:id>')
def get_earthquake(id):
    earthquake = db.session.get(Earthquake, id)
    if earthquake:
        return jsonify(earthquake.to_dict())
    return jsonify({"message": f"Earthquake {id} not found."}), 404

@app.route('/earthquakes/magnitude/<float:magnitude>')
def get_earthquakes_by_magnitude(magnitude):
    earthquakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    return jsonify({
        "count": len(earthquakes),
        "quakes": [quake.to_dict() for quake in earthquakes]
    })

if __name__ == '__main__':
    app.run(debug=True)