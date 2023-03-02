from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound

user = Blueprint("user", __name__, static_folder="../static", url_prefix="/users")

USERS = {1: "Alice", 2: "Johan", 3: "Mikail"}


@user.route("/", endpoint="list")
def user_list():
    return render_template(
        "users/list_of_people.html",
        users=USERS,
    )


@user.route("/<int:pk>", endpoint="details")
def get_user(pk: int):
    try:
        user = USERS[pk]
    except KeyError:
        raise NotFound(f"User {pk} was not found! Maybe try another..?")
    return render_template(
        "users/details.html",
        user_name=user,
    )
