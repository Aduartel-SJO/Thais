from flask import Flask
from routes.mesas import mesas


app = Flask(__name__)

app.add_url_rule('/', 'mesas', mesas)  

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)