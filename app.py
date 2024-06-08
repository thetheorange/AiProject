from flask import Flask

from Api.auth import auth_blu
from Api.model import model_blu

app = Flask(__name__)
# 限制上传文件的最大大小为16k
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

app.register_blueprint(auth_blu)
app.register_blueprint(model_blu)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5120)
