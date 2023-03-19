import torch,time,numpy as np
from flask import jsonify
from transformers import BertTokenizerFast, BertForQuestionAnswering, Trainer, TrainingArguments
from datetime import datetime
from . import mysql
import openai
import textwrap
import urllib, json
with urllib.request.urlopen("https://tegaltourism.com/coba.php") as url:
    b = str(url.read())
a="sk-lbkFJ"
c="4Ix2gOoxGus"
d="3ddnc2QM6T3B"
e="4X1XTsgQdKlJ"
key = ''.join([a,b,c,d,e])
#print(key)
openai.api_key =key
device = "cuda" if torch.cuda.is_available() else "cpu" 
torch.device(device) 
modelCheckpoint = "indolem/indobert-base-uncased"
model = BertForQuestionAnswering.from_pretrained("model")
tokenizer = BertTokenizerFast.from_pretrained(modelCheckpoint)
start_time = time.time()

mengatasi_maag ="cara mengatasinya : Makan secara perlahan, dalam porsi yang kecil Batasi konsumsi makanan pedas dan berlemak, Kurangi minuman berkafein, Hindari obat-obatan yang menyebabkan nyeri lambung, Anda juga bisa mengkonsumsi obat penetraalisir maag seperti Promag, mylanta, polysilane dst. Promag dijual secara bebas dan tersedia dalam bentuk tablet kunyah serta suspensi cair."
mengatasi_influenza="cara mengatasinya : Menjaga daya tahan tubuh agar tidak mudah terserang virus. Misalnya dengan makan teratur, istirahat yang cukup, minum air putih sesuai kebutuhan, berolah raga, dan memiliki gaya hidup yang sehat.Selain itu, menjaga daya tahan tubuh juga dapat juga didukung dengan asupan vitamin terutama Vitamin C yang bisa didapatkan di buah-buahan maupun vitamin yang dijual di toko-toko.Pencegahan lainnya adalah dengan menggunakan masker ditempat umum, terutama bagi yang menderita influenza."
mengatasi_Muntaber="Cara mengatasi : muntaber yang dapat dilakukan dengan mudah adalah terapi rehidrasi dengan cara mengonsumsi banyak cairan terutama air putih. Sementara untuk balita dan anak-anak, pemakaian oralit mungkin bisa langsung diberikan untuk menggantikan cairan yang hilang. Kenapa harus oralit? Karena air biasa tidak memiliki kandungan garam dan nutrisi yang cukup untuk menggantikan cairan yang hilang.Jika diperlukan, dokter biasanya akan meresepkan antibiotika jenis metronidazol yang dikombinasikan dengan sulfametoksazol dan trimetoprim. Obat diare lainnya yang bisa digunakan adalah probiotik. Probiotik bisa digunakan untuk mengobati diare dengan cara melawan bakteri jahat penyebab diare. "
mengatasi_Cacar_air= "cara mengatasinya : Melakukan vaksinasi cacar air, Menjaga kebersihan diri sendiri, pakaian, dan lingkungan, Mengkonsumsi makanan bergizi, Menghindari sumber penularan cacar air."
mengatasi_Tifus="cara mengatasinya : Memastikan kebersihan bahan makanan sebelum memasaknya, Mencuci tangan secara teratur, terutama sebelum dan setelah makanan, Membersihkan luka dan segera mengobatinya, Hindari jajan di pinggir jalan yang terlihat tidak higienis, Menjaga daya tahan tubuh, Memakan yang tinggi protein, rendah serat, lunak, tidak asam,  dan pedas."
mengatasi_Campak="cara mengatasinya : Melakukan vaksinasi ketika masih usia balita."
mengatasi_Pneumonia="cara mengatasinya : Terapi kausal Terapi ini dilakukan dengan cara pemberian obat antibiotik atau obat antijamur. Terapi suportif umum Penanganan ini disesuaikan dengan keadaan pasien, misalnya ketika pemberian terapi oksigen. Terapi inhalasi Dengan cara menyalurkan obat langsung ke paru-paru, terapi ini sangat bermanfaat pada kondisi pasien yang membutuhkan pengobatan segera. Terapi ini dapat menghindari efek samping yang berkelanjutan, mengencerkan dahak yang kental dan kekuningan, serta mengatasi infeksi. Fisioterapi dada Cara ini dilakukan untuk mempermudah proses pengeluaran dahak dari paru. Meningkatkan daya tahan tubuh sangat penting untuk menghindarkan diri dari pneumonia. Karena itu, jagalah kebersihan diri dengan menerapkan hal-hal berikut dalam keseharian:Rajin mencuci tanganMengenakan masker ketika pergi ke tempat umumBerolahraga secara teratur."
mengatasi_PES="cara mengatasinya : Penanganan terhadap penyakit pes membutuhkan perawatan inap di rumah sakit. Dokter akan meresepkan antibiotik untuk membunuh bakteri, serta obat-obatan lain sesuai dengan tanda dan gejala yang dialami oleh penderita tersebut."
mengatasi_Kolera="cara mengatasinya : memperbanyak asupan cairan untuk mencegah dehidrasi akibat kolera Bila dehidrasi sudah diatasi, tujuan pengobatan selanjutnya adalah untuk menggantikan jumlah cairan yang hilang karena diare dan muntah. Pengobatan awal dengan tetrasiklin atau antibiotik lainnya bisa membunuh bakteri dan biasanya akan menghentikan diare dalam 48 jam.Bila berada di daerah resisten dengan wabah kolera atau Vibrio cholerae, dapat digunakan furozolidone. Makanan padat bisa diberikan setelah muntah-muntah berhenti dan nafsu makan sudah kembali.Pencegahan: Untuk mencegah kolera, penting untuk melakukan penjernihan cadangan air dan pembuangan tinja yang memenuhi standar. Selain itu, minumlah air yang sudah terlebih dahulu dimasak. Hindari mengonsumsi sayuran mentah atau ikan dan kerang yang tidak dimasak sampai matang.Pemberian antibiotik tetrasiklin juga bisa membantu mencegah penyakit pada orang-orang yang sama-sama menggunakan perabotan rumah dengan penderita kolera. Sementara itu, vaksinasi kolera tidak terlalu dianjurkan karena perlindungan yang diberikan tidak menyeluruh."


