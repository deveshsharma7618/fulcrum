loginForm = document.getElementById("login-form");
loginForm.onsubmit = async function (event) {
  event.preventDefault();
  const email = loginForm.elements["email"].value;
  const password = loginForm.elements["password"].value;
  const formData = {
    email: email,
    password: password
  };
  console.log(formData);

  const response = await fetch("/login", {
    method: "POST",
    headers: {
      Accept: "application/json, text/plain, */*",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formData),
  });
  const result = await response.json();

  if(result.status!==200){
    alert("Invalid Credentials. Please try again.");
    return;
  }else{
    console.log(result);
    localStorage.setItem("email", email);
    localStorage.setItem("access_token", result.access_token);
    localStorage.setItem("username", result.username);
    localStorage.setItem("hostel_no", result.hostel_no);
    localStorage.setItem("clubs", result.clubs);
    localStorage.setItem("roll_no", result.roll_no);
    localStorage.setItem("current_study_year", result.current_study_year);
    window.location.href = "/";
  }
};

window.onload = () => {
  if (typeof checkAuthorized === "function" && checkAuthorized()) {
    window.location.href = "/";
  }
};