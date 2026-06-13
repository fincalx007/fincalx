console.log("GOAL JS LOADED");

document.addEventListener("DOMContentLoaded", function () {
    const btn = document.getElementById("goalBtn");
    const form = document.getElementById("goalForm");

    if (!btn || !form) return;

    form.addEventListener("submit", function (e) {
        e.preventDefault();
    });

    btn.addEventListener("click", async function (e) {
        e.preventDefault();

        const formData = new FormData(form);
        const data = Object.fromEntries(formData);

        try {
            const res = await fetch("/tools/goal-calculator/api", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(data)
            });

            const result = await res.json();

            if (result.error) {
                alert(result.error);
                return;
            }

            const resultBox = document.getElementById("goalResultBox");
            const emptyBox = document.getElementById("goalResultEmpty");
            if (resultBox) resultBox.style.display = "block";
            if (emptyBox) emptyBox.style.display = "none";

            const monthly = document.getElementById("goalMonthly");
            if (monthly) monthly.innerText =
                "₹ " + Number(result.required_monthly_investment || 0).toLocaleString("en-IN", {maximumFractionDigits: 2});

            const total = document.getElementById("goalTotal");
            if (total) total.innerText =
                "₹ " + Number(result.total_invested || 0).toLocaleString("en-IN", {maximumFractionDigits: 2});

            const growth = document.getElementById("goalGrowth");
            if (growth) growth.innerText =
                "₹ " + Number(result.expected_growth || 0).toLocaleString("en-IN", {maximumFractionDigits: 2});

        } catch (err) {
            console.error("GOAL FETCH ERROR:", err);
            alert("Something went wrong");
        }
    });
});
