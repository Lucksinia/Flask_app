from flask import Blueprint, render_template
from werkzeug.exceptions import NotFound

report = Blueprint("report", __name__, static_folder="../static", url_prefix="/reports")

REPORTS = {1: "Smt1", 2: "Smth2", 3: "Smth3"}


@report.route("/", endpoint="list")
def report_list():
    return render_template(
        "reports/list_of_reports.html",
        reports=[1, 2, 3, 4, 5],
    )


@report.route("/<int:pk>", endpoint="details")
def get_report(pk: int):
    try:
        report = REPORTS[pk]
    except KeyError:
        raise NotFound(f"User {pk} was not found! Maybe try another..?")
    return render_template(
        "reports/details.html",
        report_name=report,
    )
