document.documentElement.classList.add('js');

const menu = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#navigation');
const navigationLinks = [...navigation.querySelectorAll('a[href^="#"]')];

function closeMenu() {
  menu.setAttribute('aria-expanded', 'false');
  navigation.classList.remove('is-open');
}
menu.addEventListener('click', () => {
  const open = menu.getAttribute('aria-expanded') !== 'true';
  menu.setAttribute('aria-expanded', String(open));
  navigation.classList.toggle('is-open', open);
});
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') {
    closeMenu();
    menu.focus();
  }
});

// Native fragment navigation preserves browser history, keyboard access and
// shareable section URLs. CSS supplies smooth scrolling and header clearance.
navigationLinks.forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('click', event => {
  if (!event.target.closest('.site-header')) closeMenu();
});

const sections = navigationLinks.map(link => document.querySelector(link.hash));
let scheduled = false;
function updateNavigation() {
  const offset = document.querySelector('.site-header').getBoundingClientRect().height + 45;
  let current = sections[0];
  for (const section of sections) {
    if (section.getBoundingClientRect().top <= offset) current = section;
  }
  if (window.innerHeight + window.scrollY >= document.documentElement.scrollHeight - 8) current = sections.at(-1);
  navigationLinks.forEach(link => {
    if (link.hash === `#${current.id}`) link.setAttribute('aria-current', 'location');
    else link.removeAttribute('aria-current');
  });
  scheduled = false;
}
window.addEventListener('scroll', () => {
  if (!scheduled) { scheduled = true; requestAnimationFrame(updateNavigation); }
}, {passive: true});
window.addEventListener('resize', () => {
  if (window.innerWidth > 800) closeMenu();
  updateNavigation();
});
updateNavigation();

// Disclosure panels live below a separate action row, so opening a panel
// cannot reflow the remaining resource buttons. Native details still work
// when JavaScript is unavailable.
document.querySelectorAll('.paper-resources').forEach(resources => {
  const buttons = [...resources.querySelectorAll('.detail-toggle')];
  const panels = [...resources.querySelectorAll('.paper-detail')];
  function sync() {
    buttons.forEach(button => {
      const panel = document.getElementById(button.getAttribute('aria-controls'));
      button.setAttribute('aria-expanded', String(panel.open));
    });
  }
  buttons.forEach(button => {
    button.hidden = false;
    button.addEventListener('click', () => {
      const panel = document.getElementById(button.getAttribute('aria-controls'));
      const opening = !panel.open;
      panels.forEach(item => { item.open = item === panel && opening; });
      sync();
    });
  });
  panels.forEach(panel => panel.addEventListener('toggle', sync));
});

document.querySelectorAll('.copy-bib').forEach(button => {
  button.addEventListener('click', async () => {
    const code = document.getElementById(button.dataset.copy);
    const text = code.textContent;
    try {
      if (!navigator.clipboard) throw new Error('Clipboard unavailable');
      await navigator.clipboard.writeText(text);
    } catch {
      const selection = window.getSelection();
      const range = document.createRange();
      range.selectNodeContents(code);
      selection.removeAllRanges();
      selection.addRange(range);
      button.textContent = 'Select & copy';
      document.querySelector('#copy-status').textContent = 'Citation selected. Use your device’s Copy command.';
      return;
    }
    button.textContent = 'Copied';
    document.querySelector('#copy-status').textContent = 'BibTeX citation copied.';
    setTimeout(() => {button.textContent = 'Copy';}, 2000);
  });
});

// Retain inbound links to section IDs used by the previous homepage.
const legacySections = {
  '#about-me': '#about', '#-news': '#news',
  '#-selected-publications': '#publications', '#-services': '#service',
  '#-honors-and-awards': '#honors', '#-teaching': '#teaching',
  '#-students': '#students', '#-alumni': '#students'
};
if (legacySections[location.hash]) location.replace(legacySections[location.hash]);
