(function () {
    let savedTheme = null;
    try {
        savedTheme = localStorage.getItem("theme");
    } catch (error) {
        savedTheme = null;
    }
    const prefersDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
    if (savedTheme === "dark" || (!savedTheme && prefersDark)) {
        document.documentElement.dataset.theme = "dark";
    }
})();
