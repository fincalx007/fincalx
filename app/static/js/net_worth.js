console.log("NET WORTH JS LOADED");

document.addEventListener("DOMContentLoaded", function () {
    const btn = document.getElementById("netWorthBtn");
    const form = document.getElementById("netWorthForm");

    if (!btn || !form) return;

    form.addEventListener("submit", function (e) {
        e.preventDefault();
    });

    btn.addEventListener("click", async function (e) {
        e.preventDefault();

        const formData = new FormData(form);
        const data = Object.fromEntries(formData);

        try {
            const res = await fetch("/tools/net-worth-calculator/api", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(data)
            });

            const result = await res.json();

            if (result.error) {
                alert(result.error);
                return;
            }

            const box = document.getElementById("netWorthResultBox");
            const empty = document.getElementById("netWorthResultEmpty");
            if (box) box.style.display = "block";
            if (empty) empty.style.display = "none";

            const val = document.getElementById("netWorthValue");
            if (val) val.innerText = "₹" + Number(result.net_worth || 0).toLocaleString("en-IN");
        } catch (err) {
            console.error("NET WORTH FETCH ERROR:", err);
            alert("Something went wrong");
        }
    });
});

