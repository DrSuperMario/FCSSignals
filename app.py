from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

import os

from resources.users import UserRegister, User, UserLogin
from resources.signals import Signal, SignalList
from resources.market import Market, MarketList
from db import db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL' , 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'WYehvdjHM9chd@X'
api = Api(app)


jwt = JWTManager(app)

#@jwt.user_claims_loader
#def add_claims_to_jwt(identity):
#    if identity == 1:
#        return {'is_admin':True}
#    return {'is_admin': False}

api.add_resource(Market, '/market/<string:name>')
api.add_resource(MarketList, '/markets')
#api.add_resource(Signal, '/markets/market/signal/<string:name>')
api.add_resource(Signal, '/signal/<string:signal_name>')
api.add_resource(SignalList, '/signals')
api.add_resource(UserRegister, '/register')
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserLogin, '/login')



if __name__=="__main__":
    db.init_app(app)

    @app.before_first_request
    def create_tables():
        try:
            db.create_all()
        except:
            print("UUPS Something went seriously wrong")
    
    app.run(port=5000)