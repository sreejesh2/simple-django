function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
        return navigator.clipboard.writeText(text);
    }
    // Students open the site over http://<lan-ip>, where the Clipboard API is disabled.
    const area = document.createElement('textarea');
    area.value = text;
    area.setAttribute('readonly', '');
    area.style.position = 'fixed';
    area.style.opacity = '0';
    document.body.appendChild(area);
    area.select();
    const ok = document.execCommand('copy');
    document.body.removeChild(area);
    return ok ? Promise.resolve() : Promise.reject(new Error('copy failed'));
}

document.querySelectorAll('[data-copy]').forEach((button) => {
    button.addEventListener('click', () => {
        const code = button.closest('.code-block').querySelector('code');
        copyText(code.innerText)
            .then(() => {
                button.textContent = 'Copied';
                button.classList.add('copied');
            })
            .catch(() => {
                button.textContent = 'Select & copy';
            })
            .finally(() => {
                window.setTimeout(() => {
                    button.textContent = 'Copy';
                    button.classList.remove('copied');
                }, 1600);
            });
    });
});
