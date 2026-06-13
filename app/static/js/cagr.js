console.log("CAGR JS LOADED");

document.addEventListener("DOMContentLoaded", function () {
    const btn = document.getElementById("cagrBtn");
    const form = document.getElementById("cagrForm");

    if (!btn || !form) return;

    form.addEventListener("submit", function (e) {
        e.preventDefault();
    });

    btn.addEventListener("click", async function (e) {
        e.preventDefault();

        const formData = new FormData(form);
        const data = Object.fromEntries(formData);

        try {
            const res = await fetch("/tools/cagr-calculator/api", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(data)
            });

            const result = await res.json();

            if (result.error) {
                alert(result.error);
                return;
            }

            const resultBox = document.getElementById("cagrResultBox");
            const emptyBox = document.getElementById("cagrResultEmpty");
            if (resultBox) resultBox.style.display = "block";
            if (emptyBox) emptyBox.style.display = "none";

            const cagrValue = document.getElementById("cagrValue");
            if (cagrValue) {
                cagrValue.innerText =
                    Number(result.cagr || 0).toLocaleString("en-IN", {maximumFractionDigits: 4}) + "%";
            }
        } catch (err) {
            console.error("CAGR FETCH ERROR:", err);
            alert("Something went wrong");
        }
    });
});

