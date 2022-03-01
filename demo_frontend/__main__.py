import os
import requests
from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

PORT = os.getenv("PORT", 5000)
DEBUG = os.getenv("DEBUG", "false")
BACKEND_FQDN = "https://gds-paas-demo-backend.herokuapp.com"


@api.resource("/tables")
class GetTables(Resource):
    def get(self):
        try:
            r = requests.get(f"{BACKEND_FQDN}/tables")
            return r.json()
        except Exception as e:
            return {"error": "it failed.", "details": str(e)}


@api.resource("/")
class HelloWorld(Resource):
    def get(self):
        return {"hello": "world", "service": "frontend"}


if __name__ == "__main__":
    debug = False if DEBUG == "false" else True
    app.run(debug=debug, host="0.0.0.0", port=PORT)
