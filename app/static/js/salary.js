document.addEventListener("DOMContentLoaded", function () {
    console.log("SALARY JS LOADED");

    const btn = document.getElementById("salaryBtn");
    const form = document.getElementById("salaryForm");

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
            const res = await fetch("/tools/salary-calculator/api", {
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

            document.getElementById("salaryResultBox").style.display = "block";
            document.getElementById("salaryResultEmpty").style.display = "none";
            document.getElementById("salaryMonthly").innerText = formatMoney(result.monthly);
            document.getElementById("salaryInHand").innerText = formatMoney(result.in_hand);
            document.getElementById("salaryTotalDeductions").innerText = formatMoney(result.total_deductions);
            document.getElementById("salaryPf").innerText = formatMoney(result.pf);
            document.getElementById("salaryTax").innerText = formatMoney(result.tax);
            document.getElementById("salaryBasic").innerText = formatMoney(result.basic);
            document.getElementById("salaryHra").innerText = formatMoney(result.hra);
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
