console.log("COMPOUND INTEREST JS LOADED");

document.addEventListener("DOMContentLoaded", function () {
    const btn = document.getElementById("compoundInterestBtn");
    const form = document.getElementById("compoundInterestForm");

    if (!btn || !form) return;

    form.addEventListener("submit", function (e) {
        e.preventDefault();
    });

    btn.addEventListener("click", async function (e) {
        e.preventDefault();

        const formData = new FormData(form);
        const data = Object.fromEntries(formData);

        try {
            const res = await fetch("/tools/compound-interest-calculator/api", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(data)
            });

            const result = await res.json();

            if (result.error) {
                alert(result.error);
                return;
            }

            const box = document.getElementById("compoundInterestResultBox");
            const empty = document.getElementById("compoundInterestResultEmpty");
            if (box) box.style.display = "block";
            if (empty) empty.style.display = "none";

            const maturity = document.getElementById("compoundInterestMaturityValue");
            const earned = document.getElementById("compoundInterestEarned");

            if (maturity) maturity.innerText = "₹" + Number(result.maturity_value || 0).toLocaleString("en-IN");
            if (earned) earned.innerText = "₹" + Number(result.interest_earned || 0).toLocaleString("en-IN");
        } catch (err) {
            console.error("COMPOUND INTEREST FETCH ERROR:", err);
            alert("Something went wrong");
        }
    });
});

