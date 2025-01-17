import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1' 
import tensorflow as tf

from flask import Flask, request, redirect, render_template, flash
from werkzeug.utils import secure_filename
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.preprocessing import image
#from tensorflow.python.keras import utils
#aaa
import numpy as np

classes = ["0","1","2","3","4","5","6","7","8","9"]
image_size = 28

UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.secret_key = "12345"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

model = load_model('./model.h5', compile=False)#学習済みモデルをロード


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('ファイルがありません')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('ファイルがありません')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            filepath = os.path.join(UPLOAD_FOLDER, filename)

            #受け取った画像を読み込み、np形式に変換
            print(filepath)
            img = image.load_img(filepath, target_size=(image_size,image_size), color_mode="grayscale")
            #img = image.load_img(filepath, grayscale=True, target_size=(image_size,image_size))
            #print(img)
            img = image.img_to_array(img)
            #print(img)
            data = np.array([img])
            print(data.shape)
            #変換したデータをモデルに渡して予測する
            result = model.predict(data)[0]
            #print(result)
            predicted = result.argmax()
            print(predicted)
            pred_answer = "これは " + classes[predicted] + " です"

            return render_template("index.html",answer=pred_answer)

    return render_template("index.html",answer="")


if __name__ == "__main__":
#    app.run()
    port = int(os.environ.get('PORT', 8080))
    app.run(host ='0.0.0.0',port = port)