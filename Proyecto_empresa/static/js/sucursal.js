document.addEventListener("DOMContentLoaded", function () {
    const modalEditar = document.getElementById("modalEditarSucursal");

    modalEditar.addEventListener("show.bs.modal", function (event) {
        const button = event.relatedTarget; // Botón que activó el modal
        const idSucursal = button.getAttribute("data-idSucursal");
        const nombre = button.getAttribute("data-nombre");
        const direccion = button.getAttribute("data-direccion");
        const ciudad = button.getAttribute("data-ciudad");
        const telefono = button.getAttribute("data-telefono");
        const estado = button.getAttribute("data-estado");

        // Actualizar el formulario de edición
        const form = document.getElementById("formEditarSucursal");
        form.action = `/editar_sucursal/${idSucursal}`; // Establecer la acción correcta
        document.getElementById("editNombre").value = nombre;
        document.getElementById("editDireccion").value = direccion;
        document.getElementById("editCiudad").value = ciudad;
        document.getElementById("editTelefono").value = telefono;
        document.getElementById("editEstado").value = estado;
        
    });

    
    // Cerrar alertas automáticamente después de 3 segundos
    setTimeout(() => {
        let alerts = document.querySelectorAll(".alert");
        alerts.forEach(alert => {
            let bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 3000);
});




      


