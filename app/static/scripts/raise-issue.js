const form = document.querySelector('form#raise-issue');

form.onsubmit = async function (event) {
    event.preventDefault();
    const issue = form.elements["issue"].value;
    const access_token = localStorage.getItem("access_token");
    const email = localStorage.getItem("email");
    const formData = {
        issue: issue,
        email: email,
        access_token: access_token
    };
    console.log(formData);
    const response = await fetch("/raise-issue", {
        method: "POST",
        headers: {
            Accept: "application/json, text/plain, */*",
            "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
    });
    const result = await response.json();
    if (result.status !== 200) {
        alert("Failed to raise issue. Please try again.");
        return;
    }
    console.log(result);
    form.reset();
};