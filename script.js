// Arreglo global de objetos para almacenar las solicitudes (Requerimiento U2)
let listaSolicitudes = [];

// Elementos del DOM del Formulario de Registro
const formulario = document.getElementById('form-registro-interno');
const inputNombre = document.getElementById('reg-nombre');
const selectCategoria = document.getElementById('reg-categoria');
const txtDescripcion = document.getElementById('reg-descripcion');
const alertaFormulario = document.getElementById('alerta-formulario');

// Elementos del DOM para Renderizado e Indicadores Visuales
const contenedorRegistros = document.getElementById('contenedor-registros');
const contadorRegistros = document.getElementById('contador-registros');

// Elementos del DOM para Componentes Nuevos (Semana 8: Spinner y Modal)
const btnRegistrar = document.getElementById('btn-registrar');
const spinnerRegistro = document.getElementById('spinner-registro');
const textoBtnRegistrar = document.getElementById('texto-btn-registrar');

// Inicialización segura del Modal de Bootstrap usando su API nativa
let modalDetalle = null;
const modalElemento = document.getElementById('modalDetalleSolicitud');
if (modalElemento) {
    modalDetalle = new bootstrap.Modal(modalElemento);
}

// Función ejecutada inmediatamente para mostrar el estado vacío inicial
renderizarSolicitudes();

// --- VALIDACIÓN EN TIEMPO REAL (Mientras escribes) ---

// Validar Nombre en tiempo real
inputNombre.addEventListener('input', function () {
    if (inputNombre.value.trim().length < 4) {
        inputNombre.classList.add('is-invalid');
        inputNombre.classList.remove('is-valid');
    } else {
        inputNombre.classList.add('is-valid');
        inputNombre.classList.remove('is-invalid');
    }
});

// Validar Categoría en tiempo real
selectCategoria.addEventListener('change', function () {
    if (selectCategoria.value === "") {
        selectCategoria.classList.add('is-invalid');
        selectCategoria.classList.remove('is-valid');
    } else {
        selectCategoria.classList.add('is-valid');
        selectCategoria.classList.remove('is-invalid');
    }
});

// Validar Descripción en tiempo real
txtDescripcion.addEventListener('input', function () {
    if (txtDescripcion.value.trim().length < 10) {
        txtDescripcion.classList.add('is-invalid');
        txtDescripcion.classList.remove('is-valid');
    } else {
        txtDescripcion.classList.add('is-valid');
        txtDescripcion.classList.remove('is-invalid');
    }
});


// --- EVENTO SUBMIT DEL FORMULARIO ---
formulario.addEventListener('submit', function (e) {
    e.preventDefault(); // Previene el refresco por defecto de la página

    // Variables de control de estado de validación final
    let formularioValido = true;

    // Validación final antes de guardar
    if (inputNombre.value.trim().length < 4) {
        inputNombre.classList.add('is-invalid');
        formularioValido = false;
    }
    if (selectCategoria.value === "") {
        selectCategoria.classList.add('is-invalid');
        formularioValido = false;
    }
    if (txtDescripcion.value.trim().length < 10) {
        txtDescripcion.classList.add('is-invalid');
        formularioValido = false;
    }

    // Gestión del contenedor de alertas según el resultado de la validación
    if (!formularioValido) {
        formulario.classList.add('was-validated'); 
        alertaFormulario.className = "alert alert-danger d-block fw-bold text-center";
        alertaFormulario.textContent = "❌ Error: Por favor, corrija los campos marcados en rojo antes de registrar.";
        return; // Detiene la ejecución si hay fallos
    }

    // Deshabilitar botón e iniciar animación del spinner
    if (btnRegistrar && spinnerRegistro && textoBtnRegistrar) {
        btnRegistrar.disabled = true;
        spinnerRegistro.classList.remove('d-none');
        textoBtnRegistrar.textContent = "Procesando...";
    }

    // Simular un retraso de red o proceso asíncrono de 1 segundo
    setTimeout(() => {
        const nuevaSolicitud = {
            id: 'REQ-' + Math.floor(1000 + Math.random() * 9000),
            nombre: inputNombre.value.trim(),
            categoria: selectCategoria.value,
            descripcion: txtDescripcion.value.trim(),
            fechaRegistro: new Date().toLocaleDateString('es-EC')
        };

        listaSolicitudes.push(nuevaSolicitud);
        renderizarSolicitudes();

        alertaFormulario.className = "alert alert-success d-block fw-bold text-center";
        alertaFormulario.textContent = "✅ ¡Solicitud agregada con éxito a la lista de espera!";

        formulario.reset();
        limpiarValidaciones();

        if (btnRegistrar && spinnerRegistro && textoBtnRegistrar) {
            btnRegistrar.disabled = false;
            spinnerRegistro.classList.add('d-none');
            textoBtnRegistrar.textContent = "Agregar a la Lista";
        }

    }, 1000);
});

