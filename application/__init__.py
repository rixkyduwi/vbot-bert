from flask import Flask,request, render_template
from flask_restful import Resource, Api
from flask_mysqldb import MySQL
from flask_httpauth import HTTPTokenAuth
from flask_cors import CORS
# from dotenv import load_dotenv
# load_dotenv()
# import os
# import MySQLdb
# mysql = MySQLdb.connect(
#   host= os.getenv("HOST"),
#   user=os.getenv("USERNAME"),
#   passwd= os.getenv("PASSWORD"),
#   db= os.getenv("DATABASE"),
#   ssl_mode = "VERIFY_IDENTITY",
#   ssl      = {
#     "ca": "/etc/ssl/cert.pem"
#   }
# )

app = Flask(__name__)
api = Api(app)
mysql = MySQL(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vbot_bert.db'
app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD']  = ''
app.config['MYSQL_DB'] = 'halosus'

class apipredict(Resource):
    def get(self):
        question = request.args.get('pertanyaan')
        print(question)
        prediction = bert_prediction(str(question))
        print(prediction)
        return prediction
class apitips(Resource):
    def get(self):
        response = tips()
        return response
class apichatgpt(Resource):
    def get(self):
        question = request.args.get('pertanyaan')
        print(question)
        response = random_question(question)
        print(response)
        return response
class apiinputdokter(Resource):
    def post(self):
        cur = mysql.connection.cursor()
        response = {}
        id_dokter = request.form['id_dokter']
        print("1")
        nama_penyakit = request.form['nama_penyakit']
        print("2")
        gejala = request.form['gejala']
        print("3")
        pencegahan = request.form['pencegahan']
        print("4")
        rujukan = request.form['rujukan']
        print("5")
        cur.execute("INSERT INTO input_dokter(id_dokter,nama_penyakit,gejala,pencegahan,rekomendasi_rujukan) VALUES(%s,%s,%s,%s,%s)" , (id_dokter,nama_penyakit,gejala,pencegahan,rujukan))
        print("6")
        mysql.connection.commit()
        response.update({"status": "sukses","msg":"Data Berhasil Diinputkan"})
        return response

@app.route("/")
def index():
    return render_template("landingpage.html")
@app.route("/tips")
def tips_hidup_sehat():
    data = tips()
    return render_template("tips.html",data=data)
@app.route("/chat")
def chat():
    return render_template("index.html")
@app.route("/input-dokter")
def input_dokter():
    return render_template("inputdokter.html")

api.add_resource(apipredict, '/api/v1/model/predict', methods=['GET'])
api.add_resource(apitips, '/api/v1/scrap/tips', methods=['GET'])
api.add_resource(apiinputdokter, '/api/v1/dokter/input', methods=['POST'])
api.add_resource(apichatgpt, '/api/v1/chatgpt/predict', methods=['GET'])

CORS(app)

from .bert import bert_prediction,random_question
from .scrapping_tips_hidup_sehat import tips