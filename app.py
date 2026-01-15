from flask import Flask, render_template, request, send_file
import pdfplumber
from docx import Document
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("pdf")
        if not file:
            return "No file uploaded"

        pdf_path = os.path.join(UPLOAD_FOLDER, f"{uuid.uuid4()}.pdf")
        docx_path = pdf_path.replace(".pdf", ".docx")

        file.save(pdf_path)

        doc = Document()
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    doc.add_paragraph(text)

        doc.save(docx_path)

        return send_file(docx_path, as_attachment=True)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
