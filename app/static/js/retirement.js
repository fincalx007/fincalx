console.log("RETIREMENT JS LOADED");

document.addEventListener("DOMContentLoaded", function () {
    const btn = document.getElementById("retirementBtn");
    const form = document.getElementById("retirementForm");

    if (!btn || !form) return;

    form.addEventListener("submit", function (e) {
        e.preventDefault();
    });

    btn.addEventListener("click", async function (e) {
        e.preventDefault();

        const formData = new FormData(form);
        const data = Object.fromEntries(formData);

        try {
            const res = await fetch("/tools/retirement-calculator/api", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(data)
            });

            const result = await res.json();

            if (result.error) {
                alert(result.error);
                return;
            }

            const resultBox = document.getElementById("retirementResultBox");
            const emptyBox = document.getElementById("retirementResultEmpty");
            if (resultBox) resultBox.style.display = "block";
            if (emptyBox) emptyBox.style.display = "none";

            const corpus = document.getElementById("retirementCorpus");
            if (corpus) corpus.innerText =
                "₹ " + Number(result.retirement_corpus || 0).toLocaleString("en-IN", {maximumFractionDigits: 2});

            const income = document.getElementById("retirementIncome");
            if (income) income.innerText =
                "₹ " + Number(result.estimated_annual_income || 0).toLocaleString("en-IN", {maximumFractionDigits: 2});

        } catch (err) {
            console.error("RETIREMENT FETCH ERROR:", err);
            alert("Something went wrong");
        }
    });
});
