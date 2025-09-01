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
  if (!selectedFiles.length) return alert('Please select PDF files');

  const formData = new FormData();
  selectedFiles.forEach(f => formData.append('files', f));

  loader.style.display = 'block';
  mergeButton.disabled = true;

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
      alert(err.error || 'Something went wrong');
    }
  } catch (err) {
    alert('Server error: ' + err.message);
  }

  loader.style.display = 'none';
  mergeButton.disabled = false;
});
let response = await fetch('/merge', { method: 'POST', body: formData });
