from flask import Flask, request, send_file, render_template, jsonify
from pypdf import PdfReader, PdfWriter
import io

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/merge", methods=["POST"])
def merge_pdfs():
    try:
        if "files" not in request.files:
            return jsonify({"error": "No PDF files uploaded"}), 400

        files = request.files.getlist("files")

        if len(files) < 2:
            return jsonify({"error": "Please upload at least 2 PDF files"}), 400

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
