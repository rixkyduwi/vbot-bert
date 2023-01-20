import random,string,json
from certifi import where
from flask import Flask,jsonify, request, render_template
from bert import bert_prediction,db,HISTORY,app
from werkzeug.security import check_password_hash,generate_password_hash
from flask_restful import Resource, Api
from flask_httpauth import HTTPTokenAuth
from flask_cors import CORS
auth = HTTPTokenAuth(scheme='Bearer')
api = Api(app)
class ADMIN(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    token = db.Column(db.String(1000))
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
        user="rizky"
        print(user)
        question = request.args.get('pertanyaan')
        print(question)
        prediction = bert_prediction(user,str(question))
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
CORS(app)
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000,debug=True)