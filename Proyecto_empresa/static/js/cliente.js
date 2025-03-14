
document.addEventListener("DOMContentLoaded", function () {
    // Obtener el modal de edición
    const modalEditar = document.getElementById('modalEditarCliente');

    // Cuando el modal de edición se muestra, llenar el formulario con los datos de la categoría
    modalEditar.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget; // Botón que activó el modal
        const idCliente = button.getAttribute('data-idCliente');
        const idEncargado = button.getAttribute('data-idEncargado');
        const identificacion = button.getAttribute('data-identificacion');
        const nombres = button.getAttribute('data-nombres');
        const apellidos = button.getAttribute('data-apellidos');
        const tipoCliente = button.getAttribute('data-tipoCliente');
        const email = button.getAttribute('data-email');
        const telefono = button.getAttribute('data-telefono');
        const estado = button.getAttribute('data-estado');


        // Actualizar el formulario de edición
        const form = document.getElementById('formEditarCliente');
        form.action = `/editar_cliente/${idCliente}`; // Actualizar la acción del formulario
        document.getElementById('editIdentificacion').value = identificacion;
        document.getElementById('editNombres').value = nombres;
        document.getElementById('editApellidos').value = apellidos;
        document.getElementById('editTipoCliente').value = tipoCliente;
        document.getElementById('editEmail').value = email;
        document.getElementById('editTelefono').value = telefono;
        document.getElementById('editEncargado').value = idEncargado;
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