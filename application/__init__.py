from flask import Flask,request, render_template
from flask_restful import Resource, Api
from flask_httpauth import HTTPTokenAuth
from flask_mysqldb import MySQL 
from flask_cors import CORS


app = Flask(__name__)
api = Api(app)
mysql = MySQL()
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
        return prediction
class apitips(Resource):
    def get(self):
        response = tips()
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

api.add_resource(apipredict, '/api/v1/model/predict', methods=['GET'])
api.add_resource(apitips, '/api/v1/scrap/tips', methods=['GET'])
mysql.init_app(app)
CORS(app)

from .bert import bert_prediction
from .scrapping_tips_hidup_sehat import tips