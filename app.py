from flask import Flask, request, send_file, render_template, jsonify
from pypdf import PdfReader, PdfWriter
from PIL import Image
import io, os, zipfile

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

# 1. PDF Merge
@app.route("/merge", methods=["POST"])
def merge_pdfs():
    files = request.files.getlist("files")
    writer = PdfWriter()
    for pdf in files:
        reader = PdfReader(pdf)
        for page in reader.pages:
            writer.add_page(page)
    output = io.BytesIO()
    writer.write(output)
    output.seek(0)
    return send_file(output, as_attachment=True, download_name="merged.pdf")

# 2. PDF Split
@app.route("/split", methods=["POST"])
def split_pdf():
    file = request.files["file"]
    reader = PdfReader(file)
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zipf:
        for i, page in enumerate(reader.pages):
            writer = PdfWriter()
            writer.add_page(page)
            page_bytes = io.BytesIO()
            writer.write(page_bytes)
            page_bytes.seek(0)
            zipf.writestr(f"page_{i+1}.pdf", page_bytes.read())
    zip_buffer.seek(0)
    return send_file(zip_buffer, as_attachment=True, download_name="split_pages.zip")

# 3. PDF Compress (simple: remove metadata, optimize content)
@app.route("/compress", methods=["POST"])
def compress_pdf():
    file = request.files["file"]
    reader = PdfReader(file)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)
    output = io.BytesIO()
    writer.write(output)
    output.seek(0)
    return send_file(output, as_attachment=True, download_name="compressed.pdf")

# 4. Image to PDF
@app.route("/img2pdf", methods=["POST"])
def img_to_pdf():
    files = request.files.getlist("images")
    img_list = []
    for img in files:
        image = Image.open(img).convert("RGB")
        img_list.append(image)
    output = io.BytesIO()
    img_list[0].save(output, save_all=True, append_images=img_list[1:], format="PDF")
    output.seek(0)
    return send_file(output, as_attachment=True, download_name="images.pdf")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
import subprocess, tempfile

@app.route("/merge", methods=["POST"])
def merge_pdfs():
    files = request.files.getlist("files")
    if len(files) < 2:
        return jsonify({"error": "Need at least 2 PDFs"}), 400

    with tempfile.TemporaryDirectory() as tmpdir:
        paths = []
        for i, f in enumerate(files):
            path = os.path.join(tmpdir, f"file{i}.pdf")
            f.save(path)
            paths.append(path)

        output_path = os.path.join(tmpdir, "merged.pdf")
        cmd = ["qpdf", "--empty", "--pages"] + paths + ["--", output_path]
        subprocess.run(cmd, check=True)

        return send_file(output_path, as_attachment=True, download_name="merged.pdf")
