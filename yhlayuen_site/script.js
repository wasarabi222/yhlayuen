const header = document.querySelector("[data-header]");
const nav = document.querySelector("[data-nav]");
const menuToggle = document.querySelector("[data-menu-toggle]");
const slides = Array.from(document.querySelectorAll("[data-hero-slide]"));
const count = document.querySelector("[data-hero-count]");
const title = document.querySelector("[data-hero-title]");
const prev = document.querySelector("[data-hero-prev]");
const next = document.querySelector("[data-hero-next]");
const langOptions = Array.from(document.querySelectorAll("[data-lang-option]"));

const slideMeta = [
  { count: "01 / 02", ko: "창조 · Creativity", en: "Creation · Creativity" },
  { count: "02 / 02", ko: "부활 · Resurrection", en: "Resurrection" },
];

const languageStorageKey = "yhlayuen-language";
let currentSlide = 0;
let timer;
let currentLang = "ko";

function getContentValue(key, lang) {
  return key.split(".").reduce((value, part) => value?.[part], window.YHLAYUEN_CONTENT)?.[lang];
}

function applyContent(lang) {
  document.querySelectorAll("[data-i18n]").forEach((element) => {
    const value = getContentValue(element.dataset.i18n, lang);
    if (value !== undefined) element.textContent = value;
  });

  document.querySelectorAll("[data-i18n-html]").forEach((element) => {
    const value = getContentValue(element.dataset.i18nHtml, lang);
    if (value !== undefined) element.innerHTML = value;
  });
}

function setHeaderState() {
  if (document.body.classList.contains("inner-page")) {
    header?.classList.add("is-scrolled");
    return;
  }

  header?.classList.toggle("is-scrolled", window.scrollY > 16);
}

function showSlide(index) {
  if (!slides.length) return;
  currentSlide = (index + slides.length) % slides.length;

  slides.forEach((slide, slideIndex) => {
    slide.classList.toggle("is-active", slideIndex === currentSlide);
  });

  if (count) count.textContent = slideMeta[currentSlide].count;
  if (title) title.textContent = slideMeta[currentSlide][currentLang];
}

function startTimer() {
  window.clearInterval(timer);
  timer = window.setInterval(() => showSlide(currentSlide + 1), 6200);
}

function toggleMenu() {
  const isOpen = !nav.classList.contains("is-open");
  nav.classList.toggle("is-open", isOpen);
  header.classList.toggle("is-open", isOpen);
  document.body.classList.toggle("is-menu-open", isOpen);
  menuToggle.setAttribute("aria-expanded", String(isOpen));
}

function setLanguage(lang) {
  currentLang = lang === "en" ? "en" : "ko";
  document.body.dataset.lang = currentLang;
  document.documentElement.lang = currentLang;

  try {
    window.localStorage.setItem(languageStorageKey, currentLang);
  } catch {
    // Local files can block storage in some browser settings.
  }

  langOptions.forEach((button) => {
    button.setAttribute("aria-pressed", String(button.dataset.langOption === currentLang));
  });

  applyContent(currentLang);
  if (slides.length) showSlide(currentSlide);
}

window.addEventListener("scroll", setHeaderState, { passive: true });

menuToggle?.addEventListener("click", toggleMenu);

nav?.addEventListener("click", (event) => {
  if (event.target.matches("a") && nav.classList.contains("is-open")) {
    toggleMenu();
  }
});

langOptions.forEach((button) => {
  button.addEventListener("click", () => setLanguage(button.dataset.langOption));
});

prev?.addEventListener("click", () => {
  showSlide(currentSlide - 1);
  startTimer();
});

next?.addEventListener("click", () => {
  showSlide(currentSlide + 1);
  startTimer();
});

try {
  currentLang = window.localStorage.getItem(languageStorageKey) || "ko";
} catch {
  currentLang = "ko";
}

setHeaderState();
setLanguage(currentLang);
showSlide(0);
startTimer();
