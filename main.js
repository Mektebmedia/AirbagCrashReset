/* AirbagData.nl — Main JavaScript (with 16,878-entry Module Database) */
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

  /* ── Brand filter in Merken section ── */
  const brandFilterInput = document.getElementById('brand-filter-input');
  const brandCards = document.querySelectorAll('.brand-card');
  if (brandFilterInput && brandCards.length > 0) {
    brandFilterInput.addEventListener('input', (e) => {
      const q = e.target.value.toLowerCase();
      brandCards.forEach(c => {
        c.style.display = c.textContent.toLowerCase().includes(q) ? '' : 'none';
      });
    });
  }

  /* ── FAQ Accordion ── */
  document.querySelectorAll('.faq-card__btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const expanded = btn.getAttribute('aria-expanded') === 'true';
      document.querySelectorAll('.faq-card__btn').forEach(b => {
        b.setAttribute('aria-expanded', 'false');
        const c = b.parentElement.querySelector('.faq-card__content');
        if (c) c.classList.remove('open');
      });
      if (!expanded) {
        btn.setAttribute('aria-expanded', 'true');
        const c = btn.parentElement.querySelector('.faq-card__content');
        if (c) c.classList.add('open');
      }
    });
  });

  /* ── Counter Animation ── */
  function animateCounter(el, target, duration) {
    let start = null;
    const step = (ts) => {
      if (!start) start = ts;
      const p = Math.min((ts - start) / duration, 1);
      el.textContent = Math.round((1 - Math.pow(1 - p, 3)) * target).toLocaleString('nl-NL');
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  }

  let statsAnimated = false;
  const statsSection = document.querySelector('.stats');
  if (statsSection) {
    new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting && !statsAnimated) {
          statsAnimated = true;
          document.querySelectorAll('.stat-card__num[data-target]').forEach(el => {
            animateCounter(el, parseInt(el.dataset.target, 10), 1800);
          });
        }
      });
    }, { threshold: 0.2 }).observe(statsSection);
  }

  /* ── MODULE DATABASE SEARCH (16,878 entries from MODULE_DB global) ── */
  const mdbSearch   = document.getElementById('mdb-search');
  const mdbBrand    = document.getElementById('mdb-brand');
  const mdbClear    = document.getElementById('mdb-clear');
  const mdbCount    = document.getElementById('mdb-count');
  const mdbEmpty    = document.getElementById('mdb-empty');
  const mdbTable    = document.getElementById('mdb-table');
  const mdbTbody    = document.getElementById('mdb-tbody');
  const mdbPagination = document.getElementById('mdb-pagination');
  const mdbCta      = document.getElementById('mdb-cta');

  if (!mdbSearch || typeof MODULE_DB === 'undefined') return;

  const PAGE_SIZE = 20;
  let currentPage = 1;
  let filteredResults = [];

  function highlight(text, query) {
    if (!query || query.length < 2) return text;
    const escaped = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    return text.replace(new RegExp(`(${escaped})`, 'gi'), '<mark>$1</mark>');
  }

  function brandLabel(slug) {
    const map = {
      'alfa-romeo': 'Alfa Romeo', 'audi': 'Audi', 'bmw': 'BMW', 'byd': 'BYD',
      'chevrolet': 'Chevrolet', 'citroen': 'Citroën', 'dacia': 'Dacia', 'fiat': 'Fiat',
      'ford': 'Ford', 'honda': 'Honda', 'hyundai': 'Hyundai', 'jaguar': 'Jaguar',
      'jeep': 'Jeep', 'kia': 'Kia', 'land-rover': 'Land Rover', 'mazda': 'Mazda',
      'mercedes': 'Mercedes-Benz', 'mini': 'Mini', 'mitsubishi': 'Mitsubishi',
      'nissan': 'Nissan', 'opel': 'Opel', 'peugeot': 'Peugeot', 'renault': 'Renault',
      'seat': 'Seat', 'skoda': 'Škoda', 'suzuki': 'Suzuki', 'tesla': 'Tesla',
      'toyota': 'Toyota', 'volkswagen': 'Volkswagen', 'volvo': 'Volvo'
    };
    return map[slug] || slug.charAt(0).toUpperCase() + slug.slice(1);
  }

  function renderResults() {
    const start = (currentPage - 1) * PAGE_SIZE;
    const page = filteredResults.slice(start, start + PAGE_SIZE);
    const query = mdbSearch.value.trim();
    const total = filteredResults.length;

    // Count label
    if (total === 0) {
      mdbCount.textContent = 'Geen modules gevonden — probeer een ander nummer.';
    } else {
      mdbCount.textContent = `${total.toLocaleString('nl-NL')} module${total !== 1 ? 's' : ''} gevonden`;
    }

    // Show/hide states
    mdbEmpty.style.display   = total === 0 ? 'block' : 'none';
    mdbTable.style.display   = total > 0  ? 'table' : 'none';
    mdbCta.style.display     = total > 0  ? 'block' : 'none';

    if (total === 0) {
      mdbEmpty.innerHTML = `
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <h3>Geen module gevonden voor "<em>${query}</em>"</h3>
        <p>Neem contact met ons op via WhatsApp of het formulier hieronder. Wij controleren de module handmatig voor u.</p>
      `;
      mdbPagination.innerHTML = '';
      return;
    }

    function renderMethodHtml(methods) {
      if (!methods || !methods.length) {
        methods = ['Dump'];
      }
      return '<div class="opt-wrap">' + methods.map(m => {
        if (m === 'OBD') {
          return '<div class="opt-row"><span class="opt-pill opt-pill--obd">OBD</span><span class="opt-text">Met auto of losse module langskomen</span></div>';
        } else if (m === 'Dump') {
          return '<div class="opt-row"><span class="opt-pill opt-pill--dump">Dump</span><span class="opt-text">Data of losse module aanleveren</span></div>';
        } else if (m === 'Bench') {
          return '<div class="opt-row"><span class="opt-pill opt-pill--bench">Bench</span><span class="opt-text">Losse module aanleveren</span></div>';
        }
        return '';
      }).join('') + '</div>';
    }

    // Table rows
    mdbTbody.innerHTML = page.map(m => `
      <tr>
        <td><span class="mdb__brand-pill">${brandLabel(m.brand)}</span></td>
        <td>${highlight(m.model || '—', query)}</td>
        <td class="mdb__part-num">${highlight(m.part_number || m.raw, query)}</td>
        <td class="mdb__supplier">${highlight(m.supplier_number || '', query)}</td>
        <td class="mdb__opt">${renderMethodHtml(m.methods)}</td>
        <td>
          <a href="#contact" class="btn btn--blue" data-brand="${m.brand || ''}" data-model="${m.model || ''}" data-part="${m.part_number || m.raw || ''}" data-supplier="${m.supplier_number || ''}" data-methods="${(m.methods || []).join(',')}" style="padding:8px 16px; font-size:0.8rem;">
            Aanmelden
          </a>
        </td>
      </tr>
    `).join('');

    // Attach form prefill to Aanmelden buttons
    mdbTbody.querySelectorAll('a[href="#contact"]').forEach(btn => {
      btn.addEventListener('click', () => {
        const brand = btn.dataset.brand || '';
        const model = btn.dataset.model || '';
        const part = btn.dataset.part || '';
        const supplier = btn.dataset.supplier || '';
        const methodsStr = btn.dataset.methods || '';
        const brandInput = document.getElementById('brand');
        const partnrInput = document.getElementById('partnr');
        const deliveryInput = document.getElementById('delivery');
        if (brandInput) {
          brandInput.value = `${brandLabel(brand)} ${model}`.trim();
          brandInput.style.transition = 'background 0.3s ease';
          brandInput.style.background = '#FEFCE8';
          setTimeout(() => brandInput.style.background = '', 2000);
        }
        if (partnrInput) {
          partnrInput.value = `${part} ${supplier ? '- ' + supplier : ''}`.trim();
          partnrInput.style.transition = 'background 0.3s ease';
          partnrInput.style.background = '#FEFCE8';
          setTimeout(() => partnrInput.style.background = '', 2000);
        }
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

    // Pagination
    const totalPages = Math.ceil(total / PAGE_SIZE);
    if (totalPages <= 1) {
      mdbPagination.innerHTML = '';
      return;
    }

    let pages = '';
    // Prev
    pages += `<button ${currentPage === 1 ? 'disabled' : ''} data-page="${currentPage - 1}">‹ Vorige</button>`;

    const range = [];
    for (let i = 1; i <= totalPages; i++) {
      if (i === 1 || i === totalPages || (i >= currentPage - 2 && i <= currentPage + 2)) {
        range.push(i);
      }
    }
    let prev = null;
    for (const p of range) {
      if (prev && p - prev > 1) pages += `<button disabled>…</button>`;
      pages += `<button class="${p === currentPage ? 'active' : ''}" data-page="${p}">${p}</button>`;
      prev = p;
    }

    // Next
    pages += `<button ${currentPage === totalPages ? 'disabled' : ''} data-page="${currentPage + 1}">Volgende ›</button>`;
    mdbPagination.innerHTML = pages;

    mdbPagination.querySelectorAll('button[data-page]').forEach(btn => {
      btn.addEventListener('click', () => {
        currentPage = parseInt(btn.dataset.page, 10);
        renderResults();
        document.getElementById('module-checker').scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    });
  }

  function runSearch() {
    const raw = mdbSearch.value.trim();
    const brand = mdbBrand.value;
    const q = raw.replace(/\s+/g, ' ').toUpperCase();

    mdbClear.style.display = raw.length > 0 ? 'flex' : 'none';

    if (raw.length < 3 && !brand) {
      mdbCount.textContent = 'Typ om te zoeken in 14.264 modules...';
      mdbEmpty.style.display = 'block';
      mdbTable.style.display = 'none';
      mdbCta.style.display = 'none';
      mdbPagination.innerHTML = '';
      mdbEmpty.innerHTML = `
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <h3>Zoek uw module nummer</h3>
        <p>Typ een OEM-onderdeelnummer (bijv. <strong>2Q0 959 655</strong>) of een leveranciersnummer (bijv. <strong>BOSCH 0 285 014 912</strong>) in het zoekvak om te controleren of uw module door ons gereset kan worden.</p>
      `;
      filteredResults = [];
      return;
    }

    filteredResults = MODULE_DB.filter(m => {
      const matchesBrand = !brand || m.brand === brand;
      if (!matchesBrand) return false;
      if (!q || q.length < 3) return true;
      const raw_upper = (m.raw || '').toUpperCase();
      const pn_upper  = (m.part_number || '').toUpperCase();
      const sn_upper  = (m.supplier_number || '').toUpperCase();
      const md_upper  = (m.model || '').toUpperCase();
      return raw_upper.includes(q) || pn_upper.includes(q) || sn_upper.includes(q) || md_upper.includes(q);
    });

    currentPage = 1;
    renderResults();
  }

  let debounceTimer;
  mdbSearch.addEventListener('input', () => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(runSearch, 180);
  });

  mdbBrand.addEventListener('change', runSearch);

  mdbClear.addEventListener('click', () => {
    mdbSearch.value = '';
    mdbBrand.value = '';
    mdbSearch.focus();
    runSearch();
  });

  // Quick Brand Chips
  document.querySelectorAll('.mdb__quick-chip[data-brand]').forEach(chip => {
    chip.addEventListener('click', () => {
      document.querySelectorAll('.mdb__quick-chip').forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      const b = chip.dataset.brand || '';
      if (mdbBrand) mdbBrand.value = b;
      runSearch();
    });
  });

  // Header Database Search Input
  const headerSearchInput = document.getElementById('header-search-input');
  const headerSearchBtn = document.getElementById('header-search-btn');
  const triggerHeaderSearch = () => {
    if (!headerSearchInput) return;
    const q = headerSearchInput.value.trim();
    if (mdbSearch) {
      mdbSearch.value = q;
      runSearch();
      const target = document.getElementById('module-checker');
      if (target) {
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    }
  };
  if (headerSearchInput) {
    headerSearchInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        triggerHeaderSearch();
      }
    });
  }
  if (headerSearchBtn) {
    headerSearchBtn.addEventListener('click', triggerHeaderSearch);
  }

  /* ── Contact Form ── */
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
