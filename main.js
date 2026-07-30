/* AirbagCrashReset.nl — Main JavaScript */

(function () {
  'use strict';

  /* ── Sticky Header shadow ── */
  const header = document.getElementById('header');
  if (header) {
    const onScroll = () => {
      header.classList.toggle('scrolled', window.scrollY > 20);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ── Mobile Menu ── */
  const burgerBtn    = document.getElementById('burger-btn');
  const mobileMenu   = document.getElementById('mobile-menu');
  const mobileOverlay = document.getElementById('mobile-overlay');
  const mobileClose  = document.getElementById('mobile-close-btn');

  function openMenu() {
    mobileMenu.classList.add('open');
    mobileOverlay.classList.add('active');
    burgerBtn.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
  }

  function closeMenu() {
    mobileMenu.classList.remove('open');
    mobileOverlay.classList.remove('active');
    burgerBtn.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  }

  if (burgerBtn) burgerBtn.addEventListener('click', openMenu);
  if (mobileClose) mobileClose.addEventListener('click', closeMenu);
  if (mobileOverlay) mobileOverlay.addEventListener('click', closeMenu);

  // Close on mobile nav link click
  if (mobileMenu) {
    mobileMenu.querySelectorAll('.mobile-nav a').forEach(link => {
      link.addEventListener('click', closeMenu);
    });
  }

  /* ── Smooth scroll for anchor links ── */
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  /* ── FAQ Accordion ── */
  document.querySelectorAll('.faq-item__q').forEach(btn => {
    btn.addEventListener('click', () => {
      const expanded = btn.getAttribute('aria-expanded') === 'true';
      // Close all
      document.querySelectorAll('.faq-item__q').forEach(b => {
        b.setAttribute('aria-expanded', 'false');
        const a = b.parentElement.querySelector('.faq-item__a');
        if (a) a.classList.remove('open');
      });
      // Toggle current
      if (!expanded) {
        btn.setAttribute('aria-expanded', 'true');
        const answer = btn.parentElement.querySelector('.faq-item__a');
        if (answer) answer.classList.add('open');
      }
    });
  });

  /* ── Counter animation ── */
  function animateCounter(el, target, duration) {
    let startTime = null;
    const step = (timestamp) => {
      if (!startTime) startTime = timestamp;
      const progress = Math.min((timestamp - startTime) / duration, 1);
      const ease = 1 - Math.pow(1 - progress, 3); // ease-out cubic
      el.textContent = Math.round(ease * target);
      if (progress < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  }

  const statNumbers = document.querySelectorAll('.stat__number[data-target]');
  let statsAnimated = false;

  const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !statsAnimated) {
        statsAnimated = true;
        statNumbers.forEach(el => {
          const target = parseInt(el.dataset.target, 10);
          animateCounter(el, target, 1800);
        });
        statsObserver.disconnect();
      }
    });
  }, { threshold: 0.3 });

  const statsBar = document.querySelector('.stats-bar');
  if (statsBar) statsObserver.observe(statsBar);

  /* ── Reveal on scroll ── */
  const revealEls = document.querySelectorAll(
    '.step-card, .why__card, .brand-chip, .pricing-card, .faq-item, .stat'
  );

  revealEls.forEach((el, i) => {
    el.classList.add('reveal');
    const mod = i % 4;
    if (mod === 1) el.classList.add('reveal--delay-1');
    else if (mod === 2) el.classList.add('reveal--delay-2');
    else if (mod === 3) el.classList.add('reveal--delay-3');
  });

  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        revealObserver.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

  revealEls.forEach(el => revealObserver.observe(el));

  /* ── Contact Form ── */
  const form = document.getElementById('contact-form');
  const successEl = document.getElementById('form-success');

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();

      const btn = form.querySelector('[type="submit"]');
      const btnText = btn.querySelector('.btn__text');
      const originalText = btnText.textContent;

      // Validate
      const required = form.querySelectorAll('[required]');
      let valid = true;
      required.forEach(input => {
        if (!input.value.trim()) {
          input.style.borderColor = '#ef4444';
          valid = false;
        } else {
          input.style.borderColor = '';
        }
      });

      if (!valid) {
        if (successEl) {
          successEl.textContent = 'Vul alle verplichte velden in.';
          successEl.style.color = '#ef4444';
        }
        return;
      }

      // Loading state
      btn.disabled = true;
      btnText.textContent = 'Verzenden...';

      try {
        // Simulate send — replace with actual endpoint
        await new Promise(resolve => setTimeout(resolve, 1500));

        form.reset();
        if (successEl) {
          successEl.textContent = '✓ Uw aanvraag is ontvangen! Wij reageren binnen 2 uur.';
          successEl.style.color = '';
        }
      } catch {
        if (successEl) {
          successEl.textContent = 'Er ging iets mis. Bel ons op 06-52619000.';
          successEl.style.color = '#ef4444';
        }
      } finally {
        btn.disabled = false;
        btnText.textContent = originalText;
      }
    });
  }

  /* ── Active nav highlight ── */
  const sections = document.querySelectorAll('section[id]');
  const navLinks = document.querySelectorAll('.nav a[href^="#"]');

  const navObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        navLinks.forEach(link => {
          link.style.color = '';
          link.style.background = '';
        });
        const active = document.querySelector(`.nav a[href="#${entry.target.id}"]`);
        if (active) {
          active.style.color = 'var(--clr-primary)';
        }
      }
    });
  }, { threshold: 0.4 });

  sections.forEach(s => navObserver.observe(s));

})();
