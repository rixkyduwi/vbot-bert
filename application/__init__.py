from functools import wraps
import json
from time import time
import time
from flask import Response, Flask,request, render_template, redirect,url_for, session,flash,get_flashed_messages
from werkzeug.security import check_password_hash, generate_password_hash
from flask_restful import Resource, Api,fields, marshal_with
from flask_mysqldb import MySQL
from flask_cors import CORS
import datetime
from time import time
import time
from dotenv import load_dotenv
load_dotenv()
import os
from flask_mail import Mail, Message

app = Flask(__name__)
api = Api(app)
app.config['MYSQL_HOST']= os.environ.get('MYSQL_HOST')
app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER')
app.config['MYSQL_PASSWORD']  = os.environ.get('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB')

app.config['SECRET_KEY'] = "yang tau tau aja"

#=====================CREATE API DOC====================================================
from flask_apispec import marshal_with,use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import Schema, fields
class HaisusRequestSchema(Schema):
    api_type = fields.String(required=True, description="API type of Haisus API")
class HaisusResponseSchema(Schema):
    message = fields.Str(default='response answer')
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec

app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Haisus Open Api',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON 
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
})
docs = FlaskApiSpec(app)

#================================Permission Send Email==================================
app.config['MAIL_SERVER'] = str(os.environ.get("MAIL_SERVER"))
app.config['MAIL_PORT']= str(os.environ.get("MAIL_PORT"))
app.config['MAIL_USERNAME'] = str(os.environ.get("MAIL_USERNAME"))
app.config['MAIL_PASSWORD'] = str(os.environ.get("MAIL_PASSWORD"))
app.config['MAIL_USE_TLS']= True
app.config['MAIL_USE_SSL']= False
app.config['MAIL_SERVER'] = str(os.environ.get("MAIL_SERVER"))
app.config['MAIL_PORT']= str(os.environ.get("MAIL_PORT"))
app.config['MAIL_USERNAME'] = str(os.environ.get("MAIL_USERNAME"))
app.config['MAIL_PASSWORD'] = str(os.environ.get("MAIL_PASSWORD"))
app.config['MAIL_USE_TLS']= True
app.config['MAIL_USE_SSL']= False

mysql = MySQL(app)
mail = Mail(app)
import random,string

def kode_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
def store():
    try:
        name = request.form['name']
        email = request.form['email']
        print(email)
        password = request.form['password']
        password = generate_password_hash(password)
        kode = kode_generator()
        pesan = "here is your confirmation code: "+kode
        status = "not active"
        cur = mysql.connection.cursor()
        cur.execute("SELECT email from login" )
        emails = cur.fetchall()
        for i in emails:
            print(i[0])
            if email == i[0] :
                return False
        cur.execute("INSERT INTO login(`username`, `email`, `password`, `status`, `kode`) VALUES(%s,%s,%s,%s,%s)",(name,email,password,status,kode))
        mysql.connection.commit()
        msg = Message("Hello, {} welcome to Chatbot deteksi penyakit berdasarkan gejala".format(name),
                      sender="haysus.cs@mail.com")
        msg.add_recipient(email)
        # msg.body = "testing"
        msg.html = render_template('template_email.html', app_name="Haisus", app_contact="haysus.cs@mail.com",
                                   name=name, email=email,pesan=pesan)
        mail.send(msg)

        return True

    except Exception as e:
        print(e)
#login session
def required_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        print(func(*args, **kwargs))
        print(session)
        if 'username' not in session:
            # Jika pengguna belum login, redirect ke halaman login
            return redirect(url_for('login_dokter'))
        # Jika pengguna sudah login, izinkan akses ke fungsi yang dituju
        return func(*args, **kwargs)
    return decorated_function

#contorller
class index(MethodResource,Resource):


    def get(self):
        '''
        Get method represents a landing page for haisus.site
        '''
        #print(generate_password_hash('blabla12'))
        now = datetime.datetime.now()
        first_day = datetime.datetime(now.year,now.month,27)
        formatted_first_day = first_day.strftime("%Y-%m-%d")
        today = datetime.datetime(now.year,now.month,now.day)
        formatted_today = today.strftime("%Y-%m-%d")
        print(str(formatted_today))
        if formatted_today == formatted_first_day :
            from .train_nlp_cnn import retraining
            print("retraining")
            retraining()
        else:
            None
        return Response(render_template("landingpage.html"),mimetype='text/html')
