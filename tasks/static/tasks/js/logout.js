// Getting logout element
const logoutButton = document.getElementById("profile_logout");

// setting click event for logging out
logoutButton.addEventListener("click", function(event) {
    event.preventDefault()
    let permission = window.confirm("Do you want to logout?");
    if (permission){
        logoutButton.parentElement.submit();
    } 
})