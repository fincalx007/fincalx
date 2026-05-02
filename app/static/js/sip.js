console.log("SIP JS LOADED");

document.addEventListener("DOMContentLoaded", function () {
    const btn = document.getElementById("calcBtn");
    const form = document.getElementById("sipForm");

    if (!btn) {
        console.log("Button not found");
        return;
    }

    if (!form) {
        console.log("Form not found");
        return;
    }

    form.addEventListener("submit", function (e) {
        e.preventDefault();
    });

    btn.addEventListener("click", async function (e) {
        console.log("Button clicked");

        e.preventDefault();

        const formData = new FormData(form);
        const data = Object.fromEntries(formData);

        console.log("FORM DATA:", data);

        try {
            const res = await fetch("/tools/sip-calculator/api", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(data)
            });

            const result = await res.json();

            console.log("API RESPONSE:", result);

            if (result.error) {
                alert(result.error);
                return;
            }

            document.getElementById("resultBox").style.display = "block";

            const emptyBox = document.getElementById("sipResultEmpty");
            if (emptyBox) {
                emptyBox.style.display = "none";
            }

            document.getElementById("totalValue").innerText =
                "\u20b9 " + result.total_value.toLocaleString();

            document.getElementById("investedAmount").innerText =
                "\u20b9 " + result.invested_amount.toLocaleString();

            document.getElementById("returns").innerText =
                "\u20b9 " + result.estimated_returns.toLocaleString();
        } catch (err) {
            console.error("FETCH ERROR:", err);
            alert("Something went wrong");
        }
    });
});
