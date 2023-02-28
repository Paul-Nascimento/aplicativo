from flask import Flask,render_template,request,url_for,redirect,flash,jsonify
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)


@app.route("/")
def menu():
    return render_template("menu.html")




if __name__ == "__main__":
    app.run(port=8085,host="0.0.0.0",debug=True,threaded=True)