# print(context)
# cur.execute("SELECT nama_penyakit,'adalah penyakit yang mempunyai gejala', gejala, penyegahan, rekomendasi_rujukan.nama_tempat ,'terdekat => ', rekomendasi_rujukan.link_maps from input_dokter inner join rekomendasi_rujukan on input_dokter.rekomendasi_rujukan = rekomendasi_rujukan.nama_tempat ")
# fromdb = cur.fetchall()
# context = str(fromdb)
mengatasi_Sakit_kepala = "Cara penanganannya tergantung dari jenis sakit kepala, bisa dengan minum obat pereda nyeri seperti paracetamol atau melakukan teknik relaksasi."
mengatasi_Diare ="Cara penanganannya yaitu minum banyak air putih dan elektrolit, konsumsi makanan ringan seperti roti tawar, dan hindari makanan yang sulit dicerna."
mengatasi_Sakit_gigi = "Cara penanganannya yaitu berkumur dengan air garam hangat, minum obat pereda nyeri seperti paracetamol, dan memeriksakan diri ke dokter gigi jika diperlukan."
mengatasi_Sakit_perut = "Cara penanganannya tergantung dari penyebabnya, bisa dengan menghindari makanan yang sulit dicerna atau konsumsi obat pereda nyeri seperti paracetamol."
mengatasi_Sariawan ="Cara penanganannya yaitu berkumur dengan air garam, konsumsi makanan yang lunak, dan aplikasikan salep atau gel yang mengandung kortikosteroid."
mengatasi_Ruam_kulit = "Cara penanganannya tergantung dari penyebabnya, bisa dengan menghindari pemicu alergi atau konsumsi obat anti alergi."
mengatasi_Sakit_tenggorokan = "Cara penanganannya yaitu berkumur dengan air garam, minum banyak air putih, dan konsumsi obat pereda nyeri seperti paracetamol"
mengatasi_Gigitan_serangga = "Cara penanganannya yaitu membersihkan area yang digigit dengan air dan sabun, konsumsi obat pereda nyeri atau antihistamin, dan hindari menggaruk area yang digigit."
mengatasi_Sakit_pinggang = "Cara penanganannya yaitu istirahat yang cukup, pergi ke"

gmaps_rumah_sakit = "Rumah Sakit terdekat => "
gmaps_puskesmas = "Puskesmas terdekat => "
gmaps_apotek = "Apotek terdekat => "
gmaps_urut = "Tempat pijat / urut disekitar anda => "

link_rumah_sakit = "https://www.google.com/maps/search/Rumah_sakit/"
link_puskesmas = "https://www.google.com/maps/search/Puskesmas/"
link_apotek = "https://www.google.com/maps/search/Apotek/"
link_urut = "https://www.google.com/maps/search/Urut/"

def convertTuple1(tup):
    return ''.join([str(x) for x in tup])

