async function handleForm(formId, endpoint) {
  const form = document.getElementById(formId);
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(form);
    const response = await fetch(endpoint, { method: "POST", body: formData });
    if (response.ok) {
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = endpoint.replace("/", "") + ".pdf";
      a.click();
    } else {
      alert("Error processing file");
    }
  });
}

handleForm("mergeForm", "/merge");
handleForm("splitForm", "/split");
handleForm("compressForm", "/compress");
handleForm("imgForm", "/img2pdf");
async function handleForm(formId, endpoint) {
  const form = document.getElementById(formId);
  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    const loader = document.getElementById("loader");
    loader.style.display = "block";

    const formData = new FormData(form);
    try {
      const response = await fetch(endpoint, { method: "POST", body: formData });
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = endpoint.replace("/", "") + ".pdf";
        a.click();
      } else {
        alert("Error processing file");
      }
    } catch (err) {
      alert("Server error: " + err.message);
    } finally {
      loader.style.display = "none";
    }
  });
}
