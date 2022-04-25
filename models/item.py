from db import db


class ItemModel(db.Model):

    __tablename__ = 'items'

    i_id = db.Column(db.Integer, primary_key=True)
    i_name = db.Column(db.String(80))
    i_price = db.Column(db.Float(precision=2))

    i_store_id = db.Column(db.Integer, db.ForeignKey('stores.s_id'))
    store = db.relationship('StoreModel')

    def __init__(self, name, price, store_id) -> None:
        self.i_name = name
        self.i_price = price
        self.i_store_id = store_id

    def json(self):
        return {'name': self.i_name, 'price': self.i_price, 'store_id': self.i_store_id}

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(i_name=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
