// === Floating Sparkles (Background Stars) ===
function createStar() {
  const star = document.createElement("div");
  star.className = "star";
  star.style.left = Math.random() * 100 + "vw";
  star.style.animationDuration = 1 + Math.random() * 2 + "s";
  document.getElementById("hero")?.appendChild(star);
  setTimeout(() => star.remove(), 3000);
}
setInterval(createStar, 500);

// === Typewriter Text Effect ===
const phrases = [
 "Discover 10+ Amazing College Events in One Place!",
  "From Tech Conferences to Music Festivals - We've Got It All!",
  "Join the EventBox community and never miss an event!",
  "Your Ultimate Hub for College Events - All in One Place!",
  "Unforgettable Experiences Await You at EventBox!",
  "Explore and Attend Events You’re Passionate About!",
  "Get the Latest Updates on Campus Events - Stay in the Loop!",
  "EventBox: Connecting You to The Best College Events!",
  "Experience College Life Like Never Before - With EventBox!",
  "Join Now and Be Part of the Most Exciting Events in Town!"
];
let i = 0, j = 0, currentPhrase = [], isDeleting = false;

function loopTypewriter() {
  const typewriter = document.querySelector(".typewriter");
  if (!typewriter) return;

  if (i < phrases.length) {
    if (!isDeleting && j <= phrases[i].length) {
      currentPhrase.push(phrases[i][j]);
      typewriter.textContent = currentPhrase.join("");
      j++;
    } else if (isDeleting && j > 0) {
      currentPhrase.pop();
      typewriter.textContent = currentPhrase.join("");
      j--;
    }

    if (j === phrases[i].length) isDeleting = true;
    if (j === 0 && isDeleting) {
      isDeleting = false;
      i = (i + 1) % phrases.length;
    }

    setTimeout(loopTypewriter, isDeleting ? 50 : 150);
  }
}
loopTypewriter();

// === Magic Sound on Button Hover ===
const buttons = document.querySelectorAll(".magic-btn");
const magicSound = new Audio("/static/sounds/magic.mp3");

buttons.forEach(btn => {
  btn.addEventListener("mouseenter", () => {
    magicSound.currentTime = 0;
    magicSound.play();
  });
});

// === Page Loader & Fade-In Transition ===
window.addEventListener("load", () => {
  document.body.classList.add("loaded");
  const loader = document.getElementById("loader");
  if (loader) loader.style.display = "none";
});

// === Particle Background (tsParticles) ===
tsParticles.load("tsparticles", {
  fullScreen: { enable: true, zIndex: -1 },
  particles: {
    number: { value: 80 },
    color: { value: "#ffffff" },
    shape: { type: "circle" },
    opacity: { value: 0.7 },
    size: { value: 2 },
    move: {
      enable: true,
      speed: 1.5,
      direction: "none",
      outModes: { default: "bounce" }
    }
  },
  background: { color: "#0a0a0a" }
});

function filterCategory(selected) {
  const cards = document.querySelectorAll(".trick-card");
  cards.forEach(card => {
    const cat = card.getAttribute("data-category");
    card.style.display = (selected === "all" || cat === selected) ? "block" : "none";
  });
}

function searchTricks() {
  const searchTerm = document.getElementById("searchInput").value.toLowerCase();
  const cards = document.querySelectorAll(".trick-card");

  cards.forEach(card => {
    const title = card.getAttribute("data-title");
    card.style.display = title.includes(searchTerm) ? "block" : "none";
  });
}

function filterCategory(selected) {
  const cards = document.querySelectorAll(".trick-card");
  selected = selected.toLowerCase();

  cards.forEach(card => {
    const cat = card.getAttribute("data-category");
    const matchesCategory = selected === "all" || cat === selected;
    const isVisible = card.style.display !== "none";

    card.style.display = matchesCategory && isVisible ? "block" : "none";
  });
}

function filterCategory(selected) {
  const cards = document.querySelectorAll(".trick-card");
  selected = selected.toLowerCase();

  cards.forEach(card => {
    const cat = card.getAttribute("data-category");
    const matchesCategory = selected === "all" || cat === selected;
    const isVisible = card.style.display !== "none";

    card.style.display = matchesCategory && isVisible ? "block" : "none";
  });
}

