function toggleMenu() {
    const menu = document.getElementById("menuDropdown");
    menu.style.display = menu.style.display === "block" ? "none" : "block";
}

// Close menu if clicked outside
window.onclick = function(event) {
    if (!event.target.matches('.menu-btn')) {
        const dropdown = document.getElementById("menuDropdown");
        if (dropdown && dropdown.style.display === "block") {
            dropdown.style.display = "none";
        }
    }
}
