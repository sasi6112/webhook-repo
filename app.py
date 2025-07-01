from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
import datetime

app = Flask(__name__)
client = MongoClient("mongodb+srv://admin:admin@cluster0.5foly4b.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["webhookDB"]
collection = db["webhookEvents"]

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    event = request.headers.get("X-GitHub-Event", "manual")
    payload = {
        "request_id": data.get("after", "manual"),
        "author": data.get("pusher", {}).get("name", "anonymous"),
        "action": event.upper(),
        "from_branch": "unknown",
        "to_branch": "main",
        "timestamp": datetime.datetime.utcnow()
    }
    collection.insert_one(payload)
    return jsonify({"message": "Event stored"}), 200

@app.route('/')
def index():
    items = list(collection.find({}, {"_id": 0}))
    return render_template("index.html", data=items)

if __name__ == '__main__':
    app.run(port=5000)

