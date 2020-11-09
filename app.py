import os
from flask import Flask, request, render_template, redirect, flash, url_for
from werkzeug.utils import secure_filename

import librosa,matplotlib.pyplot as plt
import IPython.display as ipd


app = Flask(__name__)
UPLOAD_FOLDER = './tmp'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'jpg'}


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/home')
def templatetest():
    return render_template('home.html')


@app.route('/uploadcheck', methods=['GET', 'POST'])
def upload_file_check():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action=http://localhost:5000/uploadcheck method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''



@app.route('/test')
def test():
    audio_path = 'music/Data/genres_original/classical/classical.00000.wav'
    x, sr = librosa.load(audio_path, sr=44100)
    print(type(x), type(sr))
    print(x.shape, sr)

    return ipd.Audio(audio_path)


@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('home'))
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for('home'))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
