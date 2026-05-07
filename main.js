// ============================================================
// NAVBAR: Add shadow on scroll
// ============================================================
const navbar = document.getElementById('navbar');

window.addEventListener('scroll', () => {
    if (window.scrollY > 20) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// ============================================================
// MOBILE NAV TOGGLE
// ============================================================
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

// ============================================================
// SMOOTH SCROLL: Override default anchor behaviour
// Accounts for fixed navbar height
// ============================================================
document.querySelectorAll('a[href^="#"]').forEach(link => {
    link.addEventListener('click', function (e) {
        const targetId = this.getAttribute('href').slice(1);
        const target = document.getElementById(targetId);
        if (!target) return;

        e.preventDefault();

        const navHeight = navbar.offsetHeight;
        const targetTop = target.getBoundingClientRect().top + window.scrollY - navHeight - 10;

        window.scrollTo({
            top: targetTop,
            behavior: 'smooth'
        });
    });
});

// ============================================================
// ACTIVE LINK HIGHLIGHTING
// Highlights the correct nav link as you scroll
// ============================================================
const sections = [
    document.getElementById('about'),
    document.getElementById('analysis'),
    document.getElementById('interactive'),
    document.getElementById('findings')
];

const links = document.querySelectorAll('.nav-links a');

function setActiveLink() {
    const navHeight = navbar.offsetHeight + 20;
    const scrollPos = window.scrollY + navHeight;

    let currentSection = sections[0];

    sections.forEach(section => {
        if (!section) return;
        if (section.offsetTop <= scrollPos) {
            currentSection = section;
        }
    });

    links.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === '#' + currentSection.id) {
            link.classList.add('active');
        }
    });
}

window.addEventListener('scroll', setActiveLink);
window.addEventListener('load', setActiveLink);
