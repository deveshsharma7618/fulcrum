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
    localStorage.setItem("email", email);
    localStorage.setItem("api_key", password);
    window.location.href = "/";
  }
};
