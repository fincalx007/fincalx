console.log("INFLATION JS LOADED");

document.addEventListener("DOMContentLoaded", function () {
    const btn = document.getElementById("inflationBtn");
    const form = document.getElementById("inflationForm");

    if (!btn || !form) return;

    form.addEventListener("submit", function (e) {
        e.preventDefault();
    });

    btn.addEventListener("click", async function (e) {
        e.preventDefault();

        const formData = new FormData(form);
        const data = Object.fromEntries(formData);

        try {
            const res = await fetch("/tools/inflation-calculator/api", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(data)
            });

            const result = await res.json();

            if (result.error) {
                alert(result.error);
                return;
            }

            const box = document.getElementById("inflationResultBox");
            const empty = document.getElementById("inflationResultEmpty");
            if (box) box.style.display = "block";
            if (empty) empty.style.display = "none";

            const fv = document.getElementById("inflationFutureValue");
            const impact = document.getElementById("inflationImpact");

            if (fv) fv.innerText = "₹" + Number(result.future_value || 0).toLocaleString("en-IN");
            if (impact) impact.innerText = "₹" + Number(result.purchasing_power_impact || 0).toLocaleString("en-IN");
        } catch (err) {
            console.error("INFLATION FETCH ERROR:", err);
            alert("Something went wrong");
        }
    });
});

