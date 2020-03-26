from flask import Flask, render_template, request

#Flaskオブジェクトの生成
app = Flask(__name__)

#「/」へアクセスがあった場合に、「index.html」を返す
@app.route("/")
def index():
    name = request.args.get("name")
    return render_template("index.html", name=name)

@app.route("/", methods=["post"])
def post():
    name = request.form["name"]
    return render_template("index.html", name=name)

if __name__ == "__main__":
    app.run(debug=True)
