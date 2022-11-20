function toggleDarkmode() {
    console.log('toggle!');
    if (document.body.classList.contains('dark')) {
        document.body.classList.remove('dark');
        document.body.classList.add('light');
        localStorage.setItem("dark-mode", "disabled");
    } else {
        document.body.classList.remove('light');
        document.body.classList.add('dark');
        localStorage.setItem("dark-mode", "enabled");
    }
}