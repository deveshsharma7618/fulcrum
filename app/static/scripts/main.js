const authBTn = document.getElementsByClassName("auth-btn")

const checkAuthorized = function(){
    const access_token = localStorage.getItem("access_token");
    if(access_token){
        Array.from(authBTn).forEach((element)=>{
            console.log(element);
            element.style.display = "none";
        })

        return true;
    }
    return false;
}

checkAuthorized()