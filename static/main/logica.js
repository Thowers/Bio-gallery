document.addEventListener('DOMContentLoaded', function() {
    // Elementos del DOM
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImage');
    const modalTitle = document.getElementById('modalTitle');
    const modalDesc = document.getElementById('modalDescription');
    const modalQuestion = document.getElementById('modalQuestion');
    const closeBtn = document.querySelector('.close-modal');
    const unlockBtn = document.querySelector('.btn-unlock');
    const cancelBtn = document.querySelector('.btn-cancel');

    // Variables de estado
    let currentImageId = null;

    // Función para abrir el modal
    function openModal() {
        document.body.style.overflow = 'hidden';
        modal.style.display = 'flex';
        setTimeout(() => {
            modal.style.opacity = '1';
            document.querySelector('.modal-content-wrapper').style.transform = 'translateY(0)';
        }, 10);
    }

    // Función para cerrar el modal
    function closeModal() {
        modal.style.opacity = '0';
        document.querySelector('.modal-content-wrapper').style.transform = 'translateY(20px)';
        setTimeout(() => {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
            // Resetear los valores del modal
            modalImg.src = '';
            modalTitle.textContent = '';
            modalDesc.textContent = '';
            modalQuestion.textContent = '';
            currentImageId = null;
        }, 300);
    }

    // Evento para abrir modal al hacer clic en imágenes
    document.querySelectorAll('.open-modal').forEach(img => {
        img.addEventListener('click', function() {
            currentImageId = this.dataset.id;
            modalImg.src = this.dataset.image;
            modalImg.alt = this.alt;
            modalTitle.textContent = this.dataset.title || '';
            modalDesc.textContent = this.dataset.description || '';
            modalQuestion.textContent = this.dataset.pregunta || '';
            openModal();
        });
    });

    // Evento para el botón de cierre
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

    // Evento para desbloquear imagen
    unlockBtn.addEventListener('click', function() {
        if (currentImageId) {
            fetch(`/desbloquear_imagen/${currentImageId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.reload();
                }
            })
            .catch(error => {
                console.error('Error al desbloquear imagen:', error);
                alert('Ocurrió un error al desbloquear la imagen');
            });
        }
    });

    // Evento para cancelar
    cancelBtn.addEventListener('click', closeModal);

    // Función para obtener el token CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});