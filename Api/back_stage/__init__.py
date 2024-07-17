from flask import Blueprint

back_stage_blu = Blueprint("back_stage", __name__)

from . import BackStageApi
