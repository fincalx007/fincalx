const searchInput = document.getElementById("toolSearch");
const themeToggle = document.querySelector("[data-theme-toggle]");

const getSavedTheme = () => {
    try {
        return localStorage.getItem("theme");
    } catch (error) {
        return null;
    }
};

const saveTheme = (theme) => {
    try {
        localStorage.setItem("theme", theme);
    } catch (error) {
        return;
    }
};

const applyTheme = (theme) => {
    const isDark = theme === "dark";
    document.documentElement.dataset.theme = isDark ? "dark" : "light";

    if (themeToggle) {
        themeToggle.setAttribute("aria-pressed", String(isDark));
        themeToggle.setAttribute("aria-label", isDark ? "Switch to light mode" : "Switch to dark mode");
    }
};

const savedTheme = getSavedTheme();
const prefersDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
applyTheme(savedTheme || (prefersDark ? "dark" : "light"));

if (themeToggle) {
    themeToggle.addEventListener("click", () => {
        const nextTheme = document.documentElement.dataset.theme === "dark" ? "light" : "dark";
        saveTheme(nextTheme);
        applyTheme(nextTheme);
    });
}

if (searchInput) {
    const cards = Array.from(document.querySelectorAll(".tool-card"));

    searchInput.addEventListener("input", () => {
        const query = searchInput.value.trim().toLowerCase();
        cards.forEach((card) => {
            const text = card.dataset.search.toLowerCase();
            card.classList.toggle("d-none", query.length > 0 && !text.includes(query));
        });
    });
}

/* ---------- Form Validation ---------- */

(function initFormValidation() {
    const forms = document.querySelectorAll(".calculator-card");

    const validateField = (input) => {
        const value = input.value;
        const type = input.type;
        let message = "";

        if (input.required && (!value || value.trim() === "")) {
            message = input.labels && input.labels[0]
                ? `${input.labels[0].textContent.trim()} is required.`
                : "This field is required.";
        } else if (value && type === "number") {
            const num = parseFloat(value);
            if (Number.isNaN(num)) {
                message = "Please enter a valid number.";
            } else if (input.min !== "" && num < parseFloat(input.min)) {
                message = `Minimum allowed value is ${input.min}.`;
            } else if (input.max !== "" && num > parseFloat(input.max)) {
                message = `Maximum allowed value is ${input.max}.`;
            }
        } else if (value && input.maxLength && input.maxLength > 0 && value.length > input.maxLength) {
            message = `Maximum length is ${input.maxLength} characters.`;
        }

        return message;
    };

    const setInvalid = (input, message) => {
        input.classList.add("is-invalid");
        let feedback = input.parentElement.querySelector(".invalid-feedback");
        if (!feedback) {
            feedback = document.createElement("div");
            feedback.className = "invalid-feedback";
            input.parentElement.appendChild(feedback);
        }
        feedback.textContent = message;
    };

    const clearInvalid = (input) => {
        input.classList.remove("is-invalid");
        const feedback = input.parentElement.querySelector(".invalid-feedback");
        if (feedback) {
            feedback.textContent = "";
        }
    };

    forms.forEach((form) => {
        const inputs = form.querySelectorAll("input, select, textarea");

        inputs.forEach((input) => {
            input.addEventListener("input", () => clearInvalid(input));
            input.addEventListener("change", () => clearInvalid(input));
        });

        form.addEventListener("submit", (event) => {
            let isValid = true;

            inputs.forEach((input) => {
                const message = validateField(input);
                if (message) {
                    setInvalid(input, message);
                    isValid = false;
                } else {
                    clearInvalid(input);
                }
            });

            if (!isValid) {
                event.preventDefault();
                event.stopPropagation();
                const firstInvalid = form.querySelector(".is-invalid");
                if (firstInvalid) {
                    firstInvalid.focus();
                }
            }
        });
    });
})();

