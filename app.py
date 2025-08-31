from flask import Flask, request, send_file, jsonify
from pypdf import PdfMerger   # 👈 यह लाइन ऊपर imports में
import io

app = Flask(__name__)

@app.route("/")
def home():
    return "PDF Merge Service Running 🚀"

@app.route("/merge", methods=["POST"])
def merge_pdf():
    try:
        if "files" not in request.files:
            return jsonify({"error": "No PDF files uploaded"}), 400

        files = request.files.getlist("files")

        if len(files) < 2:
            return jsonify({"error": "Please upload at least 2 PDF files"}), 400

        merger = PdfMerger()

        for pdf in files:
            merger.append(pdf)

        output = io.BytesIO()
        merger.write(output)
        merger.close()
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