function searchTricks() {
  const searchTerm = document.getElementById("searchInput").value.toLowerCase();
  const cards = document.querySelectorAll(".trick-card");

  cards.forEach(card => {
    const title = card.getAttribute("data-title");
    card.style.display = title.includes(searchTerm) ? "block" : "none";
  });
}

// === Reveal Sections on Scroll ===
const revealSections = document.querySelectorAll(".reveal");

const revealOnScroll = () => {
  const triggerBottom = window.innerHeight * 0.85;
  revealSections.forEach(section => {
    const top = section.getBoundingClientRect().top;
    if (top < triggerBottom) section.classList.add("active");
  });
};

window.addEventListener("scroll", revealOnScroll);
revealOnScroll(); // Trigger on load

// === Copy Trick to Clipboard (if copy button exists) ===
const copyBtn = document.querySelector(".copy-trick-btn");
if (copyBtn) {
  copyBtn.addEventListener("click", () => {
    const trickContent = document.querySelector(".trick-content");
    if (!trickContent) return;
    navigator.clipboard.writeText(trickContent.innerText).then(() => {
      copyBtn.textContent = "Copied!";
      setTimeout(() => (copyBtn.textContent = "Copy Trick"), 1500);
    });
  });
}

// === Highlight Category on Hover ===
const categoryItems = document.querySelectorAll(".category-card");

categoryItems.forEach(item => {
  item.addEventListener("mouseenter", () => {
    item.classList.add("hovered");
  });
  item.addEventListener("mouseleave", () => {
    item.classList.remove("hovered");
  });
});

// === Count Up Animation (e.g., stats) ===
const counters = document.querySelectorAll(".counter");
const speed = 100;

counters.forEach(counter => {
  const updateCount = () => {
    const target = +counter.getAttribute("data-target");
    const count = +counter.innerText;

    const increment = Math.ceil(target / speed);
    if (count < target) {
      counter.innerText = count + increment;
      setTimeout(updateCount, 20);
    } else {
      counter.innerText = target;
    }
  };

  const observer = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        updateCount();
        obs.unobserve(counter);
      }
    });
  }, { threshold: 1 });

  observer.observe(counter);
});

// === Live Password Match Check ===
const password1 = document.querySelector("input[name='password1']");
const password2 = document.querySelector("input[name='password2']");
const registerBtn = document.querySelector(".register-form button");

function checkPasswordMatch() {
  if (!password1 || !password2 || !registerBtn) return;
  const match = password1.value === password2.value;
  registerBtn.disabled = !match;
  registerBtn.style.opacity = match ? "1" : "0.5";
}

if (password1 && password2) {
  password1.addEventListener("input", checkPasswordMatch);
  password2.addEventListener("input", checkPasswordMatch);
}

// === Glow Button on Focus ===
const inputs = document.querySelectorAll(".register-form input");
inputs.forEach(input => {
  input.addEventListener("focus", () => {
    input.style.boxShadow = "0 0 10px #9b59b6";
  });
  input.addEventListener("blur", () => {
    input.style.boxShadow = "none";
  });
});


// === Password Visibility Toggle (Login & Forgot Password) ===
document.addEventListener("DOMContentLoaded", () => {
  const toggleFields = document.querySelectorAll(".toggle-password");

  toggleFields.forEach(toggle => {
    toggle.addEventListener("click", () => {
      const input = document.querySelector(`#${toggle.dataset.target}`);
      if (input) {
        const isHidden = input.getAttribute("type") === "password";
        input.setAttribute("type", isHidden ? "text" : "password");
        toggle.textContent = isHidden ? "🙈" : "👁️";
      }
    });
  });
});

// Password visibility toggle
document.addEventListener("DOMContentLoaded", () => {
  const toggleFields = document.querySelectorAll(".toggle-password");

  toggleFields.forEach(toggle => {
    toggle.addEventListener("click", () => {
      const input = document.querySelector(`#${toggle.dataset.target}`);
      if (input) {
        const isHidden = input.getAttribute("type") === "password";
        input.setAttribute("type", isHidden ? "text" : "password");
        toggle.textContent = isHidden ? "🙈" : "👁️";
      }
    });
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.querySelector("input[name='q']");

  if (searchInput) {
    searchInput.addEventListener("focus", () => {
      searchInput.select();
    });
  }
});
