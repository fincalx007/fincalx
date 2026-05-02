document.addEventListener("DOMContentLoaded", function () {
    console.log("EMI JS LOADED");

    const btn = document.getElementById("emiBtn");
    const form = document.getElementById("emiForm");

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
            const res = await fetch("/tools/emi-calculator/api", {
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

            document.getElementById("emiResultBox").style.display = "block";
            document.getElementById("emiResultEmpty").style.display = "none";
            document.getElementById("emiValue").innerText = formatMoney(result.emi);
            document.getElementById("emiTotalInterest").innerText = formatMoney(result.total_interest);
            document.getElementById("emiTotalPayment").innerText = formatMoney(result.total_payment);
        } catch (err) {
            console.error(err);
            alert("Something went wrong");
        }
    });
});

function formatMoney(value) {
    return "\u20b9 " + Number(value || 0).toLocaleString("en-IN", {
        maximumFractionDigits: 2
    });
}
