import requests
import json
import re
from datetime import datetime as dt


data = requests.get("http://127.0.0.1:5000/markets")
web_data = data.content
jsonify = json.loads(web_data)



class FindMarket():
    
    def __init__(self, market_id=int, jsonfile=None):
        self.market_id = market_id
        self.jsonfile = jsonify

    def find_market_data(self):
        return self.jsonfile['markets'][self.market_id]['Signals']

    @classmethod    
    def find_all_market_data(cls, json_data=None):
        freshlist = []
        for x in range(len(json_data['markets'])):
            for y in range(len(json_data['markets'][x]['Signals'])):
                for keys, values in json_data['markets'][x]['Signals'][y].items(): 
                    freshlist.append(keys + ":" + values)
        return freshlist

    
    
    @classmethod
    def find_data_by_key(cls, obj, key):
        key_list = []
        
        def extract_data(obj, key_list, key):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if isinstance(v, (dict, list)):
                        extract_data(v, key_list, key)
                    elif k == key:
                        key_list.append(v)
            elif isinstance(obj, list):
                for item in obj:
                    extract_data(item, key_list, key)
            return key_list

        results = extract_data(obj, key_list, key)
        return results
        

all_data = FindMarket.find_all_market_data(json_data=jsonify)
all_data_key = FindMarket.find_data_by_key(jsonify, 'signal_name')