class chat(MethodResource,Resource):


    def get(self):
        return Response(render_template('index.html'),mimetype='text/html')
class apipredict(MethodResource,Resource):


    def get(self):
        question = request.args.get('pertanyaan')
        print(question)
        prediction = bert_prediction(str(question))
        print(prediction)
        return prediction
class apitips(MethodResource,Resource):


    def get(self):
        respon = tips()
        title = respon[0]['title']
        sumber = respon[0]['sumber']
        data = respon[0]['isi']
        return Response(render_template('tips.html',title=title,data=data,sumber=sumber),mimetype='text/html')

class input_dokter(MethodResource,Resource):
    @required_login


    def get(self):
        return Response(render_template("inputdokter.html"),mimetype='text/html')
class apiinputdokter(MethodResource,Resource):
    @required_login


    def post(self):
        cur = mysql.connection.cursor()
        response = {}
        id_dokter = request.form['id_dokter']
        print(id_dokter)
        nama_penyakit = request.form['nama_penyakit']
        print(nama_penyakit)
        gejala = request.form['gejala']
        print(gejala)
        pencegahan = request.form['pencegahan']
        print(pencegahan)
        rujukan = request.form['rujukan']
        print(rujukan)
        cur.execute("INSERT INTO input_dokter(id_dokter,nama_penyakit,gejala,pencegahan,rekomendasi_rujukan) VALUES(%s,%s,%s,%s,%s)" , (id_dokter,nama_penyakit,gejala,pencegahan,rujukan))
        mysql.connection.commit()
        response.update({"status": "sukses","msg":"Data Berhasil Diinputkan"})
        return redirect(url_for('input_dokter'))
class input_url(MethodResource,Resource):


    def get(self):
        return Response(render_template("inputartikel.html"),mimetype='text/html')
class apiinputurl(MethodResource,Resource):
    @required_login


    def post(self):
        cur = mysql.connection.cursor()
        response = {}
        id_dokter = request.form['id_dokter']
        print(id_dokter)
        url = request.form['url']
        print(url)
        cur.execute("INSERT INTO input_url(id_dokter,url) VALUES(%s,%s)" , (id_dokter,url))
        mysql.connection.commit()
        response.update({"status": "sukses","msg":"Data Berhasil Diinputkan"})
        return redirect(url_for('index'))
class apichatgpt(MethodResource,Resource):


    def get(self):
        question = request.args.get('pertanyaan')
        print(question)
        response = random_question(question)
        print(response)
        return response

class login_dokter(MethodResource,Resource):


    def get(self):
        if 'loggedin' in session:
            return redirect(url_for('input_dokter'))
        else: 
            return Response(render_template("login.html"),mimetype='text/html')
class apilogindokter(MethodResource,Resource):


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
        elif not check_password_hash(datalogin[3],password):
            cur.close()
            return redirect(url_for('login_dokter',alert="maaf password salah"))
        else:
            session['loggedin'] = True
            session['id'] = datalogin[0]
            session['role'] = datalogin[1]
            session['username'] = datalogin[2]
            session['time'] = tanggal
            cur.close()
        return redirect(url_for('input_dokter'))

class apiregisterdokter(MethodResource,Resource):


    def post(self):
        save = store()
        if save == True:
            return redirect(url_for('verifikasi',email=request.form['email']))
        else:
            return redirect(url_for('login_dokter',msg="email sudah ada"))

#print(generate_password_hash('blabla12'))
class apilogoutdokter(MethodResource,Resource):

    def get(self):
        session.pop('loggedin', None)
        session.pop('id', None)
        session.pop('role', None)
        session.pop('username', None)
        session.pop('time', None)
        return redirect(url_for('login_dokter'))


#herbalia
# @app.route('/herbalia_scan', methods=['POST'])
# def scann():
#     from application.herbalia_scan import scan
#     response = scan()
#     return response
# @app.route('/herbalia_chatbot', methods=['POST'])
# def chatbott():
#     from application.herbalia_chatbot import bert_predictionn
#     response = bert_predictionn()
#     return response

#verifikasi email
@app.route('/redi')
def redi():
    email = "emil@mal.co"
    return redirect(url_for('verifikasi', email=email))
