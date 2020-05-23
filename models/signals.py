from db import db




class SignalModel(db.Model):
    __tablename__ = 'signals'
    
    id = db.Column(db.Integer, primary_key=True)
    signal_name = db.Column(db.String(10))
    opinion = db.Column(db.String(7))
    change = db.Column(db.String(7))
    
    market_id = db.Column(db.Integer, db.ForeignKey('market.id'))
    market = db.relationship('MarketModel')

    def __init__(self,signal_name, opinion, change, market_id):
        self.signal_name = signal_name
        self.opinion = opinion
        self.change = change
        self.market_id = market_id

    def json(self):
        return {'signal_name': self.signal_name,'opinion': self.opinion,'change': self.change}

    @classmethod
    def find_market_by_id(cls, market_id):
        return cls.query.filter_by(id=market_id).first()

    @classmethod
    def find_signal_by_name(cls, signal_name):
        return cls.query.filter_by(signal_name=signal_name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
