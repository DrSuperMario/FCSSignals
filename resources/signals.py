from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.signals import SignalModel
from models.market import MarketModel


class Signal(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('opinion',
                        type=str,
                        required=False,
                        help="You must add opinion index!!"
    )
    parser.add_argument('change',
                        type=str,
                        required=True,
                        help="You must add change index!!"
    )
    
    parser.add_argument('market_id',
        type=int,
        required=True,
        help="Market dosen't Exist"
    )
    
    @jwt_required
    def get(self,signal_name):
        signal = SignalModel.find_signal_by_name(signal_name)
        if signal:
            return signal.json()
        return {"message":"signal name not found"}, 404

    def post(self,signal_name):

        data = Signal.parser.parse_args()
        signal = SignalModel(signal_name, **data)
        market = MarketModel.find_market_by_id(data['market_id'])
        if not market:
            return {"message":"Market ({}) not found  should be 1 <--Stock  2 <--Crypto 3 <--Forex".format(data['market_id'])}

        try:
            signal.save_to_db()
        except:
            return {"message":"An error occured while loading signal"}, 500
        return signal.json(), 201

    #@jwt_required#@jwt_required()
    def delete(self,signal_name):
        signal = SignalModel.find_signal_by_name(tocker_name)
        if signal:
            signal.delete_from_db()
        return {"message":"signal Deleted sucsessfully"}

    #@jwt_required()
    def put(self,signal_name):
        data = Signal.parser.parse_args()
        signal = SignalModel.find_signal_by_name(signal_name)

        if signal is None:
            signal = SignalModel(signal_name, **data)
        elif data['Opinion'] is None:
            signal.Opinion = data['Opinion']
        elif data['Change'] is None:
            signal.Change = data['Change']
        
        signal.save_to_db()
        return signal.json()



class SignalList(Resource):
    @jwt_required
    def get(self):
        return {'signals': [x.json() for x in SignalModel.query.all()]}