document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImage');
    const modalQuestion = document.getElementById('modalQuestion'); // Nuevo elemento
    const modalDescription = document.getElementById('modalDescription');
    const closeBtn = document.querySelector('.close-modal');

    document.querySelectorAll('.open-modal').forEach(img => {
        img.addEventListener('click', function() {
            const imageSrc = this.dataset.image;
            const description = this.dataset.description;
            const pregunta = this.dataset.pregunta;
            modalImg.src = imageSrc;
            modalQuestion.textContent = pregunta; // Mostrar pregunta
            modalDescription.textContent = description;
            modal.style.display = 'flex';
        });
    });
    // Función para cerrar el modal
    function closeModal() {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }

    // Cerrar modal con el botón de cierre
    closeBtn.addEventListener('click', closeModal);

    // Cerrar modal al hacer clic fuera del contenido
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeModal();
        }
    });

    // Cerrar modal con la tecla ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.style.display === 'flex') {
            closeModal();
        }
    });
});