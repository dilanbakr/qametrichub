from flask import Flask, render_template, request, json, jsonify, send_file, redirect
from io import BytesIO
import numpy as np
from bson.json_util import dumps
from storage.mongotracer import MongoTracer
from storage.miniorepo import MinioRepo
import yaml
from datetime import datetime
import uuid
from storage.postgreconnetion import get_data, update_data, login_user
import os
# importing necessary functions from dotenv library
from dotenv import load_dotenv, dotenv_values
# loading variables from .env file
load_dotenv()

app = Flask(__name__)


def load_model(path):
    a = np.load(path)
    weights = []
    for i in range(len(a.files)):
        weights.append(a[str(i)])
    return weights


with open('settings.yaml', 'r') as fh:
    try:
        settings = dict(yaml.safe_load(fh))
    except yaml.YAMLError as e:
        raise e


@app.route('/predict')
def predict():
    try:
        minio = MinioRepo(settings)
        global_model_list = minio.get_global_model_list(settings['bucket'])
        return render_template('predict.html', global_model_list=global_model_list)
    except:
        raise Exception("Ops, Could not connect to minio, make sure to run FEDn base services!")


@app.route('/testing')
def testing():
    try:
        minio = MinioRepo(settings)
        global_model_list = minio.get_global_model_list(settings['bucket'])
        predict_answer = "The Apollo program, also known as Project Apollo, was the third United States human spaceflight program "

        real_answer = "The Apollo program, also known as Project Apollo, was the third United States human spaceflight program "


        return render_template('testing.html', global_model_list=global_model_list,
                               predict_answer=predict_answer, real_answer=real_answer)
    except:
        raise Exception("Ops, Could not connect to minio, make sure to run FEDn base services!")



@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/global-models")
def global_models():
    try:
        minio = MinioRepo(settings)
        global_model_list = minio.get_object_list(settings['bucket'])
        return render_template('global_models.html', global_model_list=global_model_list)
    except:
        raise Exception("Ops, Could not connect to minio, make sure to run FEDn base services!")

@app.route('/getdata_test')
def getdata_test():
    print("gett yeni girdi")
    user_id = request.args.get('userid')
    print("userid: ", user_id)
    paragraf, question, realanswer, predictanswer, id = get_data(user_id)
    data = { 'paragraf': paragraf, 'question': question,  "realanswer" : realanswer, "predictanswer": predictanswer, "id": id }
    print(data)
    return data

@app.route('/active-learning', methods=['GET','POST'])
def active_learning():
    print(request.method)
    if request.method == "GET":
        user_id = request.args.get('userid')
        print("get girdi")
        print("user id: ", user_id)
        paragraf, question, realanswer, predictanswer, id = get_data(user_id)
        data = {'paragraf': paragraf, 'question': question,  "realanswer" : realanswer, "predictanswer": predictanswer, "id": id, "userid": user_id}
        print(data)
        # İhtiyaca göre diğer alanlar da eklenebilir
        return render_template('annotator.html', data=data)
    elif request.method == "POST":
        try:
            # POST isteği için veriyi al
            data = request.get_json()
            print("data: ", data)
            print("posta girdi")
            print(data)
            paragraph = data.get('paragraph')
            question = data.get('question')
            realanswer = data.get('realanswer')
            predictanswer = data.get('predictanswer')

            #anket
            question1 = data.get('question1')
            question2 = data.get('question2')
            question3 = data.get('question3')
            question4 = data.get('question4')
            question5 = data.get('question5')
            question6 = data.get('question6')
            question7 = data.get('question7')
            question8 = data.get('question8')
            id = data.get('id')
            user_id = data.get('userid')

            print("id: ", id)
            print(update_data(question1 , question2, question3, question4, question5, question6, question7, question8,id))

            print("user id: ", user_id)
            paragraf, question, realanswer, predictanswer, id = get_data(user_id)
            data = {'paragraf': paragraf, 'question': question,  "realanswer" : realanswer, "predictanswer": predictanswer, "id": id, "userid": user_id}
            print(data)
            # İhtiyaca göre diğer alanlar da eklenebilir
            return render_template('annotator.html', data=data)

        except Exception as e:
            # Hata durumunda hata mesajını gönder
            return jsonify({'error': str(e)})

@app.route('/category-labeling', methods=['GET','POST'])
def category_labeling():
    print(request.method)
    if request.method == "GET":
        user_id = request.args.get('userid')
        print("get girdi")
        print("user id: ", user_id)
        paragraf, question, realanswer, predictanswer, id = get_data(user_id)
        data = {'paragraf': paragraf, 'question': question,  "realanswer" : realanswer, "id": id, "userid": user_id}
        print(data)
        # İhtiyaca göre diğer alanlar da eklenebilir
        return render_template('annotator2.html', data=data)

@app.route('/', methods=['GET','POST'])
def login():
    print(request.method)
    if request.method == "GET":
        return render_template('login.html')
    elif request.method == "POST":

        print("posta girdi")
        data = request.get_json()
        username = data.get('username')
        password = data.get('pass')
        userid = login_user(username, password)
        #paragraf, question, realanswer, predictanswer, id = get_data(userid)
        data = {'userid': userid}
        print(data)
        return data

document = {
    'title': 'title here',
    'paragraphs': [],
}


if __name__ == "__main__":
    app.run(host='0.0.0.0')
