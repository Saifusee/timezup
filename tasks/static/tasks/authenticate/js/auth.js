
document.addEventListener('DOMContentLoaded', function () {
    const eyeToggle = document.querySelector('.eye-toggle');
    const passwordInput = document.querySelector('#id_password');
    const openEye = document.querySelector('#open_eye');
    const closeEye = document.querySelector('#close_eye');
    closeEye.style.display = "none"

    eyeToggle.addEventListener('click', function () {
        if (passwordInput.type === 'password') {
            passwordInput.type = 'text';
            openEye.style.display = "none"
            closeEye.style.display = "inline"
        } else {
            passwordInput.type = 'password';
            openEye.style.display = "inline"
            closeEye.style.display = "none"
        }
    });
});