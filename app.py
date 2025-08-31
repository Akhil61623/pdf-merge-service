from flask import Flask, request, send_file, jsonify
from pypdf import PdfReader, PdfWriter
import io

app = Flask(__name__)

@app.route("/")
def home():
    return "🚀 PDF Merge Service is running"

@app.route("/merge", methods=["POST"])
def merge_pdfs():
    try:
        if "files" not in request.files:
            return jsonify({"error": "No PDF files uploaded"}), 400

        files = request.files.getlist("files")

        if len(files) < 2:
            return jsonify({"error": "Please upload at least 2 PDF files"}), 400

        writer = PdfWriter()

        # हर PDF को पढ़कर add करना
        for pdf in files:
            reader = PdfReader(pdf)
            for page in reader.pages:
                writer.add_page(page)

        # Output को memory में save करना
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
