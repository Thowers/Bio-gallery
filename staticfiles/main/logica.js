document.addEventListener('DOMContentLoaded', function() {
    // Elementos del DOM
    const modal = document.getElementById('imageModal');
    const modalImg = document.getElementById('modalImage');
    const modalTitle = document.getElementById('modalTitle');
    const modalCommunity = document.getElementById('modalCommunity');
    const modalDesc = document.getElementById('modalDescription');
    const closeBtn = document.querySelector('.close-modal');
    const opcionBtn1 = document.getElementById('btn-opcion-1');
    const opcionBtn2 = document.getElementById('btn-opcion-2');
    const opcionBtn3 = document.getElementById('btn-opcion-3');
    const opcionBtn4 = document.getElementById('btn-opcion-4');
    const btnOpciones = [opcionBtn1, opcionBtn2, opcionBtn3, opcionBtn4];

    // Variables de estado
    let currentImageId = null;
    let isLockedImage = false;
    let timeCounter = 0;
    let waitTime = 1000; 
    let penalizando = false;

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
        document.getElementById('modalPregunta').textContent = '';
        currentImageId = null;
        isLockedImage = false;
        // Habilitar botones y resetear penalización
        btnOpciones.forEach(btn => btn.disabled = false);
        penalizando = false;
        waitTime = 1000;
        timeCounter = 0;
        const timeDisplay = document.querySelector('.time-display');
        if (timeDisplay) timeDisplay.textContent = 'Tiempo acumulado: 0 segundos';
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
            modalDesc.style.display = 'none'; // Oculta la descripción al abrir el modal

            // Mostrar y resetear los botones y el tiempo acumulado
            btnOpciones.forEach(b => {
                b.style.display = 'inline-block';
                b.disabled = false;
            });
            if (timeDisplay) {
                timeDisplay.style.display = 'block';
                timeDisplay.textContent = 'Tiempo acumulado: 0 segundos';
            }

            // Mostrar la pregunta
            const modalPregunta = document.getElementById('modalPregunta');
            modalPregunta.textContent = this.dataset.pregunta || '';
            
            // Preparar las opciones
            let opciones = [
                {texto: this.dataset.respuesta, correcta: true},
                {texto: this.dataset.opcion1, correcta: false},
                {texto: this.dataset.opcion2, correcta: false},
                {texto: this.dataset.opcion3, correcta: false}
            ];
            // Mezclar las opciones
            opciones = opciones.sort(() => Math.random() - 0.5);

            // Asignar texto y correcta a los botones
            for (let i = 0; i < 4; i++) {
                btnOpciones[i].textContent = opciones[i].texto;
                btnOpciones[i].dataset.correcta = opciones[i].correcta;
            }

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

    

    // Mostrar el tiempo acumulado en el modal
    const modalContent = document.querySelector('.modal-content');
    let timeDisplay = document.querySelector('.time-display');
    if (!timeDisplay) {
        timeDisplay = document.createElement('div');
        timeDisplay.className = 'time-display';
        timeDisplay.textContent = 'Tiempo acumulado: 0 segundos';
        modalContent.appendChild(timeDisplay);
    }

    // Lógica para manejar clics en los botones de opción
    btnOpciones.forEach(btn => {
        btn.addEventListener('click', function(e) {
            if (penalizando) return;
            if (this.dataset.correcta === "true") {
                modalDesc.style.display = 'block'; // Muestra la descripción solo si es correcta
                // Oculta los botones de opción
                btnOpciones.forEach(b => b.style.display = 'none');
                // Oculta el texto de tiempo acumulado
                if (timeDisplay) timeDisplay.style.display = 'none';
                // Desbloquear la imagen vía fetch
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
                        } else {
                            alert('No se pudo desbloquear la imagen.');
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        alert('Ocurrió un error al desbloquear la imagen');
                    });
                } else {
                    alert('¡Respuesta correcta!');
                }
            } else {
                penalizarTiempo();
            }
        });
    });

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

    // Función de penalización de tiempo
    function penalizarTiempo() {
        penalizando = true;
        timeCounter += waitTime / 1000; 
        timeDisplay.textContent = `Tiempo acumulado: ${timeCounter} segundos`;
        btnOpciones.forEach(btn => btn.disabled = true);
        setTimeout(() => {
            btnOpciones.forEach(btn => btn.disabled = false);
            penalizando = false;
        }, waitTime);
        waitTime *= 2;
    }
});

