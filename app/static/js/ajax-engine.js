console.log("ENGINE LOADED");

document.addEventListener("DOMContentLoaded", function () {
    const calculatorConfigs = {
        sip: {
            resultBoxId: "resultBox",
            emptyBoxId: "sipResultEmpty",
            fields: {
                totalValue: {key: "total_value", format: formatMoney},
                investedAmount: {key: "invested_amount", format: formatMoney},
                returns: {key: "estimated_returns", format: formatMoney}
            }
        },
        emi: {
            resultBoxId: "emiResultBox",
            emptyBoxId: "emiResultEmpty",
            fields: {
                emiValue: {key: "emi", format: formatMoney},
                emiTotalInterest: {key: "total_interest", format: formatMoney},
                emiTotalPayment: {key: "total_payment", format: formatMoney}
            }
        },
        salary: {
            resultBoxId: "salaryResultBox",
            emptyBoxId: "salaryResultEmpty",
            fields: {
                salaryMonthly: {key: "monthly", format: formatMoney},
                salaryInHand: {key: "in_hand", format: formatMoney},
                salaryTotalDeductions: {key: "total_deductions", format: formatMoney},
                salaryPf: {key: "pf", format: formatMoney},
                salaryTax: {key: "tax", format: formatMoney},
                salaryBasic: {key: "basic", format: formatMoney},
                salaryHra: {key: "hra", format: formatMoney}
            }
        },
        overlap: {
            resultBoxId: "overlapResultBox",
            emptyBoxId: "overlapResultEmpty",
            fields: {
                overlapFirstCount: {key: "first_count"},
                overlapSecondCount: {key: "second_count"},
                overlapPercentage: {key: "overlap_percentage", format: formatPercent}
            },
            afterUpdate: updateOverlapList
        }
    };

    document.querySelectorAll("[data-submit]").forEach(function (btn) {
        const key = btn.dataset.submit;
        const form = document.getElementById(key + "Form");

        if (!form) {
            console.log("Form not found for:", key);
            return;
        }

        form.addEventListener("submit", function (event) {
            event.preventDefault();
        });

        btn.addEventListener("click", function (event) {
            event.preventDefault();
            handleSubmit(key, form);
        });
    });

    async function handleSubmit(key, form) {
        const api = form.dataset.api;

        if (!api) {
            console.log("API endpoint not found for:", key);
            return;
        }

        const formData = new FormData(form);
        const data = Object.fromEntries(formData);

        console.log("FORM DATA:", data);

        try {
            const response = await fetch(api, {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(data)
            });

            const result = await response.json();

            console.log("API RESPONSE:", result);

            if (result.error) {
                alert(result.error);
                return;
            }

            updateResult(key, result);
        } catch (err) {
            console.error("FETCH ERROR:", err);
            alert("Something went wrong");
        }
    }

    function updateResult(key, result) {
        const config = calculatorConfigs[key] || {};

        showElement(config.resultBoxId);
        hideElement(config.emptyBoxId);
        updateFields(config.fields, result);

        if (typeof config.afterUpdate === "function") {
            config.afterUpdate(result);
        }
    }

    function updateFields(fields, result) {
        Object.keys(fields || {}).forEach(function (id) {
            const element = document.getElementById(id);

            if (!element) {
                return;
            }

            const field = fields[id];
            const value = result[field.key];

            if (value === undefined || value === null) {
                return;
            }

            element.innerText = field.format ? field.format(value) : value;
        });
    }

    function showElement(id) {
        const element = document.getElementById(id);

        if (!element) {
            return;
        }

        element.classList.remove("d-none");
        element.style.display = "block";
    }

    function hideElement(id) {
        const element = document.getElementById(id);

        if (!element) {
            return;
        }

        element.classList.add("d-none");
        element.style.display = "none";
    }

    function updateOverlapList(result) {
        const list = document.getElementById("overlapCommonList");
        const empty = document.getElementById("overlapNoCommon");

        if (!list || !empty) {
            return;
        }

        list.innerHTML = "";

        if (Array.isArray(result.common) && result.common.length) {
            result.common.forEach(function (name) {
                const item = document.createElement("li");
                item.innerText = titleCase(name);
                list.appendChild(item);
            });
            list.style.display = "block";
            empty.style.display = "none";
        } else {
            list.style.display = "none";
            empty.style.display = "block";
        }
    }

    function formatMoney(value) {
        return "\u20b9 " + Number(value || 0).toLocaleString("en-IN", {
            maximumFractionDigits: 2
        });
    }

    function formatPercent(value) {
        return Number(value || 0).toLocaleString("en-IN", {
            maximumFractionDigits: 2
        }) + "%";
    }

    function titleCase(value) {
        return String(value || "").replace(/\w\S*/g, function (text) {
            return text.charAt(0).toUpperCase() + text.slice(1).toLowerCase();
        });
    }
});
