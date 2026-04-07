document.getElementById("uploadForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const token = localStorage.getItem("access_token");
  if (!token) {
    alert("Please login first.");
    localStorage.setItem("redirect_after_login", window.location.href);
    window.location.href = "common-login";
    return;
  }

  const fileInput = document.getElementById("imgInput");
  const location = document.getElementById("location").value;
  const description = document.getElementById("desc").value;
  const lastSeen = document.getElementById("lastSeen").value;

  if (!fileInput.files || fileInput.files.length === 0) {
    alert("Please select an image file.");
    return;
  }

  const formData = new FormData();
  formData.append("image", fileInput.files[0]);
  formData.append("location", location);
  formData.append("description", description);
  formData.append("last_seen", lastSeen);

  try {
    const response = await fetch("http://localhost:5001/upload-suspicious", {
      method: "POST",
      headers: {
        "Authorization": "Bearer " + token
      },
      body: formData
    });

    const responseText = await response.text();
    let data;

    try {
      data = JSON.parse(responseText);
    } catch (jsonErr) {
      console.error("Server returned non-JSON:", responseText);
      alert("Upload failed: Server error.");
      return;
    }

    if (response.ok) {

      const confidenceValue = parseFloat(data.confidence);
      const confidenceText = !isNaN(confidenceValue)
        ? confidenceValue.toFixed(2)
        : "N/A";

      const resultText = document.getElementById("result");
      const imgPreview = document.getElementById("imgPreview");

      if (data.match_found) {

        resultText.textContent =
          `✅ Match Found: ${data.person_name} (Confidence: ${confidenceText})`;

        // show matched person's image
        if (data.photo_path) {
          imgPreview.src = `/static/uploads/${data.photo_path}`;
          imgPreview.style.display = "block";
        }

      } else {

        resultText.textContent =
          `❌ No match found. Similarity: ${confidenceText}`;

        imgPreview.style.display = "none";
      }

    } else {
      alert("Error uploading image: " + (data.error || "Unknown error"));
      document.getElementById("result").textContent =
        "Upload failed: " + (data.error || "Unknown error");
    }

  } catch (err) {
    console.error("Fetch error:", err);
    alert("Upload failed: " + err.message);
  }
});