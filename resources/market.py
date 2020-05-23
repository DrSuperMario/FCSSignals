from flask_restful import Resource, reqparse
from models.market import MarketModel



class Market(Resource):

    def get(self,name):
        market = MarketModel.find_market(name)
        if market:
            return market.json()
        return {"message":"Marketplace not found"}, 404

    def post(self,name):
        if MarketModel.find_market(name):
            return {"message":"Marketplace {} already exists".format(name)}
        market = MarketModel(name)
        try:
            market.save_to_db()
        except:
            return {"message":"An error occured while creating input"}, 500

        return market.json(), 201

    def delete(self,name):
        market = MarketModel.find_market(name)
        if market:
            market.delete_from_db()

        return {"message":"Market deleted"}

class MarketList(Resource):
    
    def get(self):
        return {'markets':[market.json() for market in MarketModel.query.all()]}

    