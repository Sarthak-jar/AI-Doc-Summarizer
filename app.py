from flask import Flask, request, render_template
import os
from summarizer import summarize_text
from extractors import extract_text_from_pdf, extract_text_from_docx

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    summary = ""
    if request.method == "POST":
        uploaded_file = request.files["document"]
        if uploaded_file:
            path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
            uploaded_file.save(path)

            if path.endswith(".pdf"):
                text = extract_text_from_pdf(path)
            elif path.endswith(".docx"):
                text = extract_text_from_docx(path)
            else:
                text = uploaded_file.read().decode()

            summary = summarize_text(text)
    return render_template("index.html", summary=summary)

if __name__ == "__main__":
    app.run(debug=True)
