from flask import (
    Flask, render_template, session, 
    url_for, redirect, send_file
)

app = Flask(__name__)
app.secret_key = "SecretKey"

@app.get("/")
def index():
    userid = session.get("userid", None)
    error = session.pop("error", None)
    success = session.pop("success", None)
    result = {}

    return render_template("index.html", userid=userid, success=success, error=error, result=result)