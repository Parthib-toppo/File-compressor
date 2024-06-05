import os
from flask import Flask, render_template, request, redirect, url_for, send_file
from huffman import compress_file

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
COMPRESSED_FOLDER = 'compressed'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['COMPRESSED_FOLDER'] = COMPRESSED_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(COMPRESSED_FOLDER):
    os.makedirs(COMPRESSED_FOLDER)

@app.route('/', methods = ['GET','POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file.filename == '':
            return "<h1> no selected file <h1>"
        else:
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'],filename)
            file.save(file_path)

            compressed_file_path = os.path.join(app.config['COMPRESSED_FOLDER'], "compressed.cumload")
            compress_file(file_path,compressed_file_path)

            return send_file(compressed_file_path, as_attachment=True, download_name = "compressed.cumload")

    else:
        return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)