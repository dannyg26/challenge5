(function () {
  function qs(selector, root) {
    return (root || document).querySelector(selector);
  }
  function qsa(selector, root) {
    return Array.from((root || document).querySelectorAll(selector));
  }

  const navToggle = qs('[data-nav-toggle]');
  const navMenu = qs('[data-nav-menu]');
  if (navToggle && navMenu) {
    navToggle.addEventListener('click', function () {
      const isOpen = navMenu.classList.toggle('open');
      navToggle.setAttribute('aria-expanded', String(isOpen));
    });

    qsa('a', navMenu).forEach((link) => {
      link.addEventListener('click', () => {
        navMenu.classList.remove('open');
        navToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  const modalBackdrop = qs('[data-modal-backdrop]');
  const openers = qsa('[data-open-demo-modal]');
  const closers = qsa('[data-close-demo-modal]');

  function openModal() {
    if (!modalBackdrop) return;
    modalBackdrop.style.display = 'flex';
    const closeButton = qs('[data-close-demo-modal]', modalBackdrop);
    if (closeButton) closeButton.focus();
  }

  function closeModal() {
    if (!modalBackdrop) return;
    modalBackdrop.style.display = 'none';
  }

  openers.forEach((btn) => btn.addEventListener('click', openModal));
  closers.forEach((btn) => btn.addEventListener('click', closeModal));

  qsa('form[data-demo-form]').forEach((form) => {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      try {
        form.reset();
      } catch (_) {
        // ignore
      }
    });
  });

  if (modalBackdrop) {
    modalBackdrop.addEventListener('click', (e) => {
      if (e.target === modalBackdrop) closeModal();
    });
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modalBackdrop.style.display === 'flex') closeModal();
    });
  }
})();
