document.addEventListener("DOMContentLoaded", function () {
    const modalEditar = document.getElementById('modalEditarEmpleado');

    modalEditar.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        const idEmpleado = button.getAttribute('data-idEmpleado');
        const identificacion = button.getAttribute('data-identificacion');
        const nombres = button.getAttribute('data-nombres');
        const apellidos = button.getAttribute('data-apellidos');
        const cargo = button.getAttribute('data-cargo');
        const salario = button.getAttribute('data-salario');
        const estado = button.getAttribute('data-estado');
        const idSucursal = button.getAttribute('data-idSucursal');  // Obtener idSucursal

        const form = document.getElementById('formEditarEmpleado');
        form.action = `/editar_empleado/${idEmpleado}`;
        document.getElementById('editIdentificacion').value = identificacion;
        document.getElementById('editNombres').value = nombres;
        document.getElementById('editApellidos').value = apellidos;
        document.getElementById('editCargo').value = cargo;
        document.getElementById('editSalario').value = salario;
        document.getElementById('editEstado').value = estado;
        document.getElementById('editIdSucursal').value = idSucursal;  // Actualizar idSucursal
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