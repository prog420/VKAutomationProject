import time
import json
from flask import Flask, request

app = Flask(__name__)
USERS = {}


@app.route("/", methods=["GET"])
def home():
    """
    Route for debugging / tracking user data
    """
    return json.dumps(USERS)


@app.route("/vk_id/<user>", methods=["GET"])
def get_vk_id(user):
    """
    Get VK ID of a user
    :param user: Username
    """
    vk_id = USERS.get(user)
    if vk_id is None:
        return json.dumps({}), 404
    else:
        return json.dumps({'vk_id': vk_id}), 200


@app.route("/user", methods=["POST"])
def create():
    """
    Create new user with vk id
    """
    user = request.json["user"]
    vk_id = request.json["vk_id"]

    if USERS.get(user) is None:
        USERS[user] = vk_id
        return json.dumps({'vk_id': vk_id}), 201
    else:
        USERS[user] = vk_id
        return json.dumps({'vk_id': vk_id}), 204


@app.route("/user/<user>/change-vk-id", methods=["PUT"])
def update(user):
    """
    Update VK ID of a user if user exists
    :param user: Username
    """
    vk_id = request.json["vk_id"]

    if USERS.get(user) is None:
        return json.dumps({}), 404
    else:
        USERS[user] = vk_id
        return json.dumps({'vk_id': vk_id}), 204


@app.route("/user/<user>", methods=["DELETE"])
def delete(user):
    """
    Delete user if exists
    :param user: Username
    """
    if USERS.get(user) is None:
        return json.dumps({}), 404
    else:
        return json.dumps({'vk_id': USERS.pop(user)}), 204


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8083)
