from flask import Flask, jsonify, request

app = Flask(__name__)

# Dummy Data
formats = ["wav"]
dummy = {"file": "FrontEnd/src/Datastore/Happy V1.stl"}
fail = dummy = {"file": ""}


@app.route('/api/sculpt', methods=['POST'])
def wav_to_model():
    # Check if file present
    if 'file' not in request.files:
        return jsonify(fail), 400

    # Load file from request
    file = request.files['file']

    if not (file and allowed_file(file.filename)):
        # No valid file attached
        return jsonify(fail), 400

    # All validations passed, proced

    # Process the data to make the model
    data = dummy
    
    return jsonify(data), 200


# Check if a given file is valid
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in formats

# Function for root URL
@app.route("/")
def hello():
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True)
    print("Fish bish")