<!DOCTYPE html>
<html lang="hi">
<head>
  <meta charset="UTF-8">
  <title>महामाया स्टेशनरी — PDF Merge Service</title>
  <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
  <style>
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: #f9f9f9;
      margin: 0;
      padding: 0;
      text-align: center;
    }
    header {
      background-color: #4a7c59;
      color: white;
      padding: 20px 0;
      font-size: 1.8rem;
      font-weight: bold;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .container {
      max-width: 600px;
      margin: 40px auto;
      background: white;
      padding: 30px;
      border-radius: 8px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    .dropzone {
      border: 2px dashed #4a7c59;
      border-radius: 8px;
      padding: 40px;
      position: relative;
      cursor: pointer;
      transition: background 0.2s;
    }
    .dropzone:hover {
      background: #f0f8f0;
    }
    .dropzone input {
      position: absolute;
      width: 100%;
      height: 100%;
      opacity: 0;
      cursor: pointer;
    }
    .dropzone p {
      margin: 0;
      font-size: 1.1rem;
      color: #333;
    }
    button {
      background-color: #4a7c59;
      color: white;
      border: none;
      padding: 12px 24px;
      border-radius: 6px;
      font-size: 1rem;
      cursor: pointer;
      transition: background 0.2s;
      margin-top: 20px;
    }
    button:hover {
      background-color: #3d6548;
    }
    .loader {
      display: none;
      margin: 20px auto;
      border: 8px solid #f3f3f3;
      border-top: 8px solid #4a7c59;
      border-radius: 50%;
      width: 60px;
      height: 60px;
      animation: spin 1s linear infinite;
    }
    @keyframes spin { 100% { transform: rotate(360deg); } }
  </style>
</head>
<body>

  <header>महामाया स्टेशनरी</header>

  <div class="container">
    <div class="dropzone" id="dropzone">
      <p>यहाँ क्लिप करें या ड्रैग करें PDF फाइलें</p>
      <input type="file" id="fileInput" name="files" accept="application/pdf" multiple>
    </div>
    <button id="mergeButton">Merge and Download</button>
    <div class="loader" id="loader"></div>
  </div>

  <script>
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('fileInput');
    const mergeButton = document.getElementById('mergeButton');
    const loader = document.getElementById('loader');

    let selectedFiles = [];

    dropzone.addEventListener('dragover', (e) => {
      e.preventDefault();
      dropzone.style.background = '#eafdee';
    });

    dropzone.addEventListener('dragleave', () => {
      dropzone.style.background = '';
    });

    dropzone.addEventListener('drop', (e) => {
      e.preventDefault();
      dropzone.style.background = '';
      handleFiles(e.dataTransfer.files);
    });

    fileInput.addEventListener('change', (e) => {
      handleFiles(e.target.files);
    });

    function handleFiles(files) {
      selectedFiles = Array.from(files);
      dropzone.querySelector('p').innerText = `${selectedFiles.length} file(s) selected`;
    }

    mergeButton.addEventListener('click', async () => {
      if (!selectedFiles.length) return alert('कृपया कम से कम एक PDF फाइल चुनें');

      let totalSize = selectedFiles.reduce((acc, f) => acc + f.size, 0);
      if (selectedFiles.length > 80 || totalSize > 25 * 1024 * 1024) {
        loader.style.display = 'none';
        return alert('Limit exceeded: ₹10 charge apply.\n(Implementation with Razorpay popup)');
      }

      const formData = new FormData();
      selectedFiles.forEach(f => formData.append('files', f));

      loader.style.display = 'block';
      mergeButton.disabled = true;

      // AJAX call to /merge endpoint
      try {
        let response = await fetch('/merge', { method: 'POST', body: formData });
        if (response.ok) {
          const blob = await response.blob();
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = 'merged.pdf';
          document.body.appendChild(a);
          a.click();
          a.remove();
        } else {
          const err = await response.json();
          alert(err.error || 'कुछ गड़बड़ हुई');
        }
      } catch (err) {
        console.error(err);
        alert('Server error');
      }

      loader.style.display = 'none';
      mergeButton.disabled = false;
    });
  </script>

</body>
</html>
