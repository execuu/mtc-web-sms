const modals = document.querySelectorAll('.zoomable-image');

modals.forEach((modal) => {
    modal.addEventListener('click', () => {
        const targetModalId = modal.getAttribute('data-bs-target');
        const targetModal = document.querySelector(targetModalId);

        const imageSrc = modal.getAttribute('src');
        const imageInModal = targetModal.querySelector('.modal-body img');
        imageInModal.src = imageSrc;
    });
});
