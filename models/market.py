from db import db


class MarketModel(db.Model):
    __tablename__ = 'market'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    signals = db.relationship('SignalModel' , lazy='dynamic')

    def __init__(self,name):
        self.name = name

    def json(self):
        return {'Name': self.name,'Signals': [signal.json() for signal in self.signals.all()]}

    @classmethod
    def find_market(cls, name):
        return cls.query.filter_by(name=name).first()
    
    @classmethod
    def find_market_by_id(cls,_id):
        return cls.query.filter_by(id=_id).first()    

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(seif)
        db.session.commit()