console.log("LUMPSUM JS LOADED");

document.addEventListener("DOMContentLoaded", function () {
    const btn = document.getElementById("lumpsumBtn");
    const form = document.getElementById("lumpsumForm");

    if (!btn || !form) return;

    form.addEventListener("submit", function (e) {
        e.preventDefault();
    });

    btn.addEventListener("click", async function (e) {
        e.preventDefault();

        const formData = new FormData(form);
        const data = Object.fromEntries(formData);

        try {
            const res = await fetch("/tools/lumpsum-calculator/api", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(data)
            });

            const result = await res.json();

            if (result.error) {
                alert(result.error);
                return;
            }

            const box = document.getElementById("lumpsumResultBox");
            const empty = document.getElementById("lumpsumResultEmpty");
            if (box) box.style.display = "block";
            if (empty) empty.style.display = "none";

            const maturity = document.getElementById("lumpsumMaturityValue");
            const invested = document.getElementById("lumpsumInvestedAmount");
            const returns = document.getElementById("lumpsumEstimatedReturns");

            if (maturity) maturity.innerText = "₹" + Number(result.maturity_value || 0).toLocaleString("en-IN");
            if (invested) invested.innerText = "₹" + Number(result.invested_amount || 0).toLocaleString("en-IN");
            if (returns) returns.innerText = "₹" + Number(result.estimated_returns || 0).toLocaleString("en-IN");
        } catch (err) {
            console.error("LUMPSUM FETCH ERROR:", err);
            alert("Something went wrong");
        }
    });
});