@app.route('/verifikasi',methods=['GET','POST'])
def verifikasi():
    if request.method == 'GET':
        return render_template('verif.html')
    elif request.method == 'POST':
        kode = request.form['kode']
        email = request.args['email']
        cur = mysql.connection.cursor()
        cur.execute('SELECT COUNT(*) FROM login where email= %s and kode = %s',(email,kode))
        data = cur.fetchone()
        print(data[0])
        if data[0]==1:
            cur.execute("UPDATE login set status=%s, kode=''  where email= %s",('terverifikasi',email))
            return redirect(url_for('login_dokter',msg="email berhasil terferivikasi"))
        else:
            return redirect(url_for('verifikasi',email=email,msg='maaf kode salah'))

@app.route('/send-reset')
def sendreset():
    try:
        from urllib import unquote
    except ImportError:
        from urllib.parse import unquote
    email = unquote(request.args['email'])
    print(str(email))
    kode= kode_generator()
    link = request.base_url+"/reset"
    pesan = "here is your reset link = <a href='"+link+"'> "+link+"</a>"
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM login WHERE `email` = %s",(str(email),))
    data = cur.fetchone()
    cur.execute("UPDATE login SET `kode` = %s WHERE `email` = %s",(kode,str(email),))
    mysql.connection.commit()
    name = data[1]

    msg = Message("Hello, {} welcome to Chatbot deteksi penyakit berdasarkan gejala".format(name),
                      sender="haysus.cs@mail.com")
                      
    msg.add_recipient(email)
    # msg.body = "testing"

    msg.html = render_template('template_email.html', app_name="Haisus", app_contact="haysus.cs@mail.com",
                               name=name, email=email,pesan=pesan)
    mail.send(msg)
    return redirect(url_for('login_dokter',msg="reset link sent"))

@app.route('/reset')
def reset():
    kode = request.args['kode']
    email = request.args['email']
    cur = mysql.connection.cursor()
    cur.execute('SELECT COUNT(*) FROM login where email= %s and kode = %s',(email,kode))
    data = cur.fetchone()
    print(data[0])
    if data[0]==1:
        return render_template('reset.html')
    else:
        return render_template('403.html')
@app.route('/aksireset/<email>',methods=['POST'])
def aksireset(email):
    email = request.form['email']
    kode = request.form['kode']
    password = request.form['password']
    cur = mysql.connection.cursor()
    cur.execute('SELECT COUNT(*) FROM login where email= %s and kode = %s',(email,kode))
    data = cur.fetchone()
    print(data[0])
    if data[0]==1:
        password= generate_password_hash(password)
        cur.execute("UPDATE login set password=%s, kode=''  where email= %s",('',email))
        mysql.connection.commit()
        return redirect(url_for('reset_password'))
    else:
        return redirect(url_for('reset',email=email,msg='maaf kode salah'))
@app.route('/tambahqna',methods=['GET','POST'])
@required_login
def tambahqna():
    if request.method=='GET':
        return render_template('tambahqna.html')
    elif request.method=='POST':
        flash('berhasil tambah data"')
        return redirect(url_for('tambahqna',msg="berhasil tambah data"))
@app.route('/insert_data',methods=['GET','POST'])
def insert_data():
    if request.method=='GET':
        cur = mysql.connection.cursor()
        cur.execute("SELECT patterns,response FROM datalatih")
        cur.fetchall()
        return "berhasil menambahkan data ke data latih"

    elif request.method=='POST':
        patterns = request.form['patterns']
        patterns = patterns.split(",")
        responses = request.form['responses']
        responses = responses.split(",")
        cur = mysql.connection.cursor()
        cur.execute("SELECT patterns,response FROM datalatih")
        with open('/modelnlp/modelnlp/knowledge.json', "r+") as f:
            data_file = open('/modelnlp/modelnlp/knowledge.json').read()
            intents = json.loads(data_file)
            rand=''.join(random.choice(string.ascii_lowercase) for i in range(4))
            y = {"tag": rand,
                "patterns": patterns,
                "responses": responses,
                "context": [""]
                }

            intents['intents'].append(y)
            with open('/modelnlp/modelnlp/knowledge.json', "w+") as k:
                json.dump(intents,k)
        flash('berhasil tambah data"')
        return redirect(url_for('tambahqna',msg="berhasil tambah data")) 
