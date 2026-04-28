// Navbar scroll effect
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
    if (window.scrollY > 20) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Mobile nav toggle
const navToggle = document.getElementById('navToggle');
const navLinks = document.getElementById('navLinks');

navToggle.addEventListener('click', () => {
    navLinks.classList.toggle('open');
});

// Close mobile nav when a link is clicked
navLinks.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => {
        navLinks.classList.remove('open');
    });
});

// Highlight active nav link on scroll
const sections = document.querySelectorAll('section[id], header[id]');
const links = document.querySelectorAll('.nav-links a');

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            links.forEach(link => {
                link.style.color = '';
                link.style.borderBottomColor = '';
                if (link.getAttribute('href') === '#' + entry.target.id) {
                    link.style.color = 'var(--accent)';
                    link.style.borderBottomColor = 'var(--accent)';
                }
            });
        }
    });
}, { threshold: 0.3 });

sections.forEach(section => observer.observe(section));
