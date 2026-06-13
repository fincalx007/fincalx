console.log("EMERGENCY FUND JS LOADED");

document.addEventListener("DOMContentLoaded", function () {
    const btn = document.getElementById("emergencyFundBtn");
    const form = document.getElementById("emergencyFundForm");

    if (!btn || !form) return;

    form.addEventListener("submit", function (e) {
        e.preventDefault();
    });

    btn.addEventListener("click", async function (e) {
        e.preventDefault();

        const formData = new FormData(form);
        const data = Object.fromEntries(formData);

        try {
            const res = await fetch("/tools/emergency-fund-calculator/api", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(data)
            });

            const result = await res.json();

            if (result.error) {
                alert(result.error);
                return;
            }

            const box = document.getElementById("emergencyFundResultBox");
            const empty = document.getElementById("emergencyFundResultEmpty");
            if (box) box.style.display = "block";
            if (empty) empty.style.display = "none";

            const rec = document.getElementById("emergencyFundRecommended");
            if (rec) rec.innerText = "₹" + Number(result.recommended_emergency_fund || 0).toLocaleString("en-IN");
        } catch (err) {
            console.error("EMERGENCY FUND FETCH ERROR:", err);
            alert("Something went wrong");
        }
    });
});