function renderizarSolicitudes() {
    contenedorRegistros.innerHTML = '';
    contadorRegistros.textContent = `Total registros: ${listaSolicitudes.length}`;

    if (listaSolicitudes.length === 0) {
        contenedorRegistros.innerHTML = `
            <div class="col-12 text-center py-4 text-muted">
                <p class="mb-0 fs-6 italic">No hay solicitudes ingresadas en este momento.</p>
            </div>
        `;
        return;
    }

    listaSolicitudes.forEach((solicitud, index) => {
        const tarjetaHTML = `
            <div class="col-12">
                <div class="card p-3 border-start border-primary border-4 shadow-sm bg-white rounded position-relative">
                    <div class="d-flex justify-content-between align-items-start me-4">
                        <div>
                            <span class="badge bg-secondary mb-1">${solicitud.id}</span>
                            <h6 class="fw-bold m-0 text-dark">${solicitud.nombre}</h6>
                            <small class="text-primary fw-medium">${solicitud.categoria}</small>
                        </div>
                    </div>
                    
                    <div class="mt-2 d-flex gap-2 justify-content-end">
                        <button type="button" class="btn btn-sm btn-info text-white fw-bold px-2 py-1" onclick="verDetalles('${solicitud.id}')" style="font-size: 0.75rem;">
                            👁️ Ver Detalles
                        </button>
                        <button type="button" class="btn btn-sm btn-outline-danger fw-bold px-2 py-1" onclick="eliminarSolicitud(${index})" style="font-size: 0.75rem;" title="Eliminar registro">
                            ✕ Eliminar
                        </button>
                    </div>
                </div>
            </div>
        `;
        contenedorRegistros.innerHTML += tarjetaHTML;
    });
}

function verDetalles(idSolicitud) {
    const registroEncontrado = listaSolicitudes.find(item => item.id === idSolicitud);

    if (registroEncontrado && modalDetalle) {
        document.getElementById('modal-id').textContent = registroEncontrado.id;
        document.getElementById('modal-nombre').textContent = registroEncontrado.nombre;
        document.getElementById('modal-categoria').textContent = registroEncontrado.categoria;
        document.getElementById('modal-descripcion').textContent = registroEncontrado.descripcion;

        modalDetalle.show();
    } else if (registroEncontrado && !modalDetalle) {
        alert(`Detalles de la Solicitud:\nID: ${registroEncontrado.id}\nNombre: ${registroEncontrado.nombre}\nCategoría: ${registroEncontrado.categoria}\nDescripción: ${registroEncontrado.descripcion}`);
    }
}

function eliminarSolicitud(indice) {
    listaSolicitudes.splice(indice, 1);
    renderizarSolicitudes();
    alertaFormulario.className = "d-none";
}

function limpiarValidaciones() {
    formulario.classList.remove('was-validated');
    inputNombre.classList.remove('is-invalid', 'is-valid');
    selectCategoria.classList.remove('is-invalid', 'is-valid');
    txtDescripcion.classList.remove('is-invalid', 'is-valid');
}