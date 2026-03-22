/* ============================================================
   KEERTHIVASAN PORTFOLIO — script.js
   ============================================================ */

'use strict';

// ── PAGE LOADER ─────────────────────────────────────────────
window.addEventListener('load', () => {
  const loader = document.getElementById('page-loader');
  setTimeout(() => {
    loader.classList.add('hide');
    document.body.style.overflow = '';
    initReveal();
  }, 1800);
});

document.body.style.overflow = 'hidden'; // prevent scroll during load

// ── SCROLL PROGRESS BAR ─────────────────────────────────────
const progressBar = document.getElementById('scroll-progress');
window.addEventListener('scroll', () => {
  const scrolled = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100;
  progressBar.style.width = Math.min(scrolled, 100) + '%';
}, { passive: true });

// ── NAVBAR ───────────────────────────────────────────────────
const navbar = document.getElementById('navbar');
const hamburger = document.getElementById('hamburger');
const navLinks = document.getElementById('nav-links');
const navLinkItems = document.querySelectorAll('.nav-link');

window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 50);
  highlightNav();
}, { passive: true });

// Hamburger toggle
hamburger.addEventListener('click', () => {
  const isOpen = navLinks.classList.toggle('open');
  hamburger.classList.toggle('open', isOpen);
  hamburger.setAttribute('aria-expanded', isOpen);
});

// Close nav on link click
navLinkItems.forEach(link => {
  link.addEventListener('click', () => {
    navLinks.classList.remove('open');
    hamburger.classList.remove('open');
    hamburger.setAttribute('aria-expanded', false);
  });
});

// Active nav highlight
function highlightNav() {
  const sections = document.querySelectorAll('section[id]');
  let currentSection = '';
  sections.forEach(sec => {
    if (window.scrollY >= sec.offsetTop - 120) {
      currentSection = sec.id;
    }
  });
  navLinkItems.forEach(link => {
    link.classList.toggle('active', link.getAttribute('href') === '#' + currentSection);
  });
}

// ── THEME TOGGLE ─────────────────────────────────────────────
const themeToggle = document.getElementById('theme-toggle');
const themeIcon = document.getElementById('theme-icon');

const savedTheme = localStorage.getItem('theme');
if (savedTheme === 'light') {
  document.body.classList.add('light-theme');
  themeIcon.className = 'fas fa-moon';
}

themeToggle.addEventListener('click', () => {
  document.body.classList.toggle('light-theme');
  const isLight = document.body.classList.contains('light-theme');
  themeIcon.className = isLight ? 'fas fa-moon' : 'fas fa-sun';
  localStorage.setItem('theme', isLight ? 'light' : 'dark');
});

// ── TYPING ANIMATION ─────────────────────────────────────────
const typedEl = document.getElementById('typed-text');
const phrases = [
  'I build web apps with Python & Flask',
  'I craft clean, responsive UIs',
  'I love solving real-world problems',
  'I\'m learning AI & Machine Learning',
  'I turn ideas into working products',
];
let phraseIndex = 0;
let charIndex = 0;
let isDeleting = false;
let typingPaused = false;

function typeLoop() {
  if (!typedEl) return;
  const current = phrases[phraseIndex];

  if (!isDeleting) {
    typedEl.textContent = current.slice(0, charIndex + 1);
    charIndex++;
    if (charIndex === current.length) {
      isDeleting = true;
      setTimeout(typeLoop, 1800);
      return;
    }
    setTimeout(typeLoop, 65);
  } else {
    typedEl.textContent = current.slice(0, charIndex - 1);
    charIndex--;
    if (charIndex === 0) {
      isDeleting = false;
      phraseIndex = (phraseIndex + 1) % phrases.length;
      setTimeout(typeLoop, 400);
      return;
    }
    setTimeout(typeLoop, 35);
  }
}

// Start typing after loader
setTimeout(typeLoop, 2000);

// ── SCROLL REVEAL ────────────────────────────────────────────
function initReveal() {
  const revealEls = document.querySelectorAll('[data-reveal]');

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const delay = el.dataset.delay ? parseInt(el.dataset.delay) : 0;
        setTimeout(() => {
          el.classList.add('revealed');
          // Trigger skill bars if inside skills section
          if (el.closest('#skills') || el.classList.contains('skills-grid')) {
            animateSkillBars();
          }
        }, delay);
        observer.unobserve(el);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -60px 0px' });

  revealEls.forEach(el => observer.observe(el));
}

// ── SKILL BAR ANIMATION ──────────────────────────────────────
let skillsAnimated = false;

function animateSkillBars() {
  if (skillsAnimated) return;
  skillsAnimated = true;

  const fills = document.querySelectorAll('.skill-bar-fill');
  fills.forEach((fill, i) => {
    const width = fill.dataset.width;
    setTimeout(() => {
      fill.style.width = width + '%';
      fill.classList.add('animated');
    }, i * 100);
  });
}

// Trigger skills when section enters view
const skillsSection = document.getElementById('skills');
if (skillsSection) {
  const skillsObserver = new IntersectionObserver((entries) => {
    if (entries[0].isIntersecting) {
      animateSkillBars();
      skillsObserver.disconnect();
    }
  }, { threshold: 0.2 });
  skillsObserver.observe(skillsSection);
}

// ── CONTACT FORM ─────────────────────────────────────────────
const contactForm = document.getElementById('contact-form');
const submitBtn = document.getElementById('submit-btn');
const btnText = document.getElementById('btn-text');
const btnLoading = document.getElementById('btn-loading');
const formFeedback = document.getElementById('form-feedback');

if (contactForm) {
  contactForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    // UI: loading state
    submitBtn.disabled = true;
    btnText.style.display = 'none';
    btnLoading.style.display = 'inline-flex';
    formFeedback.className = 'form-feedback';

    const formData = new FormData(contactForm);

    try {
      const response = await fetch('/contact', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();

      formFeedback.textContent = data.message;
      formFeedback.classList.add(data.success ? 'success' : 'error');

      if (data.success) {
        contactForm.reset();
      }
    } catch (err) {
      formFeedback.textContent = 'Something went wrong. Please try again.';
      formFeedback.classList.add('error');
    } finally {
      submitBtn.disabled = false;
      btnText.style.display = 'inline-flex';
      btnLoading.style.display = 'none';
    }
  });
}

// ── FOOTER YEAR ──────────────────────────────────────────────
const yearEl = document.getElementById('year');
if (yearEl) yearEl.textContent = new Date().getFullYear();

// ── SMOOTH SCROLL for anchor links ───────────────────────────
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function(e) {
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

// ── TOOL CARD HOVER STAGGER ──────────────────────────────────
const toolCards = document.querySelectorAll('.tool-card');
toolCards.forEach((card, i) => {
  card.style.transitionDelay = `${i * 0.04}s`;
});

// ── CURSOR GLOW EFFECT (subtle) ──────────────────────────────
const cursorGlow = document.createElement('div');
cursorGlow.style.cssText = `
  pointer-events:none;
  position:fixed;
  width:300px;height:300px;
  border-radius:50%;
  background:radial-gradient(circle,rgba(0,212,255,0.04),transparent 70%);
  transform:translate(-50%,-50%);
  z-index:0;
  transition:left 0.15s,top 0.15s;
  top:-300px;left:-300px;
`;
document.body.appendChild(cursorGlow);
window.addEventListener('mousemove', (e) => {
  cursorGlow.style.left = e.clientX + 'px';
  cursorGlow.style.top = e.clientY + 'px';
}, { passive: true });
