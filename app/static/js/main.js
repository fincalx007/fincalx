/**
 * FinCalX - Frontend Interactions
 * Handles: Theme, Search, Form Validation, Loading States, Scroll, Double-Submit Prevention
 */

// ============================================
// THEME MANAGEMENT
// ============================================
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
        // Silently fail if localStorage unavailable
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

// Initialize theme on load to prevent flash
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

// ============================================
// SEARCH FUNCTIONALITY
// ============================================
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

// ============================================
// FORM VALIDATION + LOADING + DOUBLE-SUBMIT PREVENTION
// ============================================
(function initFormValidation() {
    const forms = document.querySelectorAll(".calculator-card");
    
    // Track submitted forms to handle browser back button
    const submittedForms = new WeakSet();

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
        
        // Add animation for error feedback
        feedback.style.animation = "shakeIn 0.4s ease";
        setTimeout(() => { feedback.style.animation = ""; }, 400);
    };

    const clearInvalid = (input) => {
        input.classList.remove("is-invalid");
        const feedback = input.parentElement.querySelector(".invalid-feedback");
        if (feedback) {
            feedback.textContent = "";
        }
    };

    // Enhanced loading state with spinner
    const setLoading = (button, loading) => {
        if (!button) return;
        
        if (loading) {
            button.disabled = true;
            button.dataset.originalText = button.innerHTML;
            button.classList.add("btn-loading");
            
            // Create spinner element
            const spinner = document.createElement("span");
            spinner.className = "loading-spinner";
            spinner.setAttribute("aria-hidden", "true");
            
            button.innerHTML = "";
            button.appendChild(spinner);
            button.appendChild(document.createTextNode(" Calculating..."));
        } else {
            button.disabled = false;
            button.innerHTML = button.dataset.originalText || "Calculate";
            button.classList.remove("btn-loading");
        }
    };

    // Scroll to result section smoothly
    const scrollToResult = (resultSection) => {
        if (!resultSection) return;
        
        // Calculate offset for sticky navigation
        const navHeight = document.querySelector(".site-navbar")?.offsetHeight || 70;
        const resultPosition = resultSection.getBoundingClientRect().top + window.pageYOffset;
        
        window.scrollTo({
            top: resultPosition - navHeight - 20,
            behavior: "smooth"
        });
    };

    // Scroll to first error field
    const scrollToError = (firstInvalid) => {
        if (!firstInvalid) return;
        
        const navHeight = document.querySelector(".site-navbar")?.offsetHeight || 70;
        const fieldPosition = firstInvalid.getBoundingClientRect().top + window.pageYOffset;
        
        window.scrollTo({
            top: fieldPosition - navHeight - 20,
            behavior: "smooth"
        });
        
        // Focus on the invalid field
        setTimeout(() => firstInvalid.focus(), 400);
    };

    forms.forEach((form) => {
        const inputs = form.querySelectorAll("input, select, textarea");
        const submitBtn = form.querySelector('button[type="submit"]');
        const actionTarget = form.getAttribute("action");

        // Clear validation on input change
        inputs.forEach((input) => {
            input.addEventListener("input", () => clearInvalid(input));
            input.addEventListener("change", () => clearInvalid(input));
            
            // Also clear on paste for better UX
            input.addEventListener("paste", () => {
                setTimeout(() => clearInvalid(input), 10);
            });
        });

        form.addEventListener("submit", (event) => {
            // ===== FIX 1: Prevent Double Submission =====
            if (submitBtn && submitBtn.disabled) {
                event.preventDefault();
                return;
            }

            // ===== FIX 2: Client-Side Validation =====
            let isValid = true;
            let firstInvalid = null;

            inputs.forEach((input) => {
                const message = validateField(input);
                if (message) {
                    setInvalid(input, message);
                    isValid = false;
                    if (!firstInvalid) firstInvalid = input;
                } else {
                    clearInvalid(input);
                }
            });

            if (!isValid) {
                event.preventDefault();
                event.stopPropagation();
                scrollToError(firstInvalid);
                return;
            }

            // ===== FIX 3: Set Loading State =====
            setLoading(submitBtn, true);
            submittedForms.add(form);

            // ===== FIX 4: Store form submission state =====
            try {
                sessionStorage.setItem("formSubmitted", "true");
            } catch (e) {
                // Silently fail if sessionStorage unavailable
            }

            // ===== FIX 5: Scroll handling on result =====
            // After page loads with result, scroll to result section
            window.addEventListener("load", () => {
                if (sessionStorage.getItem("formSubmitted") === "true") {
                    sessionStorage.removeItem("formSubmitted");
                    
                    // Check if there's a result section to scroll to
                    const resultSection = document.querySelector("#result-section, .result-card");
                    if (resultSection) {
                        setTimeout(() => scrollToResult(resultSection), 100);
                    }
                }
            });
        });

        // ===== FIX 6: Handle browser back button =====
        window.addEventListener("pageshow", (event) => {
            // Reset loading state when navigating back
            if (submitBtn) {
                setLoading(submitBtn, false);
            }
            
            // Clear any cached submission state
            try {
                sessionStorage.removeItem("formSubmitted");
            } catch (e) {
                // Silently fail
            }
        });
    });
})();


