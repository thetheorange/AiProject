from datetime import timedelta

from flask import Flask, Response, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from gevent import pywsgi

from Api import back_stage
from Api.auth import auth_blu
from Api.back_stage import back_stage_blu
from Api.model import model_blu
from Core.StatusCode import StatusCode
from Logging import app_logger
from config import config_json

app = Flask(__name__)
# 限制上传文件的最大大小为16k
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000

# 设置jwt秘钥
app.config["JWT_SECRET_KEY"] = config_json["flask"]["jwt_secret"]
# 设置ACCESS_TOKEN的默认过期时间为1小时
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
jwt = JWTManager(app)

app.register_blueprint(auth_blu)
app.register_blueprint(model_blu)
app.register_blueprint(back_stage_blu)

# 配置跨域
CORS(app)


# 设置全局异常捕获
@app.errorhandler(404)
def handle_404_error(error) -> Response:
    app_logger.error(f"[404] {error}")
    return jsonify({
        "code": StatusCode.AppNotFoundError,
        "msg": "404错误 找不到此页面"
    })


@app.errorhandler(400)
def handle_400_error(error) -> Response:
    app_logger.error(f"[400] {error}")
    return jsonify({
        "code": StatusCode.AppQueryMethodError,
        "msg": "400错误 客户端请求方式错误"
    })


@app.errorhandler(500)
def handle_500_error(error) -> Response:
    app_logger.error(f"[500] {error}")
    return jsonify({
        "code": StatusCode.AppInternalError,
        "msg": "500错误 服务器内部错误"
    })


if __name__ == "__main__":
    app.run(debug=False,
            host=config_json["flask"]["server"],
            port=config_json["flask"]["port"])
    server = pywsgi
