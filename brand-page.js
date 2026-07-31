/* AirbagData.nl — Brand Page JavaScript (Accordion, Search & Form Prefill) */
(function () {
  'use strict';

  /* ── Sticky Header Shadow ── */
  const header = document.getElementById('header');
  if (header) {
    window.addEventListener('scroll', () => {
      header.classList.toggle('scrolled', window.scrollY > 15);
    }, { passive: true });
  }

  /* ── Mobile Menu Toggle ── */
  const burgerBtn = document.getElementById('burger-btn');
  const nav = document.querySelector('.nav');

  if (burgerBtn && nav) {
    const closeMenu = () => {
      burgerBtn.setAttribute('aria-expanded', 'false');
      nav.removeAttribute('style');
    };
    burgerBtn.addEventListener('click', () => {
      const isOpen = burgerBtn.getAttribute('aria-expanded') === 'true';
      if (isOpen) {
        closeMenu();
      } else {
        burgerBtn.setAttribute('aria-expanded', 'true');
        Object.assign(nav.style, {
          display: 'flex', flexDirection: 'column',
          position: 'fixed', top: 'calc(var(--topbar-h, 0px) + var(--header-h, 68px))',
          left: '0', width: '100%', background: '#FFFFFF',
          boxShadow: '0 12px 24px rgba(0,0,0,0.12)', padding: '20px 24px',
          zIndex: '800', gap: '8px'
        });
      }
    });
    nav.querySelectorAll('a').forEach(a => a.addEventListener('click', closeMenu));
  }

  /* ── Smooth Scroll ── */
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      const targetId = this.getAttribute('href');
      if (targetId && targetId !== '#') {
        const targetEl = document.querySelector(targetId);
        if (targetEl) {
          e.preventDefault();
          targetEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }
    });
  });

  /* ── Model Accordions ── */
  const modelBtns = document.querySelectorAll('.bp__model-btn');
  modelBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const expanded = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', expanded ? 'false' : 'true');
      const content = btn.parentElement.querySelector('.bp__model-content');
      if (content) {
        content.classList.toggle('open', !expanded);
      }
    });
  });

  /* ── Open first accordion by default if <= 5 models ── */
  if (modelBtns.length > 0 && modelBtns.length <= 5) {
    const firstBtn = modelBtns[0];
    firstBtn.setAttribute('aria-expanded', 'true');
    const c = firstBtn.parentElement.querySelector('.bp__model-content');
    if (c) c.classList.add('open');
  }

  /* ── Inline Search in Brand Page ── */
  const searchInput = document.getElementById('bp-search');
  const searchStatus = document.getElementById('bp-search-status');
  const searchCount = document.getElementById('bp-search-count');
  const modelCards = document.querySelectorAll('.bp__model-card');

  if (searchInput && modelCards.length > 0) {
    searchInput.addEventListener('input', (e) => {
      const q = e.target.value.trim().toUpperCase();
      let matchedRows = 0;

      if (!q) {
        searchStatus.style.display = 'none';
        modelCards.forEach((card, idx) => {
          card.style.display = '';
          const rows = card.querySelectorAll('tbody tr');
          rows.forEach(r => r.style.display = '');
          // restore first accordion default
          const btn = card.querySelector('.bp__model-btn');
          const content = card.querySelector('.bp__model-content');
          if (idx === 0 && modelCards.length <= 5) {
            if (btn) btn.setAttribute('aria-expanded', 'true');
            if (content) content.classList.add('open');
          } else {
            if (btn) btn.setAttribute('aria-expanded', 'false');
            if (content) content.classList.remove('open');
          }
        });
        return;
      }

      modelCards.forEach(card => {
        const modelName = (card.querySelector('.bp__model-name')?.textContent || '').toUpperCase();
        const rows = card.querySelectorAll('tbody tr');
        let cardHasMatch = false;

        rows.forEach(row => {
          const text = (row.textContent || '').toUpperCase();
          if (text.includes(q) || modelName.includes(q)) {
            row.style.display = '';
            cardHasMatch = true;
            matchedRows++;
          } else {
            row.style.display = 'none';
          }
        });

        if (cardHasMatch) {
          card.style.display = '';
          const btn = card.querySelector('.bp__model-btn');
          const content = card.querySelector('.bp__model-content');
          if (btn) btn.setAttribute('aria-expanded', 'true');
          if (content) content.classList.add('open');
        } else {
          card.style.display = 'none';
        }
      });

      searchStatus.style.display = 'flex';
      if (matchedRows === 0) {
        searchCount.textContent = `Geen modules gevonden voor "${q}" in dit merk.`;
      } else {
        searchCount.textContent = `${matchedRows} module${matchedRows !== 1 ? 's' : ''} gevonden in deze lijst.`;
      }
    });
  }

  /* ── Prefill Part Number and Delivery Option when clicking "Aanmelden" on a table row ── */
  document.querySelectorAll('.bp__table a[href="#contact"]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      const row = btn.closest('tr');
      if (row) {
        const pn = row.querySelector('.bp__pn')?.textContent?.trim();
        const partnrInput = document.getElementById('partnr');
        if (pn && partnrInput) {
          partnrInput.value = pn;
          // highlight input briefly
          partnrInput.style.transition = 'background 0.3s ease';
          partnrInput.style.background = '#FEFCE8';
          setTimeout(() => partnrInput.style.background = '', 2000);
        }
      }
      const methodsStr = btn.dataset.methods || '';
      const deliveryInput = document.getElementById('delivery');
      if (deliveryInput && methodsStr) {
        const firstMethod = methodsStr.split(',')[0];
        if (firstMethod === 'OBD' || firstMethod === 'Dump' || firstMethod === 'Bench') {
          deliveryInput.value = firstMethod;
          deliveryInput.style.transition = 'background 0.3s ease';
          deliveryInput.style.background = '#FEFCE8';
          setTimeout(() => deliveryInput.style.background = '', 2000);
        }
      }
    });
  });

  /* ── Contact Form Submission ── */
  const form = document.getElementById('contact-form');
  const successEl = document.getElementById('form-success');

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const submitBtn = form.querySelector('[type="submit"]');
      const btnText = submitBtn.querySelector('.btn__text');
      const originalText = btnText ? btnText.textContent : 'Versturen';

      const required = form.querySelectorAll('[required]');
      let isValid = true;
      required.forEach(input => {
        input.style.borderColor = input.value.trim() ? '' : '#EF4444';
        if (!input.value.trim()) isValid = false;
      });

      if (!isValid) {
        if (successEl) { successEl.textContent = 'Vul alstublieft alle verplichte velden in.'; successEl.style.color = '#EF4444'; }
        return;
      }

      submitBtn.disabled = true;
      if (btnText) btnText.textContent = 'Bezig met verzenden...';

      try {
        await new Promise(r => setTimeout(r, 1200));
        form.reset();
        if (successEl) { successEl.textContent = '✓ Aanvraag ontvangen! We reageren binnen 2 uur.'; successEl.style.color = '#10B981'; }
      } catch {
        if (successEl) { successEl.textContent = 'Er ging iets mis. Bel ons op 06-52619000.'; successEl.style.color = '#EF4444'; }
      } finally {
        submitBtn.disabled = false;
        if (btnText) btnText.textContent = originalText;
      }
    });
  }

})();
