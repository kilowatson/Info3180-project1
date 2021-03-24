from . import db

class Property(db.Model):

    __tablename__ = 'properties'

    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String())
    description = db.Column(db.String())
    rooms = db.Column(db.String())
    bathrooms=db.Column(db.String())
    price = db.Column(db.String())
    prop_type = db.Column(db.String())
    location = db.Column(db.String())
    photo = db.Column(db.String())
    

    def __init__(self, title, description, rooms, bathrooms, price, prop_type, location,photo):
        self.title=title
        self.description=description
        self.rooms=rooms
        self.bathrooms=bathrooms
        self.price=price
        self.prop_type=prop_type
        self.location=location
        self.photo=photo
        