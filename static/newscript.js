

// ✅ Submit user details
async function submitUser() {
  const username = document.getElementById("name").value;
  const number = document.getElementById("number").value;
  const email = document.getElementById("email").value;
  const cnic = document.getElementById("cnic").value;
  // Store user ID in browser for later use in storing results
  localStorage.setItem("cnic", cnic);
  const responseMsg = document.getElementById("responseMsg"); // get the <p> element

  // Input validation
  if (!username || !number || !email || !cnic) {
    responseMsg.textContent = "Please enter all fields!";
    return;
  }
  try {
    const response = await fetch("/add_user", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, number, email, cnic }),
    });

    const data = await response.json();
    console.log("Server response:", data);
    responseMsg.textContent = data.message;

    // ✅ Wait 1 second, then open /questions
    if (response.ok) {
      setTimeout(() => {
        window.location.href = "/questions";
      }, 1000);
    }
  } catch (error) {
    console.error("Error adding user:", error);
    responseMsg.textContent = "Error adding user!";
  }
}
