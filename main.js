/* AirbagCrashReset.nl — Main JavaScript (CarLabImmo Style) */

(function () {
  'use strict';

  /* ── Sticky Header Shadow ── */
  const header = document.getElementById('header');
  if (header) {
    const onScroll = () => {
      header.classList.toggle('scrolled', window.scrollY > 15);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  /* ── Mobile Menu Toggle ── */
  const burgerBtn = document.getElementById('burger-btn');
  const nav = document.querySelector('.nav');

  if (burgerBtn && nav) {
    burgerBtn.addEventListener('click', () => {
      const expanded = burgerBtn.getAttribute('aria-expanded') === 'true';
      burgerBtn.setAttribute('aria-expanded', String(!expanded));
      nav.style.display = expanded ? 'none' : 'flex';
      nav.style.position = 'absolute';
      nav.style.top = '100%';
      nav.style.left = '0';
      nav.style.width = '100%';
      nav.style.background = '#FFFFFF';
      nav.style.boxShadow = '0 12px 24px rgba(0,0,0,0.12)';
      nav.style.padding = '20px';
    });
  }

  /* ── Interactive Brand Filter (CarLabImmo Finder) ── */
  const brandInput = document.getElementById('brand-filter-input');
  const brandCards = document.querySelectorAll('.brand-card');

  if (brandInput && brandCards.length > 0) {
    brandInput.addEventListener('input', (e) => {
      const query = e.target.value.toLowerCase().trim();
      brandCards.forEach(card => {
        const text = card.textContent.toLowerCase();
        if (text.includes(query)) {
          card.style.display = 'flex';
        } else {
          card.style.display = 'none';
        }
      });
    });
  }

  /* ── Smooth Scroll for Navigation Links ── */
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      if (targetId && targetId !== '#') {
        const targetEl = document.querySelector(targetId);
        if (targetEl) {
          e.preventDefault();
          targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
          if (window.innerWidth <= 768 && nav && nav.style.position === 'absolute') {
            nav.style.display = 'none';
            burgerBtn.setAttribute('aria-expanded', 'false');
          }
        }
      }
    });
  });

  /* ── FAQ Accordion Toggle ── */
  document.querySelectorAll('.faq-card__btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const expanded = btn.getAttribute('aria-expanded') === 'true';
      // Close all
      document.querySelectorAll('.faq-card__btn').forEach(b => {
        b.setAttribute('aria-expanded', 'false');
        const content = b.parentElement.querySelector('.faq-card__content');
        if (content) content.classList.remove('open');
      });
      // Toggle current
      if (!expanded) {
        btn.setAttribute('aria-expanded', 'true');
        const content = btn.parentElement.querySelector('.faq-card__content');
        if (content) content.classList.add('open');
      }
    });
  });

  /* ── Counter Animation ── */
  function animateCounter(el, target, duration) {
    let start = null;
    const step = (timestamp) => {
      if (!start) start = timestamp;
      const progress = Math.min((timestamp - start) / duration, 1);
      const ease = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.round(ease * target);
      if (progress < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  }

  const statNumbers = document.querySelectorAll('.stat-card__num[data-target]');
  let animated = false;

  const statsSection = document.querySelector('.stats');
  if (statsSection && statNumbers.length > 0) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting && !animated) {
          animated = true;
          statNumbers.forEach(el => {
            const target = parseInt(el.dataset.target, 10);
            animateCounter(el, target, 1600);
          });
          observer.disconnect();
        }
      });
    }, { threshold: 0.2 });
    observer.observe(statsSection);
  }

  /* ── Contact Form Submission Handler ── */
  const form = document.getElementById('contact-form');
  const successEl = document.getElementById('form-success');

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const submitBtn = form.querySelector('[type="submit"]');
      const btnText = submitBtn.querySelector('.btn__text');
      const originalText = btnText ? btnText.textContent : 'Versturen';

      // Simple validation check
      const requiredInputs = form.querySelectorAll('[required]');
      let isValid = true;
      requiredInputs.forEach(input => {
        if (!input.value.trim()) {
          input.style.borderColor = '#EF4444';
          isValid = false;
        } else {
          input.style.borderColor = '';
        }
      });

      if (!isValid) {
        if (successEl) {
          successEl.textContent = 'Vul alstublieft alle verplichte velden in.';
          successEl.style.color = '#EF4444';
        }
        return;
      }

      // Simulate sending
      submitBtn.disabled = true;
      if (btnText) btnText.textContent = 'Bezig met verzenden...';

      try {
        await new Promise(r => setTimeout(r, 1200));
        form.reset();
        if (successEl) {
          successEl.textContent = '✓ Uw aanvraag is ontvangen! We reageren binnen 2 uur.';
          successEl.style.color = '#10B981';
        }
      } catch (err) {
        if (successEl) {
          successEl.textContent = 'Er ging iets mis. Bel ons direct op 06-52619000.';
          successEl.style.color = '#EF4444';
        }
      } finally {
        submitBtn.disabled = false;
        if (btnText) btnText.textContent = originalText;
      }
    });
  }

})();
