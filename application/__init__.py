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

import pandas as pd
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

# dataset
rules = {("sakit","demam tinggi pada beberapa hari", "sakit pada persendian", "munculnya bintik-bintik merah", "turunnya trombosit secara drastis", "pendarahan"):"DBD",
    ("sakit","nyeri","ulu","hati", "nyeri ulu hati","mual", "muntah", "muntah setelah makan"):"maag atau sindrom dispepsia",
    ("sakit","diare","buang air besar lebih sering dari biasanya", "feses yang lebih encer dari biasanya", "mual", "muntah berulang kali","nyeri perut"):"Muntaber",
    ("sakit","bintik kemerahan di kulit","bintik", "bintik kemerahan","bintik merah","bintik kemerahan di kulit yang menggelembung","kulit yang menggelembung","bintik kemerahan di kulit tidak menggelembung" ,"bintik kemerahan di kulit yang melepuh" ,"bintik kemerahan di kulit yang terasa gatal"):"Cacar air",
    ("sakit","demam","suhu tubuh naik secara bertahap","menggigil"):"Tifus",
    ("sakit","naiknya suhu tubuh", "batuk", "nyeri tenggorokan", "nyeri otot", "hingga ruam pada kulit"):"Campak",
    ("sakit","demam", "batuk", "nyeri tenggorokan", "hidung berair", "hidung tersumbat", "sakit kepala","kepala", "mudah lelah","masuk angin","masuk","angin"):"influenza",
    ("sakit","demam","menggigil","nyeri kepala" ,"Rasa lelah" ,"nyeri otot" ",Batuk berdahak", "Kesulitan bernapas" ,"mual","muntah", "demam tinggi", "nyeri kepala" ,"rasa lemah"):"PES / Pesteurellosis",
    ("sakit","diare ringan","diare berat", "diare encer secara tiba-tiba", "tanpa rasa sakit","tanpa muntah-muntah", "dehidrasi" ,"rasa haus yang hebat", "kram otot", "penurunan produksi air kemih", "badan terasa sangat lemah", "mata menjadi cekung","kulit jari-jari tangan mengeriput"):"Kolera",
    ("demam tinggi", "38","derajat","celcius","dada terasa sakit dan sulit bernapas","penurunan nafsu makan","berkeringat","menggigil","detak jantung terasa cepat"):"pneumonia",
    ("apa itu dbd","dbd","demam berdarah",""):"DBD adalah penyakit menular yang disebabkan oleh virus dengue yang dibawa oleh nyamuk Aedes aegeypti Betina. Gejala yang umum terjadi adalah demam tinggi pada beberapa hari, sakit pada persendian, munculnya bintik-bintik merah, turunnya trombosit secara drastis, dan bisa terjadi pendarahan",
    ("maag atau sindrom dispepsia","maag","sindrom dispepsia","dispepsia"):"maag matau sindrom dispepsia adalah penyakit yang mempunyai gejala nyeri ulu hati, mual, dan muntah setelah makan cara mengatasinya : Makan secara perlahan, dalam porsi yang kecil Batasi konsumsi makanan pedas dan berlemak, Kurangi minuman berkafein, Hindari obat-obatan yang menyebabkan nyeri lambung, Anda juga bisa mengkonsumsi obat penetraalisir maag seperti Promag, mylanta, polysilane dst. Promag dijual secara bebas dan tersedia dalam bentuk tablet kunyah serta suspensi cair",
    ("muntaber",):"Muntaber adalah penyakit yang mempunyai gejala diare (buang air besar lebih sering dari biasanya dan ditandai dengan kondisi feses yang lebih encer dari biasanya), mual, muntah berulang kali, dan nyeri perut,Cara mengatasi : muntaber yang dapat dilakukan dengan mudah adalah terapi rehidrasi dengan cara mengonsumsi banyak cairan terutama air putih. Sementara untuk balita dan anak-anak, pemakaian oralit mungkin bisa langsung diberikan untuk menggantikan cairan yang hilang. Kenapa harus oralit? Karena air biasa tidak memiliki kandungan garam dan nutrisi yang cukup untuk menggantikan cairan yang hilang.Jika diperlukan, dokter biasanya akan meresepkan antibiotika jenis metronidazol yang dikombinasikan dengan sulfametoksazol dan trimetoprim. Obat diare lainnya yang bisa digunakan adalah probiotik. Probiotik bisa digunakan untuk mengobati diare dengan cara melawan bakteri jahat penyebab diare",
    ("cacar air","cacar"):"Cacar air adalah penyakit yang mempunyai gejala bintik kemerahan di kulit yang menggelembung maupun tidak, melepuh, dan terasa gatal.Melakukan vaksinasi cacar air, Menjaga kebersihan diri sendiri, pakaian, dan lingkungan, Mengkonsumsi makanan bergizi, Menghindari sumber penularan cacar air.",
    ("tifus","tipes"):"Tifus adalah penyakit yang mempunyai gejala demam yang suhunya naik secara bertahap hingga membuat pendeita menggigil. cara mengatasinya : Memastikan kebersihan bahan makanan sebelum memasaknya, Mencuci tangan secara teratur, terutama sebelum dan setelah makanan, Membersihkan luka dan segera mengobatinya, Hindari jajan di pinggir jalan yang terlihat tidak higienis, Menjaga daya tahan tubuh, Memakan yang tinggi protein, rendah serat, lunak, tidak asam,  dan pedas",
    ("campak",):"Campak adalah penyakit yang mempunyai gejala naiknya suhu tubuh, batuk, nyeri tenggorokan, nyeri otot, hingga ruam pada kulit yang muncul sekitar 7-14 hari setelah terinfeksi virus. Cara Mengatasinya: Melakukan vaksinasi ketika masih usia balita.",
    ("influenza","flu"):"influenza adalah penyakit yang mempunyai gejala demam, batuk, nyeri tenggorokan, hidung berair, hidung tersumbat, sakit kepala, mudah lelah. ",
    ("pneumonia","radang paru-paru","radang paru paru","paru paru radang","paru-paru radang"):"Pneumonia atau radang paru-paru adalah penyakit yang mempunyai gejala.cara mengatasinya : Menjaga daya tahan tubuh agar tidak mudah terserang virus. Misalnya dengan makan teratur, istirahat yang cukup, minum air putih sesuai kebutuhan, berolah raga, dan memiliki gaya hidup yang sehat.Selain itu, menjaga daya tahan tubuh juga dapat juga didukung dengan asupan vitamin terutama Vitamin C yang bisa didapatkan di buah-buahan maupun vitamin yang dijual di toko-toko.Pencegahan lainnya adalah dengan menggunakan masker ditempat umum, terutama bagi yang menderita influenza",
    ("PES / Pesteurellosis","pes","pestaurellosis"):"PES atau yang juga dikenal dengan Pesteurellosis adalah penyakit yang mempunyai gejala demam dan menggigil yang tiba-tiba nyeri kepala Rasa lelah nyeri otot batuk, dengan dahak yang disertai darah kesulitan bernapas Mual dan muntah demam tinggi nyeri kepala rasa lemah . cara mengatasinya : Penanganan terhadap penyakit pes membutuhkan perawatan inap di rumah sakit. Dokter akan meresepkan antibiotik untuk membunuh bakteri, serta obat-obatan lain sesuai dengan tanda dan gejala yang dialami oleh penderita tersebut",
    ("kolera",):"Kolera adalah penyakit yang mempunyai gejala bervariasi, mulai dari diare ringan sampai diare berat yang bisa berakibat fatal. Dalam beberapa kasus, orang yang terinfeksi justru tidak menunjukkan gejala apa pun, diare encer seperti air yang terjadi secara tiba-tiba, tanpa rasa sakit dan muntah-muntah, dehidrasi disertai rasa haus yang hebat, kram otot, penurunan produksi air kemih, sehingga badan terasa sangat lemah, mata menjadi cekung dan kulit jari-jari tangan mengeriput cara mengatasinya : memperbanyak asupan cairan untuk mencegah dehidrasi akibat kolera Bila dehidrasi sudah diatasi, tujuan pengobatan selanjutnya adalah untuk menggantikan jumlah cairan yang hilang karena diare dan muntah. Pengobatan awal dengan tetrasiklin atau antibiotik lainnya bisa membunuh bakteri dan biasanya akan menghentikan diare dalam 48 jam.Bila berada di daerah resisten dengan wabah kolera atau Vibrio cholerae, dapat digunakan furozolidone. Makanan padat bisa diberikan setelah muntah-muntah berhenti dan nafsu makan sudah kembali.Pencegahan: Untuk mencegah kolera, penting untuk melakukan penjernihan cadangan air dan pembuangan tinja yang memenuhi standar. Selain itu, minumlah air yang sudah terlebih dahulu dimasak. Hindari mengonsumsi sayuran mentah atau ikan dan kerang yang tidak dimasak sampai matang.Pemberian antibiotik tetrasiklin juga bisa membantu mencegah penyakit pada orang-orang yang sama-sama menggunakan perabotan rumah dengan penderita kolera. Sementara itu, vaksinasi kolera tidak terlalu dianjurkan karena perlindungan yang diberikan tidak menyeluruh"
}

