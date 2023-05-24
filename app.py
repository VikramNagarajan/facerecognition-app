from flask import Flask, render_template, url_for, flash, redirect, request, send_from_directory, flash
from werkzeug.utils import secure_filename
import os
import face_recognition
from PIL import Image
import os
from pathlib import Path
import pickle
from collections import Counter


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(12)
app.config['UPLOAD_FOLDER'] = 'static/uploadedFiles'
DEFAULT_ENCODINGS_PATH = 'encodings.pkl'
ALLOWED_EXTENSIONS = {'png' , 'jpg', 'jpeg', 'pgm'}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/demo', methods=['GET', 'POST'])
def demo():
    return render_template('demo.html')

def _recognize_face(unknown_encoding, loaded_encodings):
    """
    Given an unknown encoding and all known encodings, find the known
    encoding with the most matches.
    """
    boolean_matches = face_recognition.compare_faces(
        loaded_encodings["encodings"], unknown_encoding
    )
    votes = Counter(
        name
        for match, name in zip(boolean_matches, loaded_encodings["names"])
        if match
    )
    if votes:
        return votes.most_common(1)[0][0]
#encode_known_faces()

def recognize_faces(
    image_location: str,
    model: str = "hog",
    encodings_location: Path = DEFAULT_ENCODINGS_PATH,
) -> None:
    """
    Given an unknown image, get the locations and encodings of any faces and
    compares them against the known encodings to find potential matches.
    """

    with open(encodings_location, 'rb') as f:
        loaded_encodings = pickle.load(f)

    input_image = face_recognition.load_image_file(image_location)
    try:
        name = _recognize_face(face_recognition.face_encodings(input_image)[0], loaded_encodings)
        return name
    except:
        return 0


@app.route('/demoResult', methods=['GET', 'POST'])
def demoResult():
    if request.method == 'POST':
        if request.files:
            f = request.files['file']
            filePath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename))
            try:
                f.save(filePath)
                label = recognize_faces(filePath)
                labelsToPeople = {'s0': 'Rohan Reddy', 's1': 'Yi-Fei Zhao', 's2': 'Pradyun Solai', 's3': 'Helen Mao', 's4': 'Raj Ginde', 's5': 'Venkie Subramanyam', 's6': 'Samhita Gudapati', 's7': 'Amanda Hulver', 's8': 'Adi Mallik', 's9': 'Kevin Mao', 's10': 'Aditya Mallepalli', 's11' : 'Harron Lee', 's12': 'Matthew Wei',}
                labelToName='None'
                if label!=0:
                    labelToName = labelsToPeople[label]
                return render_template('demoResult.html', fileName='uploadedFiles/' + f.filename, label=labelToName)
            except:
                flash("Our AI can't see any faces in your image.")
                return render_template('demoResult.html')
    return render_template('demoResult.html')


if __name__ == '__main__':
    app.run(debug=True)

