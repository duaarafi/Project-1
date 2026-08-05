// Navbar scroll effect
window.onscroll = function ()
{
    var navbar = document.querySelector(".navbar");

    if(window.scrollY > 50)
    {
        navbar.classList.add("scrolled");
    }
    else
    {
        navbar.classList.remove("scrolled");
    }
}


// Show or hide password
function togglePassword(fieldId)
{
    var input = document.getElementById(fieldId);
    var icon = document.getElementById(fieldId + "-icon");

    if(input.type == "password")
    {
        input.type = "text";
        icon.className = "fa-solid fa-eye-slash";
    }
    else
    {
        input.type = "password";
        icon.className = "fa-solid fa-eye";
    }
}


// Register form validation
function validateRegister()
{
    var name = document.getElementById("name").value;
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    var confirmPassword = document.getElementById("confirm-password").value;

    if(name == "")
    {
        alert("Please enter your name.");
        return false;
    }

    if(email == "")
    {
        alert("Please enter your email.");
        return false;
    }

    if(password.length < 8)
    {
        alert("Password must be at least 8 characters.");
        return false;
    }

    if(password != confirmPassword)
    {
        alert("Passwords do not match.");
        return false;
    }

    return true;
}

// Login form validation
function validateLogin()
{
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;

    if(email == "")
    {
        alert("Please enter your email.");
        return false;
    }

    if(password == "")
    {
        alert("Please enter your password.");
        return false;
    }

    return true;
}


// Budget progress bar color
var bars = document.querySelectorAll(".budget-progress-bar");

for(var i = 0; i < bars.length; i++)
{
    var width = parseFloat(bars[i].style.width);

    if(width >= 100)
    {
        bars[i].style.backgroundColor = "#EF4444";
    }
    else if(width >= 80)
    {
        bars[i].style.backgroundColor = "#F59E0B";
    }
    else
    {
        bars[i].style.backgroundColor = "#10B981";
    }
}