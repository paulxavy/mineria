from flask import Flask,jsonify
from flask import request,render_template
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)


@app.route("/")
def index() -> str:
  return render_template("index.html")


@app.route('/upload2', methods=['GET','POST'])
def upload_file2():
  json_data = request.json
  a_value = json_data["data"] #la palabra correcta desde de correr el algoritmo
  return jsonify(value=a_value)

@app.route('/upload', methods=['GET','POST'])
def upload_file():
  json_data = request.json
  a_value = json_data["data"] #la palabra correcta desde de correr el algoritmo
  resp = requests.post('https://flask-backenduce.herokuapp.com/', json=json_data)
  #print(resp.json())
  return jsonify(value=resp.json()["value"])
#jsonify(value=resp)
if __name__ == "__main__":
  app.run(port=8000, debug=True)