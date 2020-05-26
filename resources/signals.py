from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required
from models.signals import SignalModel
from models.market import MarketModel
from datetime import datetime as dt


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

    parser.add_argument('date', 
                        type=str,
                        default=dt.now(),
                        required=False,
                        help="Sometging went wrong with datetime"

    )
    

    def get(self,signal_name):
        signal = SignalModel.find_signal_by_name(signal_name)
        if signal:
            return signal.json()
        return {"message":"signal name not found"}, 404

    @jwt_required
    def post(self,signal_name):

        data = Signal.parser.parse_args()
        data['date'] = dt.now()
        signal = SignalModel(signal_name, **data)
        market = MarketModel.find_market_by_id(data['market_id'])
        if not market:
            return {"message":"Market ({}) not found  should be 1 <--Stock  2 <--Crypto 3 <--Forex".format(data['market_id'])}

        try:
            signal.save_to_db()
        except:
            return {"message":"An error occured while loading signal"}, 500
        return signal.json(), 201

    @jwt_required
    def delete(self,signal_name):
        signal = SignalModel.find_signal_by_name(signal_name)
        try:
            if signal:
                signal.delete_from_db()
            else:
                return {"message":"Signal -->{}<-- was not found!".format(signal_name)}, 400

            return {"message":"signal -->{}<--  Deleted sucsessfully".format(signal_name)}, 201
        except:
            return {"message":"UUPS something went wrong"}, 500

    @jwt_required
    def put(self,signal_name):
        data = Signal.parser.parse_args()
        signal = SignalModel.find_signal_by_name(signal_name)

        try: 
            if signal is None:
                signal = SignalModel(signal_name, **data)
                signal.save_to_db()
                return {"message":"New Signal -->{}<-- Created".format(signal_name)}, 201
            elif data['opinion'] != signal.opinion:
                signal.opinion = data['opinion']
            elif data['change'] != signal.change:
                signal.change = data['change']
        except:
            return {"message":"UUPS something went wrong"}, 500

        signal.save_to_db()
        return signal.json()



class SignalList(Resource):
    def get(self):
        return {'signals': [x.json() for x in SignalModel.query.all()]}