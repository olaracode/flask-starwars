from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# db.Model = Base
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

# Que modelos necesitamos para crear la starwars api
# Despues de modificar o agregar un modelo a la BBDD
# Corremos pipenv run migrate y despues pipenv run upgrade

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    eye_color = db.Column(db.String(17), nullable=True, default='N/A')
    homeworld = db.Column(db.String(80), nullable=True, default='N/A')
    gender = db.Column(db.String(80), nullable=True, default='N/A')

    def __repr__(self):
        return '<Character %r>' % self.name

    def serialize(self):
        return {
            "id":  self.id,
            "name": self.name,
            "eye_color": self.eye_color,
            "homeworld": self.homeworld,
            "gender": self.gender
        }
# Creamos el modelo Planet
class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # nullable -> No requerido?
    name = db.Column(db.String(50), nullable=False)
    population = db.Column(db.Integer, nullable=True)
    climate = db.Column(db.String(100), nullable=True)
    terrain = db.Column(db.String(100), nullable=True)
    faction = db.Column(db.String(100), nullable=True)

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id":  self.id,
            "name": self.name,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "faction": self.faction
        } 
