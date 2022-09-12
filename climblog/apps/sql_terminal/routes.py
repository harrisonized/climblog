from flask import Blueprint, request, render_template, Response
from climblog.utils.auth.connections import postgres_connect_fetch_close


sql_terminal = Blueprint('sql_terminal', __name__,
                         template_folder='templates',
                         static_folder='static')


@sql_terminal.route("/query", methods=["GET", "POST"])
def query():
    return render_template("query.html")


@sql_terminal.route("/download", methods=["POST"])
def download():
    query = request.form.get('query')
    df = postgres_connect_fetch_close(query)
    data = df.to_csv(index=False, header=True, sep=",")
    return Response(data,
                    mimetype="text/csv",
                    headers={"Content-disposition": "attachment; filename=climbing-log.csv"})
