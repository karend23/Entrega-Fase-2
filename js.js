document.querySelectorAll('.learn-more').forEach(button => {
    button.addEventListener('click', () => {
        const info = button.getAttribute('data-info');
        alert(info);
    });
});