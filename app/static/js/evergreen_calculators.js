document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".evergreen-calculator-form").forEach(function (form) {
        form.addEventListener("submit", async function (event) {
            event.preventDefault();

            const api = form.dataset.api;
            const data = Object.fromEntries(new FormData(form));
            const resultBox = document.getElementById(form.id.replace("Form", "ResultBox"));
            const emptyBox = document.getElementById(form.id.replace("Form", "ResultEmpty"));

            try {
                const response = await fetch(api, {
                    method: "POST",
                    headers: {"Content-Type": "application/json"},
                    body: JSON.stringify(data)
                });
                const result = await response.json();

                if (!response.ok || result.error) {
                    alert(result.error || "Please check your inputs and try again.");
                    return;
                }

                form.closest(".container").querySelectorAll("[data-result-key]").forEach(function (element) {
                    const key = element.dataset.resultKey;
                    if (Object.prototype.hasOwnProperty.call(result, key)) {
                        element.innerText = formatValue(key, result[key]);
                    }
                });

                if (resultBox) resultBox.classList.remove("d-none");
                if (emptyBox) emptyBox.classList.add("d-none");
            } catch (error) {
                console.error("Evergreen calculator error:", error);
                alert("Something went wrong. Please try again.");
            }
        });
    });

    function formatValue(key, value) {
        const percentKeys = new Set([
            "savings_rate",
            "debt_to_income_ratio",
            "real_rate_of_return",
            "portfolio_return",
            "equity_allocation",
            "debt_allocation",
            "cash_allocation",
            "other_allocation"
        ]);
        const countKeys = new Set([
            "estimated_years_to_double",
            "months_to_payoff",
            "years_to_payoff",
            "months_to_target",
            "years_to_target",
            "new_months_to_payoff",
            "total_quantity"
        ]);

        const number = Number(value || 0);
        if (percentKeys.has(key)) {
            return number.toLocaleString("en-IN", {maximumFractionDigits: 2}) + "%";
        }
        if (countKeys.has(key)) {
            return number.toLocaleString("en-IN", {maximumFractionDigits: 2});
        }
        return "Rs. " + number.toLocaleString("en-IN", {maximumFractionDigits: 2});
    }
});
