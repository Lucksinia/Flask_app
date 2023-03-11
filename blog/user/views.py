from flask import Blueprint, render_template
from flask_login import login_required
from werkzeug.exceptions import NotFound
from blog.models import User

user = Blueprint("user", __name__, static_folder="../static", url_prefix="/users")


@user.route("/", endpoint="list")
def user_list():
    users = User.query.all()
    return render_template(
        "users/list_of_people.html",
        users=users,
    )


@user.route("/<int:pk>", endpoint="profile")
@login_required
def profile(pk: int):
    selected_user = User.query.filter_by(id=pk).one_or_none()
    if not selected_user:
        raise NotFound(f"User {pk} was not found! Maybe try another..?")
    return render_template(
        "users/details.html",
        user_name=selected_user,
    )
