import sys
import os
from flaskr import create_app 
from flask import current_app as app

environment = os.environ["ENVIRONMENT"]

if __name__ == "__main__":
    args = sys.argv[1:]
    app = create_app(environment)
    app.run(host="0.0.0.0", port=5000)
