from flask import Flask
# from api import *
# from flask import Flask
from api import app
from config import filepath

if __name__ == '__main__':
    app.config['filepath'] = filepath 
    app.run(debug=True)

