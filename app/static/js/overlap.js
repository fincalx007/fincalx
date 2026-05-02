document.addEventListener("DOMContentLoaded", function () {
    console.log("OVERLAP JS LOADED");

    const btn = document.getElementById("overlapBtn");
    const form = document.getElementById("overlapForm");

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
            const res = await fetch("/tools/portfolio-overlap-checker/api", {
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

            document.getElementById("overlapResultBox").style.display = "block";
            document.getElementById("overlapResultEmpty").style.display = "none";
            document.getElementById("overlapFirstCount").innerText = result.first_count;
            document.getElementById("overlapSecondCount").innerText = result.second_count;
            document.getElementById("overlapPercentage").innerText = result.overlap_percentage + "%";

            const list = document.getElementById("overlapCommonList");
            const empty = document.getElementById("overlapNoCommon");
            list.innerHTML = "";

            if (result.common && result.common.length) {
                result.common.forEach(function (name) {
                    const item = document.createElement("li");
                    item.innerText = titleCase(name);
                    list.appendChild(item);
                });
                list.style.display = "block";
                empty.style.display = "none";
            } else {
                list.style.display = "none";
                empty.style.display = "block";
            }
        } catch (err) {
            console.error(err);
            alert("Something went wrong");
        }
    });
});

function titleCase(value) {
    return String(value || "").replace(/\w\S*/g, function (text) {
        return text.charAt(0).toUpperCase() + text.slice(1).toLowerCase();
    });
}
