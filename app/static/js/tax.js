document.addEventListener("DOMContentLoaded", function () {
    console.log("TAX JS LOADED");

    const btn = document.getElementById("taxBtn");
    const form = document.getElementById("taxForm");
    const regime = document.getElementById("regime");
    const deductions = document.getElementById("deductions");

    if (!btn) {
        console.log("Button not found");
        return;
    }

    if (!form) {
        console.log("Form not found");
        return;
    }

    function toggleDeductions() {
        if (!regime || !deductions) {
            return;
        }

        if (regime.value === "new") {
            deductions.disabled = true;
            deductions.value = 0;
        } else {
            deductions.disabled = false;
        }
    }

    if (regime) {
        regime.addEventListener("change", toggleDeductions);
    }
    toggleDeductions();

    form.addEventListener("submit", function (e) {
        e.preventDefault();
    });

    btn.addEventListener("click", async function (e) {
        console.log("Button clicked");

        e.preventDefault();

        const formData = new FormData(form);
        const data = Object.fromEntries(formData);

        if (!("deductions" in data)) {
            data.deductions = "0";
        }

        console.log("FORM DATA:", data);

        try {
            const res = await fetch("/tools/income-tax-calculator/api", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(data)
            });

            const result = await res.json();

            console.log("API RESPONSE:", result);

            if (result.error) {
                alert(result.error);
                return;
            }

            document.getElementById("taxResultBox").style.display = "block";
            document.getElementById("taxResultEmpty").style.display = "none";
            document.getElementById("taxTip").style.display = "block";
            document.getElementById("taxRegime").innerText = result.regime;
            document.getElementById("taxableIncome").innerText = formatMoney(result.taxable_income);
            document.getElementById("baseTax").innerText = formatMoney(result.base_tax);
            document.getElementById("cess").innerText = formatMoney(result.cess);
            document.getElementById("totalTax").innerText = formatMoney(result.total_tax);

            const surchargeRow = document.getElementById("surchargeRow");
            const surcharge = Number(result.surcharge || 0);
            if (surcharge > 0) {
                document.getElementById("surcharge").innerText = formatMoney(surcharge);
                surchargeRow.style.display = "flex";
            } else {
                surchargeRow.style.display = "none";
            }
        } catch (err) {
            console.error(err);
            alert("Something went wrong");
        }
    });
});

function formatMoney(value) {
    return "\u20b9 " + Number(value || 0).toLocaleString("en-IN", {
        maximumFractionDigits: 2
    });
}
