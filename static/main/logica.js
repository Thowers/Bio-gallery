document.addEventListener('DOMContentLoaded', function() {
    // Elementos del DOM
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImage');
    const modalTitle = document.getElementById('modalTitle');
    const modalCommunity = document.getElementById('modalCommunity');
    const modalDesc = document.getElementById('modalDescription');
    const closeBtn = document.querySelector('.close-modal');
    const unlockBtn = document.querySelector('.btn-unlock');
    const cancelBtn = document.querySelector('.btn-cancel');

    // Variables de estado
    let currentImageId = null;
    let isLockedImage = false;

    // Función para abrir el modal
    function openModal() {
        document.body.style.overflow = 'hidden';
        modal.style.display = 'flex';
        setTimeout(() => {
            modal.style.opacity = '1';
        }, 10);
    }

    // Función para cerrar el modal
    function closeModal() {
        modal.style.opacity = '0';
        setTimeout(() => {
            modal.style.display = 'none';
            document.body.style.overflow = 'auto';
            resetModal();
        }, 300);
    }

    // Función para resetear el modal
    function resetModal() {
        modalImg.src = '';
        modalTitle.textContent = '';
        modalCommunity.textContent = '';
        modalDesc.textContent = '';
        currentImageId = null;
        isLockedImage = false;
    }

    // Evento para abrir modal
    document.querySelectorAll('.open-modal').forEach(btn => {
        btn.addEventListener('click', function() {
            currentImageId = this.dataset.id;
            isLockedImage = this.dataset.locked === 'true';
            
            modalImg.src = this.dataset.image;
            modalTitle.textContent = this.dataset.title;
            modalCommunity.textContent = this.dataset.community || 'Naturaleza Colombiana';
            modalDesc.textContent = this.dataset.description || '';
            
            // Mostrar botón de desbloquear solo si está bloqueada
            unlockBtn.style.display = isLockedImage ? 'block' : 'none';
            
            openModal();
        });
    });

    // Evento para cerrar modal
    closeBtn.addEventListener('click', closeModal);

    // Cerrar al hacer clic fuera
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeModal();
        }
    });

    // Cerrar con ESC
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.style.display === 'flex') {
            closeModal();
        }
    });

    // Evento para desbloquear imagen
    unlockBtn.addEventListener('click', function() {
        if (currentImageId && isLockedImage) {
            fetch(`/bio/desbloquear-imagen/${currentImageId}/`, {                
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
                console.error('Error:', error);
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