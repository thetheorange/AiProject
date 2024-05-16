from . import model_blu


@model_blu.route("/gpt-text-model")
def text_model() -> str:
    return "this is gpt-text-model"
