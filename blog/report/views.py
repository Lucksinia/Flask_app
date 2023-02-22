from flask import Blueprint

report = Blueprint("report", __name__, static_folder="../static", url_prefix="/reports")


@report.route("/")
def report_list():
    return "report_list_here"
