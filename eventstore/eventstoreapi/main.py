from flask import Flask
# import api
from api import app_blueprints

app = Flask(__name__)
app.register_blueprint(app_blueprints)
if __name__ == '__main__':
    app.run(debug=True)