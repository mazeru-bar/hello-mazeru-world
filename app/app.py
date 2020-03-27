import os, sys
from flask import Flask, flash, request, redirect, url_for, render_template, send_from_directory
from werkzeug.utils import secure_filename
import numpy as np
from PIL import Image
import tensorflow as tf
import random
import json

from keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
from keras.preprocessing import image
from tensorflow.python.keras.backend import set_session

sess = tf.Session()
graph = tf.get_default_graph()
set_session(sess)

# VGG16 を構築する。
model = VGG16()
model.summary()


UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

#Flaskオブジェクトの生成
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def is_allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return redirect(url_for('predict'))

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file.')
            return redirect(url_for('predict'))
        file = request.files['file']
        if file.filename == '':
            flash('No file.')
            return redirect(url_for('predict'))
        if file and is_allowed_file(file.filename):
            filename = secure_filename(file.filename)
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(app.config['UPLOAD_FOLDER']+'/'+filename)
            filepath = app.config['UPLOAD_FOLDER']+'/'+filename

            img = Image.open(filepath).convert('RGB')
            img = img.resize((224, 224))
            x = np.array(img, dtype=np.float32)
            x = x / 255.
            x = x.reshape((1,) + x.shape)

            # ImageNet の日本語のラベルデータを読み込む
            with open('imagenet_class_index.json') as f:
                data = json.load(f)
                class_names = np.array([row['ja'] for row in data])

            global sess
            global graph
            with graph.as_default():
                set_session(sess)
                #scores = model.predict(x, batch_size=1, verbose=0)
                scores = model.predict(x)[0]
                top3_classes = scores.argsort()[-3:][::-1]

                resultmsg = ''
                for name, score in zip(class_names[top3_classes], scores[top3_classes]):
                    resultmsg += '{}: {:.2%}'.format(name, score)

            return render_template('result.html', resultmsg=resultmsg, filepath=filepath)

    return render_template('predict.html')

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    #app.run(debug=True)
    app.run()
