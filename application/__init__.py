from functools import wraps
from http.client import responses
import random
import string
from time import time
import time
from flask import Response, Flask,request, render_template, redirect,url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
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

#login session
def login_required(self):
    def decorator(original_route):
        @wraps(original_route)
        def decorated_route(*args, **kwargs):
            if 'loggedin' in session:
            # User is loggedin show them the home page
                print(session['time'])
                if session['time'] != ""+str(time.gmtime().tm_year)+"-"+str(time.localtime().tm_mon)+"-"+str(time.localtime().tm_mday)+"":
                    print('session expired')
                    session.pop('loggedin', None)
                    session.pop('id', None)
                    session.pop('role', None)
                    session.pop('username', None)
                    session.pop('time', None)
                    return redirect(url_for('login_dokter'))
                else:
                    print('anda sudah login')
                    return original_route(*args, **kwargs)
            else:
                return redirect(url_for('login_dokter'))
        return decorated_route
    return decorator 

#contorller
class index(Resource):
    def get(self):
        #print(generate_password_hash('blabla12'))
        return Response(render_template("landingpage.html"),mimetype='text/html')
class chat(Resource):
    def get(self):
        return Response(render_template('index.html'),mimetype='text/html')
class apitips(Resource):
    def get(self):
        respon = tips()
        title = respon[0].title
        sumber = respon[0].sumber
        data = respon[0].isi
        return Response(render_template('tips.html',titile=title,data=data,sumber=sumber),mimetype='text/html')
class login_dokter(Resource):
    def get(self):
        if 'loggedin' in session:
            return redirect(url_for('input_dokter'))
        else: 
            return Response(render_template("login.html"),mimetype='text/html')
class input_dokter(Resource):
    def get(self):
        return Response(render_template("inputdokter.html"),mimetype='text/html')
class apipredict(Resource):
    def get(self):
        question = request.args.get('pertanyaan')
        print(question)
        prediction = bert_prediction(str(question))
        print(prediction)
        return prediction

class apichatgpt(Resource):
    def get(self):
        question = request.args.get('pertanyaan')
        print(question)
        response = random_question(question)
        print(response)
        return response
class apiinputdokter(Resource):
    @login_required
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
class apilogindokter(Resource):
    def post(self):
        a=time.localtime()
        tanggal=""+str(time.gmtime().tm_year)+"-"+str(a.tm_mon)+"-"+str(a.tm_mday)+""
        cur = mysql.connection.cursor()
        username = request.form['username']
        password = request.form['password']
        cur.execute("SELECT * FROM login WHERE username = %s" , (username,))
        datalogin = cur.fetchone()
        print(datalogin)
        if datalogin == None:
            print("laka")
            cur.close()
            return redirect(url_for('login_dokter',alert="maaf username tidak ada"))
        elif not check_password_hash(datalogin[1],password):
            cur.close()
            return redirect(url_for('auth.index',alert="maaf password salah"))
        else:
            if datalogin[2]=='admin':
                cur.execute("SELECT login.nip,login.role, admin.nama,admin.email,admin.alamat,admin.no_hp FROM login INNER JOIN admin ON login.nip = admin.nip WHERE login.nip = %s" , (nip,))
                datalogin= cur.fetchone()
            elif datalogin[2]=='HRD':
                cur.execute("SELECT login.nip,login.role, hrd.nama,hrd.email,hrd.alamat,hrd.no_hp FROM login INNER JOIN hrd ON login.nip = hrd.nip WHERE login.nip = %s" , (nip,))
                datalogin= cur.fetchone()
            elif datalogin[2]=='karu':
                cur.execute("SELECT login.nip,login.role, karu.nama,karu.email,karu.alamat,karu.no_hp FROM login INNER JOIN karu ON login.nip = karu.nip WHERE login.nip = %s " , (nip,))
                datalogin= cur.fetchone()
            else:
                return "maaf nip tida ada"
            session['loggedin'] = True
            session['id'] = datalogin[0]
            session['role'] = datalogin[1]
            session['username'] = datalogin[2]
            session['time'] = tanggal
            cur.close()
        return redirect(url_for('input_dokter'))
class apilogoutdokter(Resource):
    def post(self):
        session.pop('loggedin', None)
        session.pop('id', None)
        session.pop('username', None)
        return redirect(url_for('input_dokter'))
class apiregisterdokter(Resource):
    def post(self):

        return redirect(url_for('login_dokter'))
#print(generate_password_hash('blabla12'))


#routes
api.add_resource(index, '/', methods=['GET'])
api.add_resource(chat, '/chat', methods=['GET'])
api.add_resource(apitips, '/tips', methods=['GET'])
api.add_resource(login_dokter, '/login_dokter', methods=['GET'])
api.add_resource(input_dokter, '/input_dokter', methods=['GET'])

api.add_resource(apipredict, '/api/v1/model/predict', methods=['GET'])
api.add_resource(apiinputdokter, '/api/v1/dokter/input', methods=['POST'])
api.add_resource(apichatgpt, '/api/v1/chatgpt/predict', methods=['GET'])
api.add_resource(apilogindokter, '/api/v1/dokter/login', methods=['POST'])
api.add_resource(apilogoutdokter, '/api/v1/dokter/logout', methods=['POST'])
api.add_resource(apiregisterdokter, '/api/v1/dokter/register', methods=['POST'])

CORS(app)

from .bert import bert_prediction,random_question
from .scrapping_tips_hidup_sehat import tips