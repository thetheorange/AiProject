from . import auth_blu


@auth_blu.route("/auth")
def test() -> str:
    return "hello"
