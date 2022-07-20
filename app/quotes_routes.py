from flask import Blueprint, request, jsonify
import os
from dotenv import load_dotenv
import requests

load_dotenv()

proxy_bp = Blueprint("proxy_bp", __name__)

zen_key = os.environ.get("ZEN_KEY")

@proxy_bp.route("/zen", methods=["GET"])
def get_lat_lon():
    # loc_query = request.args.get("q")
    # if not loc_query:
    #     return {"message": "must provide q parameter (location)"}

    response = requests.get(
        "https://zenquotes.io/api/random/",
        params={"key": zen_key, "format": "json"}
    )

    return jsonify(response.json())