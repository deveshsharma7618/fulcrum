createAccountForm = document.getElementById("create-account-form");
createAccountForm.onsubmit = async function (event) {
  event.preventDefault();
  const email = createAccountForm.elements["email"].value;
  localStorage.setItem("email", email);
  const formData = {
    email: email,
  };
  console.log(formData);

  const response = await fetch("/create-account", {
    method: "POST",
    headers: {
      Accept: "application/json, text/plain, */*",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formData),
  });
  const result = await response.text();
  console.log(result);
  window.location.href = "/verify-otp";
};
