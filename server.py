# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, Response
import run_web
import os
from datetime import datetime as dt

app = Flask(__name__)

# template route
@app.route('/')
def index():
  return render_template('index.html')

# api route
@app.route('/api/estimator', methods=["POST"])
def estimator():
  # imageのリクエストを受けて保存
  image = request.files["img"]
  file_name = dt.now().strftime('%Y%m%d%H%M%S') + '.png'
  image.save(os.path.join('./img/', file_name))
  # OpenPoseに投げる
  image = run_web.run(file_name)
  # OpenPose側で出力された画像を返す
  f = open('./img/' + file_name, 'rb')
  image = f.read()
  os.remove(os.path.join('./img/', file_name))
  return Response(response=image, content_type='image/png')

if __name__ == "__main__":
  app.run("127.0.0.1", debug=True)
