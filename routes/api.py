from flask import Blueprint, jsonify

api_pb = Blueprint("api", __name__)


@api_pb.route("/health", methods=["GET"])
def health_check():
    """
    Health check endpoint.
    """
    return jsonify({"status": "ok"}), 200
