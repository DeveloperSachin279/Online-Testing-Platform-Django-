
document.addEventListener('DOMContentLoaded', () => {
    // Mobile menu toggle
    const toggleBtn = document.getElementById('menu-toggle');
    const sidebar = document.getElementById('sidebar');
    if (toggleBtn && sidebar) {
        toggleBtn.addEventListener('click', () => {
            sidebar.classList.toggle('open');
        });
    }

    // Dismiss alerts
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        alert.addEventListener('click', () => {
            alert.style.display = 'none';
        });
    });
});
