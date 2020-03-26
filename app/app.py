from flask import Flask,render_template,request

#Flaskオブジェクトの生成
app = Flask(__name__)

#「/」へアクセスがあった場合に、"Hello World"の文字列を返す
@app.route("/")
def hello():
    return "Hello World"

#「/index」へアクセスがあった場合に、「index.html」を返す
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/index", methods=["post"])
def post():
    name = request.form["name"]
    return render_template("index.html", name=name)

if __name__ == "__main__":
    app.run(debug=True)