import numpy as np
import os
import pickle
import random
import pickle
import json
import nltk
from keras.models import load_model
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
import re
model = load_model("chatbotdnn/chatbot_model.h5")
intents = json.loads(open("chatbotdnn/intents.json").read())
words = pickle.load(open("chatbotdnn/words.pkl", "rb"))
classes = pickle.load(open("chatbotdnn/classes.pkl", "rb"))
@app.route('/dnn/tambahChatbot', methods = ['POST'])
def tambahdataChatbot():
    cur = mysql.connection.cursor()

    name_patterns = request.form['Patterns']
    
    name_patterns = name_patterns.split(",")
    print(name_patterns)
    desk_responses = request.form['Responses']
    desk_responses = desk_responses.split(",")
    print(desk_responses)
    cur.execute("insert into chatbot (patterns,responses) values(%s,%s)",(str(name_patterns),str(desk_responses)))
    mysql.connection.commit()
    cur.close()
    chatbot_directory = os.path.abspath(os.path.join(__file__, "../../chatbotdoni/intents.json")) 
    with open(chatbot_directory, "r+") as f:
        inten = json.loads(f.read())
        import uuid,string
        letters = string.ascii_lowercase
        rando = ''.join(random.choice(letters) for i in range(4))
        y = {"tag":str(rando),
            "patterns": name_patterns,
            "responses": desk_responses,
            "context": [""]
            }
        inten['intents'].append(y)
        
        with open(chatbot_directory, "w+") as k:
            json.dump(inten,k)
        
    from retraining import retraining
    retraining()

    return "done"

@app.route("/dnn/get", methods=["POST"])
def chatbot_response():
    msg = request.form["msg"]
    print(msg)
    if msg.startswith('my name is'):
        name = msg[11:]
        ints = predict_class(msg, model)
        res1 = getResponse(ints, intents)
        res =res1.replace("{n}",name)
    elif msg.startswith('hi my name is'):
        name = msg[14:]
        ints = predict_class(msg, model)
        res1 = getResponse(ints, intents)
        res =res1.replace("{n}",name)
    else:
        print("jln")
        ints = predict_class(msg, model)
        print(ints)
        res = getResponse(ints, intents)
    return res

def clean_up_sentence(sentence):
    import nltk
    nltk.download('popular')
    from nltk.stem import WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    print(sentence_words)
    return sentence_words

def bow(sentence, words, show_details=True):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    print(bag)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return np.array(bag)

def predict_class(sentence, model):
    p = bow(sentence, words, show_details=False)
    print(p)
    res = model.predict(np.array([p]))[0]
    print(res)
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    if res == []:
        return_list.append({"intent": "error", "probability": 0})
    else:
        for r in results:
            return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    print(return_list)
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]["intent"]
    list_of_intents = intents_json["intents"]
    for i in list_of_intents:
        print(tag)
        print(i['tag'])
        if i["tag"] == tag:
            result = random.choice(i["responses"])
            break
        else:
            result = "Maaf saya tidak bisa menjawab"
    return result
#routes
api.add_resource(index, '/', methods=['GET'])
api.add_resource(chat, '/chat', methods=['GET'])
api.add_resource(apitips, '/tips', methods=['GET'])
api.add_resource(login_dokter, '/login_dokter', methods=['GET'])
api.add_resource(input_dokter, '/input_dokter', methods=['GET'])
api.add_resource(input_url, '/input_artikel', methods=['GET'])
api.add_resource(apipredict, '/api/v1/model/predict', methods=['GET'])
api.add_resource(apiinputdokter, '/api/v1/dokter/input', methods=['POST'])
api.add_resource(apichatgpt, '/api/v1/chatgpt/predict', methods=['GET'])
api.add_resource(apilogindokter, '/api/v1/dokter/login', methods=['POST'])
api.add_resource(apilogoutdokter, '/api/v1/dokter/logout', methods=['GET'])
api.add_resource(apiregisterdokter, '/api/v1/dokter/register', methods=['POST'])
#add to api doc
docs.register(index)
docs.register(chat)
docs.register(apitips)
docs.register(login_dokter)
docs.register(input_dokter)
docs.register(input_url)
docs.register(apipredict)
docs.register(apiinputdokter)
docs.register(apichatgpt)
docs.register(apilogindokter)
docs.register(apilogoutdokter)
docs.register(apiregisterdokter)
CORS(app)



from .bert import bert_prediction,random_question
from .scrapping_tips_hidup_sehat import tips