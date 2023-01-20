import torch,time,numpy as np
from flask import Flask,jsonify
from transformers import BertTokenizerFast, BertForQuestionAnswering, Trainer, TrainingArguments
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
db = SQLAlchemy()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']= True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bigprojeks2.db'
class HISTORY(db.Model):
    id = db.Column(db.Integer, primary_key=True) # kudu ana primary key
    nama = db.Column(db.String(100))
    konteks = db.Column(db.String(3000))
    pertanyaan = db.Column(db.String(1000))
    rank = db.Column(db.String(100))
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

mengatasi_maag ="cara mengatasinya : Makan secara perlahan, dalam porsi yang kecil Batasi konsumsi makanan pedas dan berlemak, Kurangi minuman berkafein, Hindari obat-obatan yang menyebabkan nyeri lambung"
mengatasi_influenza="cara mengatasinya : Menjaga daya tahan tubuh agar tidak mudah terserang virus. Misalnya dengan makan teratur, istirahat yang cukup, minum air putih sesuai kebutuhan, berolah raga, dan memiliki gaya hidup yang sehat.Selain itu, menjaga daya tahan tubuh juga dapat juga didukung dengan asupan vitamin terutama Vitamin C yang bisa didapatkan di buah-buahan maupun vitamin yang dijual di toko-toko.Pencegahan lainnya adalah dengan menggunakan masker ditempat umum, terutama bagi yang menderita influenza."
mengatasi_Muntaber="Cara mengatasi muntaber yang dapat dilakukan dengan mudah adalah terapi rehidrasi dengan cara mengonsumsi banyak cairan terutama air putih. Sementara untuk balita dan anak-anak, pemakaian oralit mungkin bisa langsung diberikan untuk menggantikan cairan yang hilang. Kenapa harus oralit? Karena air biasa tidak memiliki kandungan garam dan nutrisi yang cukup untuk menggantikan cairan yang hilang.Jika diperlukan, dokter biasanya akan meresepkan antibiotika jenis metronidazol yang dikombinasikan dengan sulfametoksazol dan trimetoprim. Obat diare lainnya yang bisa digunakan adalah probiotik. Probiotik bisa digunakan untuk mengobati diare dengan cara melawan bakteri jahat penyebab diare.Baca lebih lanjut di DokterSehat: Muntaber: Penyebab, Gejala, Obat, Penanganan, dll | https://doktersehat.com/penyakit-a-z/muntaber/"
mengatasi_Cacar_air= "Melakukan vaksinasi cacar air, Menjaga kebersihan diri sendiri, pakaian, dan lingkungan, Mengkonsumsi makanan bergizi, Menghindari sumber penularan cacar air "
mengatasi_Tifus="Memastikan kebersihan bahan makanan sebelum memasaknya, Mencuci tangan secara teratur, terutama sebelum dan setelah makanan, Membersihkan luka dan segera mengobatinya, Hindari jajan di pinggir jalan yang terlihat tidak higienis, Menjaga daya tahan tubuh, Memakan yang tinggi protein, rendah serat, lunak, tidak asam,  dan pedas,"
mengatasi_Campak="Melakukan vaksinasi ketika masih usia balita."
mengatasi_Pneumonia="Terapi kausal Terapi ini dilakukan dengan cara pemberian obat antibiotik atau obat antijamur. Terapi suportif umum Penanganan ini disesuaikan dengan keadaan pasien, misalnya ketika pemberian terapi oksigen. Terapi inhalasi Dengan cara menyalurkan obat langsung ke paru-paru, terapi ini sangat bermanfaat pada kondisi pasien yang membutuhkan pengobatan segera. Terapi ini dapat menghindari efek samping yang berkelanjutan, mengencerkan dahak yang kental dan kekuningan, serta mengatasi infeksi. Fisioterapi dada Cara ini dilakukan untuk mempermudah proses pengeluaran dahak dari paru. Meningkatkan daya tahan tubuh sangat penting untuk menghindarkan diri dari pneumonia. Karena itu, jagalah kebersihan diri dengan menerapkan hal-hal berikut dalam keseharian:Rajin mencuci tanganMengenakan masker ketika pergi ke tempat umumBerolahraga secara teratur"
mengatasi_PES="Penanganan terhadap penyakit pes membutuhkan perawatan inap di rumah sakit. Dokter akan meresepkan antibiotik untuk membunuh bakteri, serta obat-obatan lain sesuai dengan tanda dan gejala yang dialami oleh penderita tersebut. rumah sakit terdekat => https://www.google.com/maps/search/Rumah_sakit/ "
mengatasi_Kolera="memperbanyak asupan cairan untuk mencegah dehidrasi akibat kolera Bila dehidrasi sudah diatasi, tujuan pengobatan selanjutnya adalah untuk menggantikan jumlah cairan yang hilang karena diare dan muntah. Pengobatan awal dengan tetrasiklin atau antibiotik lainnya bisa membunuh bakteri dan biasanya akan menghentikan diare dalam 48 jam.Bila berada di daerah resisten dengan wabah kolera atau Vibrio cholerae, dapat digunakan furozolidone. Makanan padat bisa diberikan setelah muntah-muntah berhenti dan nafsu makan sudah kembali.Pencegahan: Untuk mencegah kolera, penting untuk melakukan penjernihan cadangan air dan pembuangan tinja yang memenuhi standar. Selain itu, minumlah air yang sudah terlebih dahulu dimasak. Hindari mengonsumsi sayuran mentah atau ikan dan kerang yang tidak dimasak sampai matang.Pemberian antibiotik tetrasiklin juga bisa membantu mencegah penyakit pada orang-orang yang sama-sama menggunakan perabotan rumah dengan penderita kolera. Sementara itu, vaksinasi kolera tidak terlalu dianjurkan karena perlindungan yang diberikan tidak menyeluruh."

