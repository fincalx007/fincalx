console.log("STEP-UP SIP JS LOADED");

document.addEventListener("DOMContentLoaded", function () {
    const btn = document.getElementById("stepUpSIPBtn");
    const form = document.getElementById("stepUpSIPForm");

    if (!btn || !form) return;

    form.addEventListener("submit", function (e) {
        e.preventDefault();
    });

    btn.addEventListener("click", async function (e) {
        e.preventDefault();

        const formData = new FormData(form);
        const data = Object.fromEntries(formData);

        try {
            const res = await fetch("/tools/step-up-sip-calculator/api", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(data)
            });

            const result = await res.json();

            if (result.error) {
                alert(result.error);
                return;
            }

            const resultBox = document.getElementById("stepUpSIPResultBox");
            const emptyBox = document.getElementById("stepUpSIPResultEmpty");
            if (resultBox) resultBox.style.display = "block";
            if (emptyBox) emptyBox.style.display = "none";

            const maturity = document.getElementById("stepUpSIPMaturity");
            if (maturity) maturity.innerText =
                "₹ " + Number(result.maturity_value || 0).toLocaleString("en-IN", {maximumFractionDigits: 2});

            const invested = document.getElementById("stepUpSIPInvested");
            if (invested) invested.innerText =
                "₹ " + Number(result.total_invested || 0).toLocaleString("en-IN", {maximumFractionDigits: 2});

            const wealth = document.getElementById("stepUpSIPWealth");
            if (wealth) wealth.innerText =
                "₹ " + Number(result.wealth_generated || 0).toLocaleString("en-IN", {maximumFractionDigits: 2});

        } catch (err) {
            console.error("STEP-UP SIP FETCH ERROR:", err);
            alert("Something went wrong");
        }
    });
});