raw1 = ["DBD (Demam Berdarah Dengue): Penyakit menular disebabkan oleh virus dengue yang dibawa oleh nyamuk Aedes aegeypti Betina. Gejalanya meliputi demam tinggi, sakit persendian, bintik-bintik merah, penurunan trombosit, dan mungkin pendarahan.",
"Maag atau Sindrom Dispepsia: Penyakit dengan gejala nyeri ulu hati, mual, dan muntah setelah makan. Pengobatannya meliputi makan perlahan, menghindari makanan pedas dan berlemak, serta penggunaan obat maag seperti Promag.",
"Muntaber (Diare): Penyakit dengan gejala diare, mual, muntah, dan nyeri perut. Pengobatannya termasuk rehidrasi dengan mengonsumsi banyak cairan dan, jika diperlukan, antibiotik.",
"Cacar Air: Penyakit dengan gejala bintik-bintik kemerahan di kulit yang menggelembung, melepuh, dan gatal. Pencegahannya meliputi vaksinasi dan menjaga kebersihan diri dan lingkungan.",
"Tifus: Penyakit dengan gejala demam, menggigil, dan penurunan trombosit. Cara mengatasi meliputi menjaga kebersihan makanan, mencuci tangan, dan menjaga daya tahan tubuh.",
"Campak: Penyakit dengan gejala demam, batuk, nyeri tenggorokan, dan ruam kulit. Pengobatan melibatkan vaksinasi.",
"Influenza: Penyakit dengan gejala demam, batuk, nyeri tenggorokan, hidung berair, dan lainnya. Umumnya diobati dengan istirahat dan cairan.",
"Pneumonia (Radang Paru-Paru): Penyakit dengan gejala seperti demam, batuk, dan sulit bernapas. Pengobatannya melibatkan antibiotik dan menjaga daya tahan tubuh.",
"PES (Pesteurellosis): Penyakit dengan gejala demam, nyeri kepala, lelah, dan lainnya. Penanganannya melibatkan antibiotik.",
"Kolera: Penyakit dengan gejala diare berat, dehidrasi, dan lainnya. Pengobatan melibatkan pemberian cairan dan antibiotik, sementara pencegahannya termasuk penjernihan air dan pengolahan tinja.",
"Rumah Sakit terdekat => https://www.google.com/maps/search/Rumah_sakit/ ",
"Puskesmas terdekat => https://www.google.com/maps/search/Puskesmas/ ",
"Apotek terdekat => https://www.google.com/maps/search/Apotek/ ",
"Tempat pijat / urut disekitar anda => https://www.google.com/maps/search/Urut/ "]

