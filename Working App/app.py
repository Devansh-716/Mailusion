from flask import Flask, request, render_template
import subprocess
import os

app = Flask(__name__)
UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__))

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html") 

@app.route("/upload", methods=["POST"]) 
def upload():
    excel = request.files["data"]
    csv = request.files["body_subject"]

    if excel.filename and csv.filename:
        excel.save(os.path.join(UPLOAD_FOLDER, "data.xlsx")) 
        csv.save(os.path.join(UPLOAD_FOLDER, "body_subject.csv"))

        # Run main.py and capture output
        result = subprocess.run(["python", "main.py"], capture_output=True, text=True)

        return f"""
        <h2>Files uploaded and emails sent.</h2>
        <h3>stdout:</h3><pre>{result.stdout}</pre>
        <h3>stderr:</h3><pre>{result.stderr}</pre>
        """

    return "<h2>Error: Please upload both files.</h2>"

if __name__ == "__main__":
    app.run(debug=True)
