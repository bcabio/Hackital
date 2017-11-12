from flask import Flask, send_from_directory, request
import requests
from pymongo import MongoClient
import time
from bson.json_util import dumps


client = MongoClient("mongodb://admin:admin@ds259105.mlab.com:59105/hackital")

db = client['hackital']
collection = db['drawer_history']


app = Flask(__name__)

@app.route('/isOpening', methods=["POST"])
def opening():
	instance = {'event' : 'drawerOpened', \
				'time' : int(time.time()),
				'wasUser': None}
	try:	
		collection.insert_one(instance)
		return "done"
	except:
		return "rip"

@app.route('/verify', methods=["POST"])
def verify():
	time = request.args.get('time')
	wasUser = request.args.get('wasUser')
	try: 
		result = collection.update_one({'time': time }, {"$set" :{"wasUser": wasUser}})
		return "DB Successfully written to"
	except:
		return "rip DB"

@app.route('/getTimestamps', methods=["GET"])
def get_timestamps():
	return dumps(collection.find())

if __name__ == "__main__":
	from os import environ
	app.run(host="0.0.0.0", port=environ.get("PORT", "8000"))