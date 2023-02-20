import random,string,json
from certifi import where
from flask import Flask,jsonify, request, render_template
from werkzeug.security import check_password_hash,generate_password_hash
from flask_restful import Resource, Api
from flask_httpauth import HTTPTokenAuth
from flask_mysqldb import MySQL 
from flask_cors import CORS
import torch,time,numpy as np
from flask import Flask,jsonify
from transformers import BertTokenizerFast, BertForQuestionAnswering, Trainer, TrainingArguments
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
db = SQLAlchemy()
mysql = MySQL()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vbot_bert.db'
app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD']  = ''
app.config['MYSQL_DB'] = 'halosus'
class HISTORY(db.Model):
    id = db.Column(db.Integer, primary_key=True) # kudu ana primary key
    nama = db.Column(db.String(100))
    pertanyaan = db.Column(db.String(1000))
    jawaban = db.Column(db.String(1000))
    score = db.Column(db.String(100))
    waktu_proses = db.Column(db.String(100))
db.init_app(app)  
device = "cuda" if torch.cuda.is_available() else "cpu" 
torch.device(device) 
modelCheckpoint = "indolem/indobert-base-uncased"
model = BertForQuestionAnswering.from_pretrained("model")
tokenizer = BertTokenizerFast.from_pretrained(modelCheckpoint)
start_time = time.time()
auth = HTTPTokenAuth(scheme='Bearer')
api = Api(app)
class ADMIN(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    token = db.Column(db.String(1000))
app.app_context().push()
db.init_app(app)
@auth.verify_token
def verify_token(token):
    user=ADMIN.query.filter_by(token=token).first() 
    return user.name
class apisignup(Resource):
    def post(self):
        email = request.json['email']
        name = request.json['name']
        password = request.json['password']
        admin = ADMIN(email=email,name=name,password=generate_password_hash(password),token= '')
        db.session.add(admin)
        db.session.commit()
        return jsonify({"msg" : "registrasi sukses","status":200})
class apilogin(Resource):
    def post(self):
        email = request.json['email']
        password = request.json['password']
        j=15
        user= ADMIN.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return jsonify({"msg":"login gagal","url": "/login","status":200})
        token = ''.join(random.choices(string.ascii_uppercase + string.digits, k = j))
        user.token= token
        db.session.commit()
        return jsonify({"msg":"login sukses, hai "+user.name,"token":token,"url": "/dashboard", "status":200})
class apipredict(Resource):
    def get(self):
        question = request.args.get('pertanyaan')
        print(question)
        prediction = bert_prediction(str(question))
        return prediction
class apihistory(Resource):
    @auth.login_required
    def get(self):
        histories = HISTORY.query.filter_by(nama=auth.current_user()).first()
        output = [
            {
                "nama":history.nama,
                "konteks":history.konteks, 
                "pertanyaan":history.pertanyaan,  
                "rank":history.rank, 
                "jawaban":history.jawaban,  
                "score":history.score, 
                "waktu_proses":history.waktu_proses
            } 
            for history in histories ]
        response = {
            "code" : 200, 
            "msg"  : "Query data sukses",
            "data" : output}
        return response, 200
@app.route("/")
def index():
    return render_template("landingpage.html")
@app.route("/chat")
def chat():
    return render_template("index.html")
api.add_resource(apisignup, '/api/v1/users/create', methods=['POST'])
api.add_resource(apilogin, '/api/v1/users/login', methods=['POST'])
api.add_resource(apipredict, '/api/v1/model/predict', methods=['GET'])
api.add_resource(apihistory, '/api/v1/users/history', methods=['GET'])
mysql.init_app(app)
CORS(app)
mengatasi_maag ="cara mengatasinya : Makan secara perlahan, dalam porsi yang kecil Batasi konsumsi makanan pedas dan berlemak, Kurangi minuman berkafein, Hindari obat-obatan yang menyebabkan nyeri lambung, Anda juga bisa mengkonsumsi obat penetraalisir maag seperti Promag, mylanta, polysilane dst. Promag dijual secara bebas dan tersedia dalam bentuk tablet kunyah serta suspensi cair."
mengatasi_influenza="cara mengatasinya : Menjaga daya tahan tubuh agar tidak mudah terserang virus. Misalnya dengan makan teratur, istirahat yang cukup, minum air putih sesuai kebutuhan, berolah raga, dan memiliki gaya hidup yang sehat.Selain itu, menjaga daya tahan tubuh juga dapat juga didukung dengan asupan vitamin terutama Vitamin C yang bisa didapatkan di buah-buahan maupun vitamin yang dijual di toko-toko.Pencegahan lainnya adalah dengan menggunakan masker ditempat umum, terutama bagi yang menderita influenza."
mengatasi_Muntaber="Cara mengatasi : muntaber yang dapat dilakukan dengan mudah adalah terapi rehidrasi dengan cara mengonsumsi banyak cairan terutama air putih. Sementara untuk balita dan anak-anak, pemakaian oralit mungkin bisa langsung diberikan untuk menggantikan cairan yang hilang. Kenapa harus oralit? Karena air biasa tidak memiliki kandungan garam dan nutrisi yang cukup untuk menggantikan cairan yang hilang.Jika diperlukan, dokter biasanya akan meresepkan antibiotika jenis metronidazol yang dikombinasikan dengan sulfametoksazol dan trimetoprim. Obat diare lainnya yang bisa digunakan adalah probiotik. Probiotik bisa digunakan untuk mengobati diare dengan cara melawan bakteri jahat penyebab diare. "
mengatasi_Cacar_air= "cara mengatasinya : Melakukan vaksinasi cacar air, Menjaga kebersihan diri sendiri, pakaian, dan lingkungan, Mengkonsumsi makanan bergizi, Menghindari sumber penularan cacar air."
mengatasi_Tifus="cara mengatasinya : Memastikan kebersihan bahan makanan sebelum memasaknya, Mencuci tangan secara teratur, terutama sebelum dan setelah makanan, Membersihkan luka dan segera mengobatinya, Hindari jajan di pinggir jalan yang terlihat tidak higienis, Menjaga daya tahan tubuh, Memakan yang tinggi protein, rendah serat, lunak, tidak asam,  dan pedas."
mengatasi_Campak="cara mengatasinya : Melakukan vaksinasi ketika masih usia balita."
mengatasi_Pneumonia="cara mengatasinya : Terapi kausal Terapi ini dilakukan dengan cara pemberian obat antibiotik atau obat antijamur. Terapi suportif umum Penanganan ini disesuaikan dengan keadaan pasien, misalnya ketika pemberian terapi oksigen. Terapi inhalasi Dengan cara menyalurkan obat langsung ke paru-paru, terapi ini sangat bermanfaat pada kondisi pasien yang membutuhkan pengobatan segera. Terapi ini dapat menghindari efek samping yang berkelanjutan, mengencerkan dahak yang kental dan kekuningan, serta mengatasi infeksi. Fisioterapi dada Cara ini dilakukan untuk mempermudah proses pengeluaran dahak dari paru. Meningkatkan daya tahan tubuh sangat penting untuk menghindarkan diri dari pneumonia. Karena itu, jagalah kebersihan diri dengan menerapkan hal-hal berikut dalam keseharian:Rajin mencuci tanganMengenakan masker ketika pergi ke tempat umumBerolahraga secara teratur."
mengatasi_PES="cara mengatasinya : Penanganan terhadap penyakit pes membutuhkan perawatan inap di rumah sakit. Dokter akan meresepkan antibiotik untuk membunuh bakteri, serta obat-obatan lain sesuai dengan tanda dan gejala yang dialami oleh penderita tersebut."
mengatasi_Kolera="cara mengatasinya : memperbanyak asupan cairan untuk mencegah dehidrasi akibat kolera Bila dehidrasi sudah diatasi, tujuan pengobatan selanjutnya adalah untuk menggantikan jumlah cairan yang hilang karena diare dan muntah. Pengobatan awal dengan tetrasiklin atau antibiotik lainnya bisa membunuh bakteri dan biasanya akan menghentikan diare dalam 48 jam.Bila berada di daerah resisten dengan wabah kolera atau Vibrio cholerae, dapat digunakan furozolidone. Makanan padat bisa diberikan setelah muntah-muntah berhenti dan nafsu makan sudah kembali.Pencegahan: Untuk mencegah kolera, penting untuk melakukan penjernihan cadangan air dan pembuangan tinja yang memenuhi standar. Selain itu, minumlah air yang sudah terlebih dahulu dimasak. Hindari mengonsumsi sayuran mentah atau ikan dan kerang yang tidak dimasak sampai matang.Pemberian antibiotik tetrasiklin juga bisa membantu mencegah penyakit pada orang-orang yang sama-sama menggunakan perabotan rumah dengan penderita kolera. Sementara itu, vaksinasi kolera tidak terlalu dianjurkan karena perlindungan yang diberikan tidak menyeluruh."

context="maag atau sindrom dispepsia adalah penyakit yang mempunyai gejala Nyeri ulu hati, mual, dan muntah setelah makan. Muntaber adalah penyakit yang mempunyai gejala diare (buang air besar lebih sering dari biasanya dan ditandai dengan kondisi feses yang lebih encer dari biasanya), mual, muntah berulang kali, dan nyeri perut. Cacar air adalah penyakit yang mempunyai gejala bintik kemerahan di kulit yang menggelembung maupun tidak, melepuh, dan terasa gatal. Tifus adalah penyakit yang mempunyai gejala demam yang suhunya naik secara bertahap hingga membuat pendeita menggigil. Campak adalah penyakit yang mempunyai gejala naiknya suhu tubuh, batuk, nyeri tenggorokan, nyeri otot, hingga ruam pada kulit yang muncul sekitar 7-14 hari setelah terinfeksi virus.influenza adalah penyakit yang mempunyai gejala Demam, batuk, nyeri tenggorokan, hidung berair, hidung tersumbat, sakit kepala, mudah lelah. Pneumonia atau radang paru-paru adalah penyakit yang mempunyai gejala. PES atau yang juga dikenal dengan Pesteurellosis adalah penyakit yang mempunyai gejala demam dan menggigil yang tiba-tiba Nyeri kepala Rasa lelah Nyeri otot Batuk, dengan dahak yang disertai darah Kesulitan bernapas Mual dan muntah Demam tinggi Nyeri kepala Rasa lemah .Kolera adalah penyakit yang mempunyai gejala bervariasi, mulai dari diare ringan sampai diare berat yang bisa berakibat fatal. Dalam beberapa kasus, orang yang terinfeksi justru tidak menunjukkan gejala apa pun, diare encer seperti air yang terjadi secara tiba-tiba, tanpa rasa sakit dan muntah-muntah, dehidrasi disertai rasa haus yang hebat, kram otot, penurunan produksi air kemih, sehingga badan terasa sangat lemah, mata menjadi cekung dan kulit jari-jari tangan mengeriput "
context2= "Sakit kepala: Ada beberapa jenis sakit kepala seperti migrain, sakit kepala tegang, dan sakit kepala sinus. Diare: Gejala diare antara lain perut kembung, mual, dan buang air besar yang berlebihan dan berair. Sakit gigi: Gejala sakit gigi antara lain rasa sakit pada gigi atau gusi, dan sakit kepala. Sakit perut: Gejala sakit perut antara lain rasa sakit pada perut, kembung, dan mual. Sariawan: Gejala sariawan antara lain luka pada mulut, terutama pada lidah atau bagian dalam pipi.Ruam kulit: Gejala ruam kulit antara lain gatal-gatal dan bercak-bercak pada kulit. Sakit tenggorokan: Gejala sakit tenggorokan antara lain sakit saat menelan dan tenggorokan merah. Gigitan serangga: Gejala gigitan serangga antara lain rasa sakit, gatal-gatal, dan bengkak pada kulit. Sakit punggung: Gejala sakit punggung antara lain rasa sakit pada bagian punggung bawah dan sulit untuk bergerak."
mengatasi_Sakit_kepala = "Cara penanganannya tergantung dari jenis sakit kepala, bisa dengan minum obat pereda nyeri seperti paracetamol atau melakukan teknik relaksasi."
mengatasi_Diare ="Cara penanganannya yaitu minum banyak air putih dan elektrolit, konsumsi makanan ringan seperti roti tawar, dan hindari makanan yang sulit dicerna."
mengatasi_Sakit_gigi = "Cara penanganannya yaitu berkumur dengan air garam hangat, minum obat pereda nyeri seperti paracetamol, dan memeriksakan diri ke dokter gigi jika diperlukan."
mengatasi_Sakit_perut = "Cara penanganannya tergantung dari penyebabnya, bisa dengan menghindari makanan yang sulit dicerna atau konsumsi obat pereda nyeri seperti paracetamol."
mengatasi_Sariawan ="Cara penanganannya yaitu berkumur dengan air garam, konsumsi makanan yang lunak, dan aplikasikan salep atau gel yang mengandung kortikosteroid."
mengatasi_Ruam_kulit = "Cara penanganannya tergantung dari penyebabnya, bisa dengan menghindari pemicu alergi atau konsumsi obat anti alergi."
mengatasi_Sakit_tenggorokan = "Cara penanganannya yaitu berkumur dengan air garam, minum banyak air putih, dan konsumsi obat pereda nyeri seperti paracetamol"
mengatasi_Gigitan_serangga = "Cara penanganannya yaitu membersihkan area yang digigit dengan air dan sabun, konsumsi obat pereda nyeri atau antihistamin, dan hindari menggaruk area yang digigit."
mengatasi_Sakit_pinggang = "Cara penanganannya yaitu istirahat yang cukup, pergi ke"

gmaps_rumah_sakit = "Rumah Sakit terdekat =>"
gmaps_puskesmas = "Puskesmas terdekat =>"
gmaps_apotek = "Apotek terdekat =>"
gmaps_urut = "Tempat pijat / urut disekitar anda =>"

link_rumah_sakit = "https://www.google.com/maps/search/Rumah_sakit/"
link_puskesmas = "https://www.google.com/maps/search/Puskesmas/"
link_apotek = "https://www.google.com/maps/search/Apotek/"
link_urut = "https://www.google.com/maps/search/Urut/"

def bert_prediction(question):
  respon_model = []
  if question in context:
    begin = datetime.now()
    encodedData = tokenizer(question, context, padding=True, return_offsets_mapping=True, truncation="only_second", return_tensors="pt")
    offsetMapping = encodedData.pop("offset_mapping")[0]
    encodedData.to(device)
    model.to(device)
    print(context)
    print(question)
    model.eval() 
    with torch.no_grad(): # IMPORTANT! Do not computing gradient!
      outputs = model(encodedData["input_ids"], attention_mask=encodedData["attention_mask"]) # Feed forward. Without calculating loss.
    startLogits = outputs.start_logits[0].detach().cpu().numpy() # Getting logits, moving to CPU.
    endLogits = outputs.end_logits[0].detach().cpu().numpy() # Getting logits, moving to CPU.
    start_indexes = np.argsort(startLogits).tolist()
    end_indexes = np.argsort(endLogits).tolist()
    candidates = []
    for start_index in start_indexes:
      for end_index in end_indexes:
        if (
          start_index >= len(offsetMapping)
          or end_index >= len(offsetMapping)
          or offsetMapping[start_index] is None
          or offsetMapping[end_index] is None
        ):
          continue 
        if end_index < start_index or end_index - start_index + 1 > 25:
          continue
        if start_index <= end_index:
          start_char = offsetMapping[start_index][0]
          end_char = offsetMapping[end_index][1]
          candidates.append({
            "score": startLogits[start_index] + endLogits[end_index],
            "text": context[start_char: end_char]
          })
    candidates = sorted(candidates, key=lambda x: x["score"], reverse=True)[:1]
    respon_model = []
    for i, candidate in enumerate(candidates):
      dictlogs = {}
      #rank = str(i+1) #convert number rank to string
      scoree = str(candidate['score']) #convert float32 to string
      print(scoree)
      print(candidate['text'])
      nama_penyakit = candidate['text']
      status = True
      print(candidate['text'])
      if 'maag' in nama_penyakit:
        status = True
        solusi= mengatasi_maag
        gmaps = gmaps_apotek 
        link = link_apotek
      elif 'influenza' in nama_penyakit:
        status = True
        solusi=mengatasi_influenza
        gmaps = gmaps_apotek 
        link = link_apotek
      elif 'Muntaber' in nama_penyakit:
        status = True
        solusi= mengatasi_Muntaber
        gmaps = gmaps_apotek 
        link = link_apotek
      elif 'Cacar air' in nama_penyakit:
        status = True
        solusi= mengatasi_Cacar_air
        gmaps = gmaps_puskesmas
        link = link_puskesmas
      elif 'Tifus'in nama_penyakit:
        status = True
        solusi= mengatasi_Tifus
        gmaps = gmaps_rumah_sakit
        link = link_rumah_sakit
      elif 'Campak'in nama_penyakit:
        status = True
        solusi= mengatasi_Campak
        gmaps = gmaps_puskesmas
        link = link_puskesmas
      elif 'Pneumonia'in nama_penyakit:
        status = True
        solusi= mengatasi_Pneumonia
        gmaps = gmaps_rumah_sakit
        link = link_rumah_sakit
      elif 'PES'in nama_penyakit:
        status = True
        solusi= mengatasi_PES
        gmaps = gmaps_rumah_sakit
        link = link_rumah_sakit
      elif 'Kolera'in nama_penyakit:
        status = True
        solusi= mengatasi_Kolera
        gmaps = gmaps_rumah_sakit
        link = link_rumah_sakit
      else:
        status = False
      print(status)
      cur = mysql.connection.cursor()
      if(status == False):
        dictlogs.update({"status": status,"deskripsi":"maaf kami tidak berhasil mencari gejala yang sesuai dengan penyakit anda"})
        cur.execute("INSERT INTO history(pertanyaan,status,keterangan) VALUES(%s,%s,%s)" , (question,status,"maaf kami tidak berhasil mencari gejala yang sesuai dengan penyakit anda"))
        mysql.connection.commit()
      else:
        dictlogs.update({"status": status,"jawaban": "berdasarkan gejala yang anda alami kemungkinan anda menderita penyakit "+nama_penyakit, "solusi": solusi,"gmaps":gmaps,"link":link})
        cur.execute("INSERT INTO history(pertanyaan,status,nama_penyakit,solusi) VALUES(%s,%s,%s,%s)" , (question,status,nama_penyakit,solusi))
        mysql.connection.commit()
      respon_model.append(dictlogs)
      #langsung save db 
      #book=  HISTORY(id=1,nama="guest",pertanyaan=question,jawaban=candidate['text'],score=scoree,waktu_proses=str(datetime.now()-begin))
      #db.session.add(book)
      #db.session.commit()
  elif question in context2:
    begin = datetime.now()
    encodedData = tokenizer(question, context2, padding=True, return_offsets_mapping=True, truncation="only_second", return_tensors="pt")
    offsetMapping = encodedData.pop("offset_mapping")[0]
    encodedData.to(device)
    model.to(device)
    print(context)
    print(question)
    model.eval() 
    with torch.no_grad(): # IMPORTANT! Do not computing gradient!
      outputs = model(encodedData["input_ids"], attention_mask=encodedData["attention_mask"]) # Feed forward. Without calculating loss.
    startLogits = outputs.start_logits[0].detach().cpu().numpy() # Getting logits, moving to CPU.
    endLogits = outputs.end_logits[0].detach().cpu().numpy() # Getting logits, moving to CPU.
    start_indexes = np.argsort(startLogits).tolist()
    end_indexes = np.argsort(endLogits).tolist()
    candidates = []
    for start_index in start_indexes:
      for end_index in end_indexes:
        if (
          start_index >= len(offsetMapping)
          or end_index >= len(offsetMapping)
          or offsetMapping[start_index] is None
          or offsetMapping[end_index] is None
        ):
          continue 
        if end_index < start_index or end_index - start_index + 1 > 25:
          continue
        if start_index <= end_index:
          start_char = offsetMapping[start_index][0]
          end_char = offsetMapping[end_index][1]
          candidates.append({
            "score": startLogits[start_index] + endLogits[end_index],
            "text": context[start_char: end_char]
          })
    candidates = sorted(candidates, key=lambda x: x["score"], reverse=True)[:1]
    respon_model = []
    for i, candidate in enumerate(candidates):
      dictlogs = {}
      #rank = str(i+1) #convert number rank to string
      scoree = str(candidate['score']) #convert float32 to string
      print(scoree)
      print(candidate['text'])
      nama_penyakit = candidate['text']
      status = True
      print(candidate['text'])
      if 'Sakit kepala' in nama_penyakit:
        status = True
        solusi= mengatasi_Sakit_kepala
      elif 'Diare' in nama_penyakit:
        status = True
        solusi=mengatasi_Diare
      elif 'Muntaber' in nama_penyakit:
        status = True
        solusi= mengatasi_Muntaber
      elif 'Cacar air' in nama_penyakit:
        status = True
        solusi= mengatasi_Cacar_air
      elif 'Tifus'in nama_penyakit:
        status = True
        solusi= mengatasi_Tifus
      elif 'Campak'in nama_penyakit:
        status = True
        solusi= mengatasi_Campak
      elif 'Pneumonia'in nama_penyakit:
        status = True
        solusi= mengatasi_Pneumonia
      elif 'PES'in nama_penyakit:
        status = True
        solusi= mengatasi_PES
      elif 'Kolera'in nama_penyakit:
        status = True
        solusi= mengatasi_Kolera
      else:
        status = False
      print(status)
      cur = mysql.connection.cursor()
      if(status == False):
        dictlogs.update({"status": status,"deskripsi":"maaf kami tidak berhasil mencari gejala yang sesuai dengan penyakit anda"})
        cur.execute("INSERT INTO history(pertanyaan,status,keterangan) VALUES(%s,%s,%s)" , (question,status,"maaf kami tidak berhasil mencari gejala yang sesuai dengan penyakit anda"))
        mysql.connection.commit()
      else:
        dictlogs.update({"status": status,"jawaban": "berdasarkan gejala yang anda alami kemungkinan anda menderita penyakit "+nama_penyakit, "solusi": solusi})
        cur.execute("INSERT INTO history(pertanyaan,status,nama_penyakit,solusi) VALUES(%s,%s,%s,%s)" , (question,status,nama_penyakit,solusi))
        mysql.connection.commit()
      respon_model.append(dictlogs)
      #langsung save db 
      #book=  HISTORY(id=1,nama="guest",pertanyaan=question,jawaban=candidate['text'],score=scoree,waktu_proses=str(datetime.now()-begin))
      #db.session.add(book)
      #db.session.commit()
  else:
    print("tidak ditemukan di context")
    cur = mysql.connection.cursor()
    respon_model = []
    dictlogs = {}
    status= False
    dictlogs.update({"status": status,"deskripsi":"maaf kami tidak berhasil mencari gejala yang sesuai dengan penyakit anda"})
    cur.execute("INSERT INTO history(pertanyaan,status,keterangan) VALUES(%s,%s,%s)" , (question,status,"maaf kami tidak berhasil mencari gejala yang sesuai dengan penyakit anda"))
    mysql.connection.commit()
    respon_model.append(dictlogs)
  return jsonify(respon_model)
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=4040,debug=True)