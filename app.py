from flask import Flask, request, jsonify, render_template
import fitz  # PyMuPDF
from gemini_handler import gemini_summarize

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/summarize', methods=['POST'])
def summarize_doc():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if not file:
        return jsonify({'error': 'Empty file'}), 400

    # Read PDF content
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()

    summary = gemini_summarize(text)
    return jsonify({'summary': summary})

if __name__ == '__main__':
    app.run(debug=True)
