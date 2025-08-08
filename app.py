from flask import Flask, request, render_template, flash, redirect, url_for
import os
from werkzeug.utils import secure_filename

# Import your upgraded functions
from summarizer import summarize_text
from extractors import extract_text_from_pdf, extract_text_from_docx, extract_text_from_txt

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'supersecretkey' # Needed for flash messages

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """Checks if the file has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Check if the post request has the file part
        if 'document' not in request.files:
            flash('No file part in the request.')
            return redirect(request.url)
        
        file = request.files['document']
        
        # If the user does not select a file, the browser submits an empty file without a filename.
        if file.filename == '':
            flash('No selected file.')
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            # Use a secure filename to prevent security issues
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            text = ""
            try:
                if filename.endswith(".pdf"):
                    text = extract_text_from_pdf(filepath)
                elif filename.endswith(".docx"):
                    text = extract_text_from_docx(filepath)
                elif filename.endswith(".txt"):
                    text = extract_text_from_txt(filepath)
                
                if not text.strip():
                    flash('Could not extract text from the document. It might be empty or scanned.')
                    return render_template("index.html", summary=None, filename=filename)

                # Generate the summary
                summary = summarize_text(text)
                
                # Render the result on the same page
                return render_template("index.html", summary=summary, filename=filename)

            except Exception as e:
                flash(f"An error occurred: {e}")
                return redirect(request.url)

        else:
            flash('Invalid file type. Please upload a .txt, .pdf, or .docx file.')
            return redirect(request.url)

    # For GET requests
    return render_template("index.html", summary=None, filename=None)

if __name__ == "__main__":
    app.run(debug=True)