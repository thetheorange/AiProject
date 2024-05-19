from flask import Flask

from Api.auth import auth_blu
from Api.model import model_blu

app = Flask(__name__)

app.register_blueprint(auth_blu)
app.register_blueprint(model_blu)

if __name__ == '__main__':
    app.run(debug=True)
