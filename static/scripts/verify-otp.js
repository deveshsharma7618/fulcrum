form = document.getElementById("otp-form");
const login_user = (email,password)=>{

}

document.onload = function() {
  const email = localStorage.getItem("email");
  const password = localStorage.getItem("password");
  if(login_user(email,password)){
    window.location.href = "/";
  }else{
    localStorage.clear();
  }
}

form.onsubmit = async function (event) {
  event.preventDefault();
  const otp = form.elements["otp"].value;
  const username = form.elements["username"].value;
  const current_study_year = form.elements["current_study_year"].value;
  const hostel_no = form.elements["hostel_no"].value;
  const clubs = form.elements["clubs"].value;
  const password = form.elements["password"].value;
  const formData = {
    otp: otp,
    username: username,
    current_study_year: current_study_year,
    hostel_no: hostel_no,
    clubs: clubs,
    password: password,
  };
  const email = localStorage.getItem("email");

  formData["email"] = email;
  const response = await fetch("/verify-otp", {
    method: "POST",
    headers: {
      Accept: "application/json, text/plain, */*",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(formData),
  });
  const result = await response.json();
  console.log(typeof result);
  if(result.status===200){
    localStorage.setItem("username", username);
    localStorage.setItem("email", email);
    localStorage.setItem("current_study_year", current_study_year);
    localStorage.setItem("hostel_no", hostel_no);
    localStorage.setItem("clubs", clubs);
    window.location.href = "/";

  } else {
    alert("Something went wrong. Please try again.");
  }
};
