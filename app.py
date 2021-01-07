import os
from flask import Flask, request, render_template, redirect, flash, url_for
from flask import send_from_directory
from werkzeug.utils import secure_filename

import librosa,matplotlib.pyplot as plt
import IPython.display as ipd
from findgenre import findg


app = Flask(__name__)
UPLOAD_FOLDER = './tmp'
UPLOAD_FOLDERB = './static/audio'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'jpg'}


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_FOLDERB'] = UPLOAD_FOLDERB


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
            file.save(os.path.join(app.config['UPLOAD_FOLDERB'], filename))
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
        if os.path.exists("tmp/abc.wav"):
            os.remove("tmp/abc.wav")
        if os.path.exists("static/audio/abc.wav"):
            os.remove("static/audio/abc.wav")

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
            file.save(os.path.join(app.config['UPLOAD_FOLDERB'], filename))
            #file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'abc.wav'))
            source = UPLOAD_FOLDER + "/" + filename
            destination = UPLOAD_FOLDER + "/" + "abc.wav"
            os.rename(source, destination)
            sourceb = UPLOAD_FOLDERB + "/" + filename
            destinationb = UPLOAD_FOLDERB + "/" + "abc.wav"
            os.rename(sourceb, destinationb)
            # return redirect(url_for('uploaded_file', filename='abc.wav'))
            genre = findg()
            print(genre)
            return redirect(url_for('result', filename=filename, genre=genre))

@app.route('/result/<string:filename>/<int:genre>')
def result(filename, genre):
    if genre == 0:
        genre = 'Blues'
    elif genre == 1:
        genre = 'Classical'
    elif genre == 2:
        genre = 'Country'
    elif genre == 3:
        genre = 'Disco'
    elif genre == 4:
        genre = 'Hiphop'
    elif genre == 5:
        genre = 'Jazz'
    elif genre == 6:
        genre = 'Metal'
    elif genre == 7:
        genre = 'Pop'
    elif genre == 8:
        genre = 'Reggae'
    elif genre == 9:
        genre = 'Rock'
    return render_template('result.html', filename=filename, genre=genre)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
