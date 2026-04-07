// ✅ Auto-remove expired JWT before any token operations
(function autoRemoveExpiredToken() {
  const token = localStorage.getItem("access_token");
  if (!token) return;

  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    const isExpired = payload.exp * 1000 < Date.now();
    if (isExpired) {
      console.warn("Token expired. Removing from storage.");
      localStorage.removeItem("access_token");
      alert("Session expired. Please log in again.");
      window.location.href = "/common-login";  // 🔁 Redirect to login page
    }
  } catch (e) {
    console.error("Invalid token. Removing.");
    localStorage.removeItem("access_token");
    alert("Invalid session. Please log in again.");
    window.location.href = "/common-login";
  }
})();

// ✅ Upload setup logic
function setupImageUpload() {
  // Preview image logic
  window.previewImage = (inputId, previewId) => {
    const file = document.getElementById(inputId).files[0];
    const preview = document.getElementById(previewId);
    const reader = new FileReader();

    reader.onload = (e) => {
      preview.src = e.target.result;
      preview.style.display = "block";
    };

    if (file) reader.readAsDataURL(file);
  };

  // Upload image logic
  window.uploadSuspiciousImage = async () => {
    const token = localStorage.getItem("access_token");
    console.log("Sending token:", token);
    if (!token) {
      alert("Please login as Police to continue.");
      return false;
    }

    const fileInput = document.getElementById("imgInput");
    const file = fileInput.files[0];
    const location = document.getElementById("location").value;
    const description = document.getElementById("desc").value;

    if (!file || !location) {
      alert("Image and location are required.");
      return false;
    }

    const formData = new FormData();
    formData.append("image", file);
    formData.append("location", location);
    formData.append("description", description);

    try {
      const res = await fetch("http://localhost:5001/upload", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`
        },
        body: formData
      });

      if (!res.ok) {
        const errorText = await res.text();
        throw new Error(`Error uploading image: ${errorText}`);
      }

      const result = await res.json();
      if (result.predicted_name) {
        alert(`Prediction: ${result.prediction} (Confidence: ${result.confidence.toFixed(2)})`);
      } else {
        alert("Prediction failed or unknown result.");
      }
    } catch (err) {
      console.error(err);
      alert(err.message || "Error uploading image.");
    }

    return false;
  };
}

// ✅ This ensures setup runs when the page loads
document.addEventListener("DOMContentLoaded", () => {
  setupImageUpload();
});
