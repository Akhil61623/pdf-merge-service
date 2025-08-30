import os
from flask import Flask, request, render_template, send_file, jsonify, redirect, url_for
from werkzeug.utils import secure_filename
from PyPDF2 import PdfMerger
import razorpay
import tempfile
import time

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

# Razorpay setup
razorpay_client = razorpay.Client(auth=(
    os.environ.get("RAZORPAY_KEY_ID", ""),
    os.environ.get("RAZORPAY_KEY_SECRET", "")
))

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/merge', methods=['POST'])
def merge_pdfs():
    files = request.files.getlist("pdfs")
    if not files or len(files) == 0:
        return "कृपया PDFs चुनें", 400

    # Size check
    total_size = sum(len(f.read()) for f in files)
    for f in files: f.seek(0)

    # Rules
    if len(files) <= 80 and total_size <= 25 * 1024 * 1024:
        # Free merge → redirect to waiting page
        return render_template("waiting.html", files=len(files))
    else:
        # Razorpay payment required
        order = razorpay_client.order.create({
            "amount": 1000,   # ₹10
            "currency": "INR",
            "payment_capture": 1
        })
        return jsonify({"error": "payment_required", "order_id": order["id"], "amount": 1000})

@app.route('/process_merge', methods=['POST'])
def process_merge():
    files = request.files.getlist("pdfs")
    merger = PdfMerger()
    out_path = os.path.join(app.config['UPLOAD_FOLDER'], "merged.pdf")

    for f in files:
        filename = secure_filename(f.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(file_path)
        merger.append(file_path)

    merger.write(out_path)
    merger.close()

    time.sleep(2)  # waiting effect
    return send_file(out_path, as_attachment=True, download_name="merged.pdf")

@app.route("/healthz")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