list_penyakit = ["DBD (Demam Berdarah Dengue)","Maag","Muntaber (Diare)","Cacar Air",
"Tifus","Campak","Influenza","Pneumonia (Radang Paru-Paru)","PES (Pesteurellosis)","Kolera"]
#contorller

#routes

#add to api doc
@app.route("/")
def index():
        '''
        Get method represents a landing page for haisus.site
        '''
        #print(generate_password_hash('blabla12'))
       
        return Response(render_template("landingpage.html"),mimetype='text/html')
@app.route('/chat', methods=['GET'])
def chat():
        cur = mysql.connection.cursor()
        cur.execute("SELECT nama_penyakit,' adalah penyakit yang mempunyai gejala ', gejala from input_dokter")
        fromdb= cur.fetchall()
        for x in fromdb:
            # raw1.append(x)
            list_penyakit.append(x[0])
            list_string = x[2].split(",")
            filter_String = []
            for string in list_string:
                new_string = string.strip() 
                new_string = string.lower() 
                filter_String.append(new_string)
            rules[tuple(filter_String)]=str(x[0])
        
        return Response(render_template('index.html'),mimetype='text/html')
@app.route('/chat_pilih_context', methods=['GET'])
def chat2():
        cur = mysql.connection.cursor()
        cur.execute("SELECT nama_penyakit,' adalah penyakit yang mempunyai gejala ', gejala from input_dokter")
        fromdb= cur.fetchall()
        for x in fromdb:
            raw1.append(x)
            list_penyakit.append(x[0])
            list_string = x[2].split(",")
            filter_String = []
            for string in list_string:
                new_string = string.strip() 
                new_string = string.lower() 
                filter_String.append(new_string)
            rules[tuple(filter_String)]=str(x[0])
        print(list_penyakit)
        return Response(render_template('chatbot_pilih_context.html',raw1=raw1,len= len(list_penyakit),list_penyakit=list_penyakit),mimetype='text/html')
@app.route('/api/v1/model/predict', methods=['GET'])
def apipredict():
        question = request.args.get('pertanyaan')
        print(question)
        cur = mysql.connection.cursor()
        # cur.execute("SELECT nama_penyakit,' adalah penyakit yang mempunyai gejala ', gejala from input_dokter")
        # fromdb= cur.fetchall()
        # for x in fromdb:
        #     raw1.append(x[0]+x[1]+x[2])
        prediction = bert_prediction(raw1,str(question.lower()))
        print(prediction)
        return prediction

