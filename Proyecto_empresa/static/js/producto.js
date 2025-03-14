
document.addEventListener("DOMContentLoaded", function () {
    // Obtener el modal de edición
    const modalEditar = document.getElementById('modalEditarProducto');

    // Cuando el modal de edición se muestra, llenar el formulario con los datos de la producto
    modalEditar.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget; // Botón que activó el modal
        const idProducto = button.getAttribute('data-idProducto');
        const idCategoria = button.getAttribute('data-idCategoria');
        const producto = button.getAttribute('data-producto');
        const descripcion = button.getAttribute('data-descripcion');
        const referencia = button.getAttribute('data-referencia');
        const precio = button.getAttribute('data-precio');
        const stock = button.getAttribute('data-stock');
        const estado = button.getAttribute('data-estado');
        console.log("Datos recibidos:", { idProducto, idCategoria, producto, descripcion, referencia, precio, stock });

        // Actualizar el formulario de edición
        const form = document.getElementById('formEditarProducto');
        form.action = `/editar_producto/${idProducto}`; // Actualizar la acción del formulario
        document.getElementById('editIdCategoria').value = idCategoria;
        document.getElementById('editProducto').value = producto;
        document.getElementById('editDescripcion').value = descripcion;
        document.getElementById('editReferencia').value = referencia;
        document.getElementById('editPrecio').value = precio;
        document.getElementById('editStock').value = stock;
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