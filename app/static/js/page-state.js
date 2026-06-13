window.addEventListener("beforeunload", function () {
    try { sessionStorage.setItem("scrollPos", window.scrollY); } catch (e) { }
});

window.addEventListener("load", function () {
    try {
        const scrollPos = sessionStorage.getItem("scrollPos");
        if (scrollPos !== null) {
            window.scrollTo({ top: parseInt(scrollPos), behavior: "instant" });
            sessionStorage.removeItem("scrollPos");
        }
    } catch (e) {
        // silently fail
    }
});
