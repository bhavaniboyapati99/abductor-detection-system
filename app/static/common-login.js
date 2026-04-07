document.getElementById("loginForm").addEventListener("submit", async function (e) {
  e.preventDefault();

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;

  try {
    const response = await fetch("http://127.0.0.1:5001/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ username, password })
    });

    const data = await response.json();

    if (response.ok) {
      // Save JWT token in localStorage
      localStorage.setItem("token", data.access_token);
      // Redirect to upload page or dashboard
      window.location.href = "upload-image.html";
    } else {
      document.getElementById("loginError").textContent = data.msg || "Login failed";
    }
  } catch (err) {
    document.getElementById("loginError").textContent = "Login error: " + err.message;
    console.error("Login failed:", err);
  }
});
