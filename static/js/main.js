/* =============================================================================
   ThaiCook — main.js
   Handles: ingredient chip toggle, category tabs, search filter, form submit
   ============================================================================= */

document.addEventListener('DOMContentLoaded', () => {

  // ── State ────────────────────────────────────────────────────────────────────
  const selectedIds = new Set(window.SAVED_IDS || []);

  // ── DOM refs ─────────────────────────────────────────────────────────────────
  const chips         = document.querySelectorAll('.ingredient-chip');
  const countEl       = document.getElementById('selectedCount');
  const tagsEl        = document.getElementById('selectedTags');
  const searchBtn     = document.getElementById('searchBtn');
  const clearBtn      = document.getElementById('clearAllBtn');
  const idsInput      = document.getElementById('ingredientIdsInput');
  const form          = document.getElementById('recommendForm');
  const ingSearch     = document.getElementById('ingredientSearch');
  const catTabs       = document.querySelectorAll('.cat-tab');
  const grid          = document.getElementById('ingredientGrid');

  if (!chips.length) return;   // guard — not on home page

  // ── Helpers ──────────────────────────────────────────────────────────────────
  function updateUI() {
    // Update count badge
    if (countEl) countEl.textContent = selectedIds.size;

    // Update hidden input (comma-separated IDs → Django multi-value via repeated field)
    if (idsInput) {
      // We'll inject hidden inputs for each ID instead
      // Remove old hidden duplicates
      form.querySelectorAll('.ing-hidden').forEach(el => el.remove());
      selectedIds.forEach(id => {
        const input = document.createElement('input');
        input.type = 'hidden';
        input.name = 'ingredient_ids';
        input.value = id;
        input.className = 'ing-hidden';
        form.appendChild(input);
      });
    }

    // Enable / disable search button
    if (searchBtn) {
      searchBtn.disabled = selectedIds.size === 0;
    }

    // Selected tags in bar
    if (tagsEl) {
      tagsEl.innerHTML = '';
      selectedIds.forEach(id => {
        const chip = document.querySelector(`.ingredient-chip[data-id="${id}"]`);
        if (chip) {
          const span = document.createElement('span');
          span.className = 'selected-tag-pill';
          span.textContent = chip.dataset.name;
          tagsEl.appendChild(span);
        }
      });
    }
  }

  // ── Chip click ───────────────────────────────────────────────────────────────
  chips.forEach(chip => {
    // Restore saved state
    const id = parseInt(chip.dataset.id);
    if (selectedIds.has(id)) chip.classList.add('selected');

    chip.addEventListener('click', () => {
      const chipId = parseInt(chip.dataset.id);
      if (selectedIds.has(chipId)) {
        selectedIds.delete(chipId);
        chip.classList.remove('selected');
      } else {
        selectedIds.add(chipId);
        chip.classList.add('selected');
      }
      updateUI();
    });
  });

  // ── Clear all ────────────────────────────────────────────────────────────────
  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      selectedIds.clear();
      chips.forEach(c => c.classList.remove('selected'));
      updateUI();
    });
  }

  // ── Category tabs ────────────────────────────────────────────────────────────
  let activeCat = 'protein';

  function filterByCategory(cat) {
    activeCat = cat;
    chips.forEach(chip => {
      const matchCat = (chip.dataset.cat === cat);
      const matchSearch = !ingSearch || chip.dataset.name.includes(ingSearch.value.trim());
      chip.classList.toggle('hidden', !(matchCat && matchSearch));
    });
  }

  catTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      catTabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
      filterByCategory(tab.dataset.cat);
    });
  });

  // ── Ingredient search filter ──────────────────────────────────────────────────
  if (ingSearch) {
    ingSearch.addEventListener('input', () => {
      const q = ingSearch.value.trim().toLowerCase();
      chips.forEach(chip => {
        const matchCat = (chip.dataset.cat === activeCat);
        const matchSearch = chip.dataset.name.toLowerCase().includes(q);
        chip.classList.toggle('hidden', !(matchCat && matchSearch));
      });
    });
  }

  // ── Navbar scroll shrink ─────────────────────────────────────────────────────
  const nav = document.getElementById('mainNav');
  if (nav) {
    window.addEventListener('scroll', () => {
      nav.classList.toggle('scrolled', window.scrollY > 40);
    }, { passive: true });
  }

  // ── Match bar animation (results page) ───────────────────────────────────────
  // Set initial width to 0 then animate on load
  document.querySelectorAll('.match-bar-fill').forEach(bar => {
    const target = bar.style.width;
    bar.style.width = '0%';
    setTimeout(() => { bar.style.width = target; }, 150);
  });

  // ── Smooth scroll for hero CTA ────────────────────────────────────────────────
  const heroCta = document.querySelector('a[href="#ingredient-section"]');
  if (heroCta) {
    heroCta.addEventListener('click', e => {
      e.preventDefault();
      document.getElementById('ingredient-section')?.scrollIntoView({ behavior: 'smooth' });
    });
  }

  // ── Init ─────────────────────────────────────────────────────────────────────
  filterByCategory('protein');
  updateUI();
});
