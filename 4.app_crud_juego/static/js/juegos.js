// Modal de edición de juego
const modalEditarJuego = document.getElementById('modalEditarJuego');
modalEditarJuego.addEventListener('show.bs.modal', function (event) {
    const button = event.relatedTarget; // Botón que abrió el modal
    const id = button.getAttribute('data-id');
    const nombre = button.getAttribute('data-nombre');
    const descripcion = button.getAttribute('data-descripcion');
    const precioCompra = button.getAttribute('data-preciocompra');

    // Llenar los campos del formulario de edición
    document.getElementById('editId').value = id;
    document.getElementById('editNombre').value = nombre;
    document.getElementById('editDescripcion').value = descripcion;
    document.getElementById('editPrecioCompra').value = precioCompra;
});

// Modal de detalles del juego
document.addEventListener("DOMContentLoaded", function () {
    const detalleButtons = document.querySelectorAll(".btn-detalles");

    detalleButtons.forEach(button => {
        button.addEventListener("click", function () {
            const juegoId = this.dataset.id;

            // Llamada a la API para obtener los detalles del juego
            fetch(`/juegos/${juegoId}`)
                .then(response => response.json())
                .then(data => {
                    // Actualizar el contenido del modal con los datos del juego
                    document.getElementById("detalleNombre").innerText = data.nombre;
                    document.getElementById("detalleDescripcion").innerText = data.descripcion;
                    document.getElementById("detallePrecio").innerText = `$${data.PrecioCompra}`;
                    
                    // Mostrar el modal de detalles
                    const detalleModal = new bootstrap.Modal(document.getElementById('modalDetallesJuego'));
                    detalleModal.show();
                })
                .catch(error => {
                    console.error("Error al obtener detalles:", error);
                });
        });
    });
});
