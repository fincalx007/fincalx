console.log("FIRE JS LOADED");

document.addEventListener("DOMContentLoaded", function () {
    const btn = document.getElementById("fireBtn");
    const form = document.getElementById("fireForm");

    if (!btn || !form) return;

    form.addEventListener("submit", function (e) {
        e.preventDefault();
    });

    btn.addEventListener("click", async function (e) {
        e.preventDefault();

        const formData = new FormData(form);
        const data = Object.fromEntries(formData);

        try {
            const res = await fetch("/tools/fire-calculator/api", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(data)
            });

            const result = await res.json();

            if (result.error) {
                alert(result.error);
                return;
            }

            const resultBox = document.getElementById("fireResultBox");
            const emptyBox = document.getElementById("fireResultEmpty");
            if (resultBox) resultBox.style.display = "block";
            if (emptyBox) emptyBox.style.display = "none";

            const number = document.getElementById("fireNumber");
            if (number) number.innerText =
                "₹ " + Number(result.fire_number || 0).toLocaleString("en-IN", {maximumFractionDigits: 2});

            const corpus = document.getElementById("fireCorpus");
            if (corpus) corpus.innerText =
                "₹ " + Number(result.required_retirement_corpus || 0).toLocaleString("en-IN", {maximumFractionDigits: 2});

        } catch (err) {
            console.error("FIRE FETCH ERROR:", err);
            alert("Something went wrong");
        }
    });
});
