"""
Des 各大模型调用接口
@Author thetheOrange
Time 2024/5/19
"""
from . import model_blu


@model_blu.route("/gpt-text-model")
def text_model() -> str:
    return "this is gpt-text-Model"


@model_blu.route("/gpt-voice-model")
def voice_model() -> str:
    return "this is gpt-voice-Model"
