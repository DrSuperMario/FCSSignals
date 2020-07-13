from app import app, db


if __name__=="__main__":
    db.init_app(app)

    @app.before_first_request
    def create_tables():
        try:
            db.create_all()
        except:
            print("UUPS Something went seriously wrong")
    
    app.run()