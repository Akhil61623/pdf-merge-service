from flask import Flask, request, render_template_string
import time
from tqdm import tqdm

app = Flask(__name__)

# Home Page (Form Input)
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        file_name = request.form["file_name"]
        target_size = request.form["target_size"]
        part_size = request.form["part_size"]

        # यहाँ आप असली compression/split logic लगा सकते हो
        # अभी सिर्फ demo message दिखा रहा है
        return f"""
        ✅ File: {file_name}<br>
        🎯 Target Compress Size: {target_size} MB<br>
        ✂️ Split Part Size: {part_size} MB<br>
        <br>
        ✅ Operation completed successfully!
        """

    return render_template_string("""
        <h2>📂 File Compressor & Splitter</h2>
        <form method="POST">
            File Name: <input type="text" name="file_name"><br><br>
            Target Size (MB): <input type="number" name="target_size"><br><br>
            Split Size (MB): <input type="number" name="part_size"><br><br>
            <button type="submit">Run</button>
        </form>
    """)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
