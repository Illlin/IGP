from flask import Flask, jsonify, request, render_template, send_from_directory
from ibm_bridge import get_emotion
from cube import emotion_cube
import os

build_dir = "../FrontEnd/build/"

app = Flask(
    __name__,
    static_url_path="", 
    template_folder=build_dir, 
    static_folder=build_dir
    )

# Dummy Data
formats = ["wav"]
dummy = {"file": os.path.join("FlaskServer","cach","model.stl")}
fail = {"file": ""}

save_loc = os.path.join("cache", "audio.wav")
out_loc = os.path.join("cache", "model.stl")

@app.route('/api/sculpt', methods=['POST'])
def wav_to_model():
    if 'file' not in request.files:
        return jsonify(fail), 400

    # Load file from request
    file = request.files['file']

    if not (file and allowed_file(file.filename)):
        # No valid file attached
        return jsonify(fail), 400

    # All validations passed, proced

    print(type(file))
    file.save(save_loc)
    emotion, time_stamps = get_emotion(save_loc)
    emotion_cube(save_loc, out_loc, emotion)

    # Process the data to make the model
    data = dummy
    
    return jsonify(data), 200


# Check if a given file is valid
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in formats


# Server static site
@app.route('/')
def serve():
    print("Hello")
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)