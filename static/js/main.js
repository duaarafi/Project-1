// Navbar scroll effect
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Password toggle
function togglePassword(fieldId) {
    const input = document.getElementById(fieldId);
    const icon = document.getElementById(fieldId + '-icon');
    if (input.type === 'password') {
        input.type = 'text';
        icon.classList.replace('fa-eye', 'fa-eye-slash');
    } else {
        input.type = 'password';
        icon.classList.replace('fa-eye-slash', 'fa-eye');
    }
}

// Budget progress bar color
document.querySelectorAll('.budget-progress-bar').forEach(bar => {
    const width = parseFloat(bar.style.width);
    if (width >= 100) {
        bar.style.backgroundColor = '#EF4444';
    } else if (width >= 80) {
        bar.style.backgroundColor = '#F59E0B';
    } else {
        bar.style.backgroundColor = '#10B981';
    }
});