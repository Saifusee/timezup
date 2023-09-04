// Getting logout element
const logoutButton = document.getElementById("profile_logout");
const showButton = document.getElementsByClassName("show_button")[0];
const profileContent = document.getElementsByClassName("profile_content")[0];
const profileUsername = document.getElementsByClassName("profile_username")[0];

console.log(showButton)
// setting click event for logging out
logoutButton.addEventListener("click", function(event) {
    event.preventDefault()
    let permission = window.confirm("Do you want to logout?");
    if (permission){
        logoutButton.parentElement.submit();
    } 
})

showButton.addEventListener("click", function(event){
    profileContent.style.display = "inline"
    showButton.style.display = "none"
})

profileUsername.addEventListener("click", function(event){
    showButton.style.display = "inline"
    profileContent.style.display = "none"
})