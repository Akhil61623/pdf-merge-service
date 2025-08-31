from flask import Flask, request, send_file, render_template, jsonify
from pypdf import PdfReader, PdfWriter
import io, os
import razorpay

app = Flask(__name__)

# Razorpay Client
razorpay_client = razorpay.Client(auth=(os.getenv("RAZORPAY_KEY_ID"), os.getenv("RAZORPAY_KEY_SECRET")))

FREE_FILE_LIMIT = 80
FREE_SIZE_LIMIT_MB = 25

@app.route("/")
def home():
    return render_template("index.html", razorpay_key=os.getenv("RAZORPAY_KEY_ID"))

@app.route("/create-order", methods=["POST"])
def create_order():
    data = request.get_json()
    amount = data.get("amount", 10) * 100  # INR to paisa
    order = razorpay_client.order.create({"amount": amount, "currency": "INR", "payment_capture": 1})
    return jsonify(order)

@app.route("/merge", methods=["POST"])
def merge_pdfs():
    try:
        if "files" not in request.files:
            return jsonify({"error": "No PDF files uploaded"}), 400

        files = request.files.getlist("files")
        total_size = sum(len(f.read()) for f in files)
        for f in files:
            f.seek(0)  # reset pointer

        # Check free limit
        if len(files) > FREE_FILE_LIMIT or total_size > FREE_SIZE_LIMIT_MB * 1024 * 1024:
            return jsonify({"payment_required": True, "message": "Limit exceeded. Please pay ₹10"}), 402

        writer = PdfWriter()
        for pdf in files:
            reader = PdfReader(pdf)
            if reader.is_encrypted:
                return jsonify({"error": f"File {pdf.filename} is password protected"}), 400
            for page in reader.pages:
                writer.add_page(page)

        output = io.BytesIO()
        writer.write(output)
        writer.close()
        output.seek(0)

        return send_file(
            output,
            as_attachment=True,
            download_name="merged.pdf",
            mimetype="application/pdf"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500
