// Esperar a que el DOM esté completamente cargado y listo
document.addEventListener('DOMContentLoaded', () => {

    // 1. Selección de elementos del DOM mediante sus IDs
    const formRegistro = document.getElementById('form-registro-interno');
    const inputNombre = document.getElementById('reg-nombre');
    const selectCategoria = document.getElementById('reg-categoria');
    const txtDescripcion = document.getElementById('reg-descripcion');
    
    const contenedorRegistros = document.getElementById('contenedor-registros');
    const contadorRegistros = document.getElementById('contador-registros');
    const alertaFormulario = document.getElementById('alerta-formulario');
    const mensajeVacio = document.getElementById('mensaje-vacio');

    // Variable global para controlar el total de registros activos
    let totalRegistros = 0;

    // 2. Función para actualizar el contador en la interfaz
    function actualizarContador() {
        contadorRegistros.textContent = `Total registros: ${totalRegistros}`;
    }

    // 3. Función para mostrar alertas de validación dinámicas con Bootstrap
    function mostrarAlerta(mensaje, tipo) {
        alertaFormulario.textContent = mensaje;
        // Aplica clases de Bootstrap dinámicamente (alert-danger o alert-success)
        alertaFormulario.className = `alert alert-${tipo} py-2 small d-block`;

        // Ocultar la alerta automáticamente después de 3.5 segundos
        setTimeout(() => {
            alertaFormulario.className = 'alert d-none';
        }, 3500);
    }

    // 4. Capturar el evento 'submit' del formulario usando addEventListener
    formRegistro.addEventListener('submit', (evento) => {
        // Evitar que la página se recargue (Requisito: preventDefault)
        evento.preventDefault();

        // Obtener los valores de los inputs y limpiar espacios en blanco
        const nombre = inputNombre.value.trim();
        const categoria = selectCategoria.value;
        const descripcion = txtDescripcion.value.trim();

        // 5. Validación básica: comprobar que los campos no estén vacíos
        if (nombre === '' || categoria === '' || descripcion === '') {
            mostrarAlerta('Error: Todos los campos del formulario son obligatorios.', 'danger');
            return; // Detiene la ejecución si hay un error
        }

        // Si pasa la validación, ocultamos el mensaje de "No hay solicitudes" si es el primer registro
        if (totalRegistros === 0 && mensajeVacio) {
            mensajeVacio.style.display = 'none';
        }

        // Mostrar mensaje dinámico de éxito al usuario
        mostrarAlerta('¡Solicitud registrada con éxito en el DOM!', 'success');

        // 6. Creación dinámica de elementos (Requisito: createElement)
        // Creamos la columna contenedora (diseño responsivo de Bootstrap)
        const colDiv = document.createElement('div');
        colDiv.className = 'col-12';

        // Creamos la tarjeta que mostrará los datos del alumno
        const cardDiv = document.createElement('div');
        cardDiv.className = 'card p-3 border-start border-danger border-3 bg-white shadow-sm d-flex flex-row justify-content-between align-items-center';

        // Estructura interna de texto para los datos
        const infoDiv = document.createElement('div');
        infoDiv.innerHTML = `
            <h6 class="mb-1 fw-bold text-dark">${nombre}</h6>
            <span class="badge bg-secondary mb-1" style="font-size: 0.75rem;">${categoria}</span>
            <p class="mb-0 text-muted small">${descripcion}</p>
        `;

        // 7. Botón para eliminar el registro (Requisito: botón y evento click)
        const btnEliminar = document.createElement('button');
        btnEliminar.className = 'btn btn-sm btn-outline-danger fw-bold px-2';
        btnEliminar.innerHTML = '✕';
        btnEliminar.title = 'Eliminar registro';

        // Evento de escucha tipo click para remover el elemento de la pantalla
        btnEliminar.addEventListener('click', () => {
            colDiv.remove(); // Remueve el elemento del árbol DOM
            totalRegistros--; // Resta uno al contador
            actualizarContador(); // Actualiza el total en pantalla

            // Si ya no quedan registros, vuelve a mostrar el mensaje de lista vacía
            if (totalRegistros === 0 && mensajeVacio) {
                mensajeVacio.style.display = 'block';
            }
        });

        // 8. Ensamblar las partes creadas utilizando appendChild (Requisito)
        cardDiv.appendChild(infoDiv);
        cardDiv.appendChild(btnEliminar);
        colDiv.appendChild(cardDiv);
        contenedorRegistros.appendChild(colDiv);

        // 9. Incrementar el contador global y actualizar la pantalla
        totalRegistros++;
        actualizarContador();

        // 10. Limpiar los campos del formulario para un nuevo ingreso
        formRegistro.reset();
    });
});