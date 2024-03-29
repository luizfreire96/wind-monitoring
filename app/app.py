from flask import Flask
from dash_application import create_dash_application
import os

app = Flask(__name__)
create_dash_application(app)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 80))
    app.run(host='0.0.0.0', port=port)