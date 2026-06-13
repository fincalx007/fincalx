console.log("SWP JS LOADED");

document.addEventListener("DOMContentLoaded", function () {
    const btn = document.getElementById("swpBtn");
    const form = document.getElementById("swpForm");

    if (!btn || !form) return;

    form.addEventListener("submit", function (e) {
        e.preventDefault();
    });

    btn.addEventListener("click", async function (e) {
        e.preventDefault();

        const formData = new FormData(form);
        const data = Object.fromEntries(formData);

        try {
            const res = await fetch("/tools/swp-calculator/api", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(data)
            });

            const result = await res.json();

            if (result.error) {
                alert(result.error);
                return;
            }

            const resultBox = document.getElementById("swpResultBox");
            const emptyBox = document.getElementById("swpResultEmpty");
            if (resultBox) resultBox.style.display = "block";
            if (emptyBox) emptyBox.style.display = "none";

            const remaining = document.getElementById("swpRemaining");
            if (remaining) remaining.innerText =
                "₹ " + Number(result.remaining_corpus || 0).toLocaleString("en-IN", {maximumFractionDigits: 2});

            const withdrawals = document.getElementById("swpWithdrawals");
            if (withdrawals) withdrawals.innerText =
                "₹ " + Number(result.total_withdrawals || 0).toLocaleString("en-IN", {maximumFractionDigits: 2});

            const growth = document.getElementById("swpGrowth");
            if (growth) growth.innerText =
                "₹ " + Number(result.corpus_growth || 0).toLocaleString("en-IN", {maximumFractionDigits: 2});

        } catch (err) {
            console.error("SWP FETCH ERROR:", err);
            alert("Something went wrong");
        }
    });
});
