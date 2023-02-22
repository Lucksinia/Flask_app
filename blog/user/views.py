from flask import Blueprint

user = Blueprint("user", __name__, static_folder="../static", url_prefix="/users")


@user.route("/")
def user_list():
    return "user_list_here"


@user.route("/<pk>")
def get_user(pk: int):
    return pk
