document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('switchToSignUp').addEventListener('click', function(event) {
        event.preventDefault();
        document.getElementById('loginForm').style.display = 'none';
        document.getElementById('signUpForm').style.display = 'block';
    });

    document.getElementById('switchToLogin').addEventListener('click', function(event) {
        event.preventDefault();
        document.getElementById('signUpForm').style.display = 'none';
        document.getElementById('loginForm').style.display = 'block';
    });
});