@app.route('/api/v2/model/predict', methods=['GET'])
def apipredict2():
        question = request.args.get('pertanyaan')
        id = request.args.get('id_context')
        cur = mysql.connection.cursor()
        cur.execute("SELECT nama_penyakit,' adalah penyakit yang mempunyai gejala ', gejala from input_dokter")
        fromdb= cur.fetchall()
        for x in fromdb:
            raw1.append(x)
        print(id)
        context = raw1[int(id)]
        print(question)
        prediction = bert_prediction_pilih_context(context,str(question.lower()))
        print(prediction)
        return prediction
@app.route('/tips', methods=['GET'])
def apitips():
        respon = tips()
        title = respon[0]['title']
        sumber = respon[0]['sumber']
        data = respon[0]['isi']
        return Response(render_template('tips.html',title=title,data=data,sumber=sumber),mimetype='text/html')
@app.route('/input_dokter', methods=['GET'])
@required_login
def input_dokter():
        return Response(render_template("inputdokter.html"),mimetype='text/html')
@app.route('/api/v1/dokter/input', methods=['POST'])
@required_login
def apiinputdokter():
        cur = mysql.connection.cursor()
        response = {}
        id_dokter = request.json['id_dokter']
        print(id_dokter)
        nama_penyakit = request.json['nama_penyakit']
        print(nama_penyakit)
        gejala = request.json['gejala']
        print(gejala)
        pencegahan = request.json['pencegahan']
        print(pencegahan)
        rujukan = request.json['rujukan']
        print(rujukan)
        cur.execute("INSERT INTO input_dokter(id_dokter,nama_penyakit,gejala,pencegahan,rekomendasi_rujukan) VALUES(%s,%s,%s,%s,%s)" , (id_dokter,nama_penyakit.lower(),gejala.lower(),pencegahan,rujukan))
        mysql.connection.commit()
        response.update({"status": "sukses","msg":"Data Berhasil Diinputkan"})
        return response
@app.route('/input_artikel', methods=['GET'])
def input_url():
        return Response(render_template("inputartikel.html"),mimetype='text/html')
@app.route('/input_artikel', methods=['POST'])
@required_login
def apiinputurl():
        cur = mysql.connection.cursor()
        response = {}
        id_dokter = request.json['id_dokter']
        print(id_dokter)
        url = request.json['url']
        print(url)
        nama = request.json['nama']
        print(nama)
        cur.execute("INSERT INTO artikel(url,nama) VALUES(%s,%s)" , (url,nama))
        mysql.connection.commit()
        response.update({"status": "sukses","msg":"Data Berhasil Diinputkan"})
        return response
@app.route('/api/v1/chatgpt/predict', methods=['GET'])
def apichatgpt():
        question = request.args.get('pertanyaan')
        print(question)
        response = random_question(question)
        print(response)
        return response
        
@app.route('/login_dokter', methods=['GET'])
def login_dokter():
        if 'loggedin' in session:
            return redirect(url_for('input_dokter'))
        else: 
            return Response(render_template("login.html"),mimetype='text/html')
@app.route('/api/v1/dokter/login', methods=['POST'])
def apilogindokter():
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
            flash('maaf username tidak ada')
            return redirect(url_for('login_dokter',alert="maaf username tidak ada"))
        elif not check_password_hash(datalogin[3],password):
            cur.close()
            flash("maaf password salah")
            return redirect(url_for('login_dokter',alert="maaf password salah"))
        else:
            session['loggedin'] = True
            session['id'] = datalogin[0]
            session['role'] = datalogin[1]
            session['username'] = datalogin[2]
            session['time'] = tanggal
            cur.close()
        return redirect(url_for('input_dokter'))
@app.route('/api/v1/dokter/register', methods=['POST'])
def apiregisterdokter():
        save = store()
        if save == True:
            return redirect(url_for('verifikasi',email=request.form['email']))
        else:
            return redirect(url_for('login_dokter',msg="email sudah ada"))

#print(generate_password_hash('blabla12'))
@app.route('/api/v1/dokter/logout', methods=['GET'])
def apilogoutdokter():
        session.pop('loggedin', None)
        session.pop('id', None)
        session.pop('role', None)
        session.pop('username', None)
        session.pop('time', None)
        return redirect(url_for('login_dokter'))
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
CORS(app)
from .bert import bert_prediction,random_question, bert_prediction_pilih_context
from .rule_based import rules_prediction
from .scrapping_tips_hidup_sehat import tips