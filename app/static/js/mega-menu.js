// Mega menu hover and keyboard accessibility
(() => {
    const dropdown = document.getElementById('toolsDropdown');
    if (!dropdown) return;
    const toggle = document.getElementById('toolsToggle');
    const menu = dropdown.querySelector('.tools-mega-menu') || dropdown.querySelector('.tools-dropdown.mega-menu');
    let hideTimer = null;

    function openMenu() {
        dropdown.classList.add('open');
        menu.classList.add('show');
    }
    function closeMenu() {
        dropdown.classList.remove('open');
        menu.classList.remove('show');
    }

    // Hover behaviour
    dropdown.addEventListener('mouseenter', () => {
        clearTimeout(hideTimer);
        openMenu();
    });
    dropdown.addEventListener('mouseleave', () => {
        hideTimer = setTimeout(closeMenu, 220);
    });

    // Focus / keyboard behaviour
    toggle.addEventListener('focus', () => {
        openMenu();
    });
    toggle.addEventListener('blur', (e) => {
        // delay to allow focus to move into menu
        setTimeout(() => {
            if (!menu.contains(document.activeElement) && document.activeElement !== toggle) {
                closeMenu();
            }
        }, 120);
    });

    // Close on Escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeMenu();
    });

    // Close when clicking outside
    document.addEventListener('click', (e) => {
        if (!dropdown.contains(e.target)) closeMenu();
    });

    // Mobile: convert category headings into accordion toggles
    function initMobileAccordion() {
        const isMobile = window.matchMedia('(max-width: 575px)').matches;
        const headings = menu.querySelectorAll('.tools-column h4');
        headings.forEach((h) => {
            // next sibling links until next h4 or end
            let next = h.nextElementSibling;
            const group = [];
            while (next && next.tagName !== 'H4') {
                group.push(next);
                next = next.nextElementSibling;
            }
            if (isMobile) {
                group.forEach(el => el.style.display = 'none');
                h.setAttribute('role', 'button');
                h.tabIndex = 0;
                if (!h.dataset.bound) {
                    h.addEventListener('click', () => {
                        const visible = group[0].style.display === 'block';
                        group.forEach(el => el.style.display = visible ? 'none' : 'block');
                    });
                    h.addEventListener('keydown', (e) => {
                        if (e.key === 'Enter' || e.key === ' ') {
                            e.preventDefault();
                            const visible = group[0].style.display === 'block';
                            group.forEach(el => el.style.display = visible ? 'none' : 'block');
                        }
                    });
                    h.dataset.bound = '1';
                }
            } else {
                group.forEach(el => el.style.display = '');
                h.removeAttribute('role');
                h.tabIndex = -1;
            }
        });
    }

    initMobileAccordion();
    window.addEventListener('resize', () => initMobileAccordion());
})();
