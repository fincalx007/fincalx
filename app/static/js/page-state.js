(function () {
    if (!("scrollRestoration" in history)) {
        return;
    }

    const entries = performance.getEntriesByType
        ? performance.getEntriesByType("navigation")
        : [];
    const navigationType = entries.length ? entries[0].type : "";

    if (navigationType === "reload" && !window.location.hash) {
        history.scrollRestoration = "manual";
        window.addEventListener("load", function () {
            history.scrollRestoration = "auto";
        }, { once: true });
        return;
    }

    history.scrollRestoration = "auto";
})();
