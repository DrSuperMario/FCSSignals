import requests as req
import json


#get data from API
class GetData():

    def __init__(self,url):
        self.url = url

    def parse_url_data(self):
        data = req.get(self.url)
        return data.content   

    def parse_json_data(self):
        data = req.get(self.url)
        _json = json.loads(data.content)
        return _json

if __name__=="__main__":
    app = GetData("http://127.0.0.1:5000/markets")
    jsonify = app.parse_json_data()

    

        
#make data Beutiful