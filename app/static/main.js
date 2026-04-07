// main.js

// Function to preview image before uploading
function previewImage(inputId, previewId) {
    const file = document.getElementById(inputId).files[0];
    const preview = document.getElementById(previewId);

    const reader = new FileReader();

    reader.onload = function(e) {
        preview.src = e.target.result;
        preview.style.display = "block";
    };

    if (file) {
        reader.readAsDataURL(file);
    }
}


// Function to validate form submission
function validateForm() {
    const fileInput = document.getElementById('imgInput');
    const locationInput = document.getElementById('location');

    if (!fileInput || !fileInput.files.length) {
        alert("Please select an image to upload.");
        return false;
    }

    if (!locationInput || !locationInput.value.trim()) {
        alert("Please enter location.");
        return false;
    }

    return true;
}