from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.market import MarketModel



class Market(Resource):

    def get(self,name):
        market = MarketModel.find_market(name)
        if market:
            return market.json()
        return {"message":"Marketplace not found"}, 404

    @jwt_required
    def post(self,name):
        if MarketModel.find_market(name):
            return {"message":"Marketplace {} already exists".format(name)}
        market = MarketModel(name)
        try:
            market.save_to_db()
        except:
            return {"message":"An error occured while creating input"}, 500

        return market.json(), 201

    @jwt_required
    def delete(self,name):
        market = MarketModel.find_market(name)
        try:
            if market:
                market.delete_from_db()

            return {"message":"Market deleted"}
        except:
            return {"message":"UUPS Somethng went wrong!"}, 500

class MarketList(Resource):
    
    def get(self):
        return {'markets':[market.json() for market in MarketModel.query.all()]}

    