context="maag atau sindrom dispepsia adalah penyakit yang mempunyai gejala Nyeri ulu hati, mual, dan muntah setelah makan. Muntaber adalah penyakit yang mempunyai gejala diare (buang air besar lebih sering dari biasanya dan ditandai dengan kondisi feses yang lebih encer dari biasanya), mual, muntah berulang kali, dan nyeri perut. Cacar air adalah penyakit yang mempunyai gejala bintik kemerahan di kulit yang menggelembung maupun tidak, melepuh, dan terasa gatal. Tifus adalah penyakit yang mempunyai gejala demam yang suhunya naik secara bertahap hingga membuat pendeita menggigil. Campak adalah penyakit yang mempunyai gejala naiknya suhu tubuh, batuk, nyeri tenggorokan, nyeri otot, hingga ruam pada kulit yang muncul sekitar 7-14 hari setelah terinfeksi virus.influenza adalah penyakit yang mempunyai gejala Demam, batuk, nyeri tenggorokan, hidung berair, hidung tersumbat, sakit kepala, mudah lelah. Pneumonia atau radang paru-paru adalah penyakit yang mempunyai gejala. PES atau yang juga dikenal dengan Pesteurellosis adalah penyakit yang mempunyai gejala demam dan menggigil yang tiba-tiba Nyeri kepala Rasa lelah Nyeri otot Batuk, dengan dahak yang disertai darah Kesulitan bernapas Mual dan muntah Demam tinggi Nyeri kepala Rasa lemah .Kolera adalah penyakit yang mempunyai gejala bervariasi, mulai dari diare ringan sampai diare berat yang bisa berakibat fatal. Dalam beberapa kasus, orang yang terinfeksi justru tidak menunjukkan gejala apa pun, diare encer seperti air yang terjadi secara tiba-tiba, tanpa rasa sakit dan muntah-muntah, dehidrasi disertai rasa haus yang hebat, kram otot, penurunan produksi air kemih, sehingga badan terasa sangat lemah, mata menjadi cekung dan kulit jari-jari tangan mengeriput"
def bert_prediction(user,question):
  if question in context:
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
        score = str(candidate['score']) #convert float32 to string
        print(score)
        print(candidate['text'])
        if 'maag' in candidate['text']:
          status = True
          solusi= mengatasi_maag
        elif 'influenza' in candidate['text']:
          status = True
          solusi=mengatasi_influenza
        elif 'Muntaber' in candidate['text']:
          status = True
          solusi= mengatasi_Muntaber
        elif 'Cacar air' in candidate['text']:
          status = True
          solusi= mengatasi_Cacar_air
        elif 'Tifus'in candidate['text']:
          status = True
          solusi= mengatasi_Tifus
        elif 'Campak'in candidate['text']:
          status = True
          solusi= mengatasi_Campak
        elif 'Pneumonia'in candidate['text']:
          status = True
          solusi= mengatasi_Pneumonia
        elif 'PES'in candidate['text']:
          status = True
          solusi= mengatasi_PES
        elif 'Kolera'in candidate['text']:
          status = True
          solusi= mengatasi_Kolera
        else:
          status = False
        if(status == False):
          dictlogs.update({"status": status,"deskripsi":"maaf kami tidak berhasil mencari gejala yang sesuai dengan penyakit anda"})
        else:
          dictlogs.update({"status": status,"jawaban": "berdasarkan gejala yang anda alami kemungkinan anda menderita penyakit "+candidate['text'], "solusi": solusi})
        respon_model.append(dictlogs)
        #langsung save db bosku
    else:
         respon_model = []
  print(respon_model)
  return jsonify(respon_model)