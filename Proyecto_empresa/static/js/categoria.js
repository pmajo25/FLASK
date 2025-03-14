
document.addEventListener("DOMContentLoaded", function () {
    // Obtener el modal de edición
    const modalEditar = document.getElementById('modalEditarCategoria');

    // Cuando el modal de edición se muestra, llenar el formulario con los datos de la categoría
    modalEditar.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget; // Botón que activó el modal
        const id = button.getAttribute('data-id');
        const nombre = button.getAttribute('data-nombre');
        const descripcion = button.getAttribute('data-descripcion');
        const estado = button.getAttribute('data-estado');

        // Actualizar el formulario de edición
        const form = document.getElementById('formEditarCategoria');
        form.action = `/editar_categoria/${id}`; // Actualizar la acción del formulario
        document.getElementById('editNombre').value = nombre;
        document.getElementById('editDescripcion').value = descripcion;
        document.getElementById('editEstado').value = estado;
    });
});

// Cerrar automáticamente las alertas después de 3 segundos
setTimeout(() => {
    let alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        let bsAlert = new bootstrap.Alert(alert);
        bsAlert.close();
    });
}, 3000);