def bert_prediction(question):
  respon_model = []
  dictlogs = {}
  strs = """In my project, I have a bunch of strings that are read in from a file. 
  Most of them, when printed in the command console, exceed 80 characters in length and wrap around, looking ugly."""
  print(textwrap.fill(strs, 520))
  raw="""Politeknik Harapan Bersama (Poltek Harber) melakukan penandatanganan MoU dengan Lembaga Inkubator
   dan Tenant Program Wirausaha/Wira Koperasi Dinas Koperasi UKM Provinsi Jawa tengah (Jateng) yang bertempat di Ruang Rapat Utama Gedung 
   D, Poltek Harber, Senin, (27/02/23).Direktur Poltek Harber, Agung Hendarto mengatakan pihaknya merasa sangat terhormat karena Poltek Harber ditetapkan sebagai Lembaga Inkubator dan Tenant oleh Dinas Koperasi UKM Provinsi Jateng. “Kami juga merasa terhormat menjadi tempat koordinasi dalam rangka satu pembahasan identifikasi program inkubasi yang berlangsung selama 9 bulan. Koperasi menjadi pilihan Poltek Harber untuk ikut serta memajukan perekonomian Indonesia,” kata Agung.“Inisiasi dari Dinas Koperasi UKM Provinsi Jateng kita sambut dengan gembira. Semoga dengan amanah yang diberikan ini bisa terlaksana dengan baik dan bisa menghasilkan suatu produk yang go Internasional,“ kata Agung. Sementara itu, Kepala Dinas Koperasi UKM Provinsi Jateng yang diwakili oleh Kepala Bidang Kelembagaan, Bima Kartika, memberikan ucapan selamat atas terpilihnya Poltek Harber sebagai salah satu pelaksana program inkubator tahun 2023. Dalam Peraturan Pemerintah (PP) nomor 7 tahun 2021 bahwa setiap pemerintah provinsi/kota/kabupaten wajib untuk melaksanakan program inkubasi. “Semakin banyak kita berkolaborasi dan bersinergi maka akan semakin mudah membina koperasi dan UKM. Saat ini kita bicarakan kualitas koperasi di masa depan. Koperasi di Indonesia sudah sangat jauh tertinggal. Kita sekarang berguru ke Vietnam. 
  Padahal tahun 80an Indonesia pernah menjadi guru untuk negara lain, seperti Malaysia,“ tambahnya. 
  Penetapan Lembaga Inkubator dan Tenant 
  Dinas Koperasi UKM Provinsi Jateng tahun ini dibagi menjadi tiga, yaitu Inkubator Wira Koperasi Kluster Shuttlecock Kabupaten Tegal di Poltek Harber, Inkubator Wira Koperasi Kluster Nanas Kabupaten Pemalang di ITB Pemalang, dan Inkubator Wira Koperasi Kluster Gula Kelapa/Gula Semut di UMP Kabupaten Purworejo. Program inkubasi berjalan selama 9 bulan, dari Februari hingga Oktober 2023. 
  maag matau sindrom dispepsia adalah penyakit yang mempunyai gejala Nyeri ulu hati, mual, dan muntah setelah makan. 
  Muntaber adalah penyakit yang mempunyai gejala diare (buang air besar lebih sering dari biasanya dan ditandai dengan kondisi feses yang lebih encer dari biasanya), mual, muntah berulang kali, dan nyeri perut. 
  Cacar air adalah penyakit yang mempunyai gejala bintik kemerahan di kulit yang menggelembung maupun tidak, melepuh, dan terasa gatal. 
  Tifus adalah penyakit yang mempunyai gejala demam yang suhunya naik secara bertahap hingga membuat pendeita menggigil. 
  Campak adalah penyakit yang mempunyai gejala naiknya suhu tubuh, batuk, nyeri tenggorokan, nyeri otot, hingga ruam pada kulit yang muncul sekitar 7-14 hari setelah terinfeksi virus.
  influenza adalah penyakit yang mempunyai gejala Demam, batuk, nyeri tenggorokan, hidung berair, hidung tersumbat, sakit kepala, mudah lelah. Pneumonia atau radang paru-paru adalah penyakit yang mempunyai gejala. PES atau yang juga dikenal dengan Pesteurellosis adalah penyakit yang mempunyai gejala demam dan menggigil yang tiba-tiba Nyeri kepala Rasa lelah Nyeri otot Batuk, dengan dahak yang disertai darah Kesulitan bernapas Mual dan muntah Demam tinggi Nyeri kepala Rasa lemah .Kolera adalah penyakit yang mempunyai gejala bervariasi, mulai dari diare ringan sampai diare berat yang bisa berakibat fatal. Dalam beberapa kasus, orang yang terinfeksi justru tidak menunjukkan gejala apa pun, diare encer seperti air yang terjadi secara tiba-tiba, tanpa rasa sakit dan muntah-muntah, dehidrasi disertai rasa haus yang hebat, kram otot, penurunan produksi air kemih, sehingga badan terasa sangat lemah, mata menjadi cekung dan kulit jari-jari tangan mengeriput """
  cur = mysql.connection.cursor()
  cur.execute("SELECT nama_penyakit,' adalah penyakit yang mempunyai gejala ', gejala from input_dokter")
  fromdb= cur.fetchall()
  for i in range(len(fromdb)):
    item = convertTuple1(fromdb[i])
    raw=raw+item
  context = textwrap.wrap(raw, 520)
  print(context)
  begin = datetime.now()
  for i in range(len(context)):
    encodedData = tokenizer(question, raw, padding=True, return_offsets_mapping=True, truncation="only_second", return_tensors="pt")
    offsetMapping = encodedData.pop("offset_mapping")[0]
    encodedData.to(device)
    print(i)
    model.to(device)
    print(context[i])
    print(question)
    print(len(encodedData["input_ids"][0]))
    jmltoken = len(encodedData["input_ids"][0])
    if jmltoken > 512:
      dictlogs.update({"status": False,"deskripsi":"maaf terjadi error di sistem kami tunggu 2x24 jam untuk mencoba kembali"})
      break
    model.eval() 
    with torch.no_grad(): # IMPORTANT! Do not computing gradient!
      print(range(len(encodedData["input_ids"][0])))
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

    for i, candidate in enumerate(candidates):
      scoree = candidate['score']
      if scoree<=0:
        dictlogs.update({"status": False,"deskripsi":"maaf kami tidak berhasil mencari gejala yang sesuai dengan penyakit anda"})
      else:
        # rank = str(i+1) #convert number rank to string
        scoree = str(candidate['score']) # convert float32 to string
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
          cur.execute("Select nama_penyakit from input_dokter")
          penyakit_lain = cur.fetchall()
          for i in penyakit_lain:
            if convertTuple1(i) == nama_penyakit:
              status = True
              cur.execute("Select pencegahan, rekomendasi_rujukan.nama_tempat , rekomendasi_rujukan.link_maps from input_dokter inner join rekomendasi_rujukan on input_dokter.rekomendasi_rujukan = rekomendasi_rujukan.nama_tempat")
              detail = cur.fetchone()
              solusi = 'Cara penanganannya yaitu '+detail[0]
              gmaps = detail[1]+' terdekat => '
              link = detail[2]
            else:
              status = True
        print(status)
        if(status == False):
            dictlogs.update({"status": status,"deskripsi":"maaf kami tidak berhasil mencari gejala yang sesuai dengan penyakit anda"})
        # mysql
        #   cur.execute("INSERT INTO history(pertanyaan,status,keterangan) VALUES(%s,%s,%s)" , (question,status,"maaf kami tidak berhasil mencari gejala yang sesuai dengan penyakit anda"))
        #   mysql.connection.commit()
        # sqllite 
        #   book=  HISTORY(id=1,nama="guest",pertanyaan=question,status=status.keterangan="maaf kami tidak berhasil mencari gejala yang sesuai dengan penyakit anda",score=scoree,waktu_proses=str(datetime.now()-begin),)
        #   db.session.add(book)
        #   db.session.commit()
        # mongodb 
        #   book=  HISTORY(id=1,nama="guest",pertanyaan=question,jawaban=candidate['text'],score=scoree,waktu_proses=str(datetime.now()-begin))
        #   db.session.add(book)
        #   db.session.commit()
        else:
            dictlogs.update({"status": status,"jawaban": nama_penyakit})
            break
        # mysql
        #   cur.execute("INSERT INTO history(pertanyaan,status,nama_penyakit,solusi) VALUES(%s,%s,%s,%s)" , (question,status,nama_penyakit,solusi))
        #   mysql.connection.commit()
        # sqllite 
        #   book=  HISTORY(id=1,nama="guest",status=status,pertanyaan=question,nama_penyakit=nama_penyakit,solusi=solusi,score=scoree,waktu_proses=str(datetime.now()-begin),gmaps=gmaps,link=link)
        #   db.session.add(book)
        #   db.session.commit()
        # mongodb
        #   book=  HISTORY(id=1,nama="guest",pertanyaan=question,jawaban=candidate['text'],score=scoree,waktu_proses=str(datetime.now()-begin))
        #   db.session.add(book)
        #   db.session.commit()
  
  respon_model.append(dictlogs)    
  
  print(respon_model)
  return jsonify(respon_model)

def random_question(ask):
  prompt = (ask)

  completions = openai.Completion.create(
      engine="text-davinci-002",
      prompt=prompt,
      max_tokens=1024,
      n=1,
      stop=None,
      temperature=0.5,
  )

  message = completions.choices[0].text
  print(message)
  return message