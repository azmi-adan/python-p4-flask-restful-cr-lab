from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Plant(db.Model, SerializerMixin):
    __tablename__ = 'plants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False, default="https://i.pinimg.com/474x/10/05/22/1005223b9956fd09a9ee099c90b15133.jpg")
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False, default=0.0)

    def to_dict(self):
        """Convert Plant object to dictionary for serialization."""
        return {
            "id": self.id,
            "name": self.name,
            "image": self.image,
            "price": str(self.price),  # Convert to string to avoid serialization issues
        }