// ============================================
// SCROLL FIXES FOR MOBILE/NATIVE
// ============================================
// Fix for iOS Safari scroll issues
(function fixScrollBehavior() {
    // Fix for result section not scrolling properly on mobile
    const resultSections = document.querySelectorAll("#result-section");
    
    resultSections.forEach(section => {
        // Ensure smooth scroll works on iOS
        section.style.scrollBehavior = "smooth";
        section.style.webkitOverflowScrolling = "touch";
    });

    // Fix horizontal scroll on mobile - prevent body overflow
    document.body.style.overflowX = "hidden";
    
    // Handle keyboard showing on mobile
    const inputs = document.querySelectorAll("input, select, textarea");
    inputs.forEach(input => {
        input.addEventListener("focus", () => {
            // Small delay to allow keyboard to open
            setTimeout(() => {
                window.scrollTo({
                    top: window.scrollY + 1,
                    behavior: "instant"
                });
            }, 100);
        });
    });
})();


// ============================================
// ENHANCED ERROR DISPLAY
// ============================================
(function enhanceErrorDisplay() {
    // Add keyboard accessibility to error messages
    const invalidInputs = document.querySelectorAll(".is-invalid");
    
    invalidInputs.forEach(input => {
        // Make invalid inputs accessible
        input.setAttribute("aria-describedby", 
            input.parentElement.querySelector(".invalid-feedback")?.id || "invalid-feedback");
        input.setAttribute("aria-invalid", "true");
    });
})();


// ============================================
// CSS KEYFRAME FOR SHAKE ANIMATION (should be in styles.css)
// ============================================
// This is handled via JavaScript to keep animations in one place
const style = document.createElement("style");
style.textContent = `
@keyframes shakeIn {
    0%, 100% { transform: translateX(0); }
    20% { transform: translateX(-8px); }
    40% { transform: translateX(8px); }
    60% { transform: translateX(-4px); }
    80% { transform: translateX(4px); }
}

.loading-spinner {
    display: inline-block;
    width: 16px;
    height: 16px;
    border: 2px solid rgba(255,255,255,0.3);
    border-top-color: #fff;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    vertical-align: middle;
    margin-right: 8px;
}

.btn-loading .loading-spinner {
    border-color: rgba(108, 76, 241, 0.3);
    border-top-color: #6c4cf1;
    background: transparent;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* Smooth transitions for form interactions */
.form-control, .form-select, .btn {
    transition: all 0.2s ease;
}

.form-control:focus, .form-select:focus {
    transition: box-shadow 0.2s ease, border-color 0.2s ease;
}

/* Focus visible for accessibility */
.btn:focus-visible {
    outline: 3px solid rgba(108, 76, 241, 0.5);
    outline-offset: 2px;
}

/* Smooth loading button */
.btn-loading {
    cursor: wait;
    opacity: 0.9;
}
`;
document.head.appendChild(style);


// ============================================
// PREVENT ACCIDENTAL DOUBLE SUBMISSION
// ============================================
(function preventDoubleSubmission() {
    // Additional protection: disable form on submit
    document.addEventListener("submit", (event) => {
        const form = event.target;
        const submitBtn = form.querySelector('button[type="submit"]');
        
        if (submitBtn && submitBtn.disabled) {
            event.preventDefault();
            return false;
        }
    }, true);
})();
