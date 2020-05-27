import os
from flask import Flask, Blueprint, render_template, request, flash
from api.upload import uploadapi
from flask_json import FlaskJSON

app = Flask(__name__)
app.config['SECRET_KEY'] =  os.urandom(12)


app.register_blueprint(uploadapi)
FlaskJSON(app)



@app.route("/",methods=["GET","POST"])
def index():
    if request.method == "POST":
        flash("Successed","success")
    return render_template("index.html")

    
if __name__ == "__main__":
    app.run(debug=True)