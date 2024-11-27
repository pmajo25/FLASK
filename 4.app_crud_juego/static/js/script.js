let isDarkMode = true;

document.getElementById('updateTema').addEventListener('click', function() {
    if (isDarkMode) {
        document.body.style.backgroundImage = "url('../static/img/4.jpg')";
        document.querySelector('.bg-footer').style.backgroundColor = "#f5f5f5e3"; 
        document.querySelectorAll('.navbar .nav-link').forEach(function(element) {
            element.style.color = '#000000'; // Cambiar texto de navbar a negro
        });

        document.querySelectorAll('.modal-content').forEach(function(modal) {
            modal.classList.remove('bg-dark', 'text-white');  // Eliminar clases del modo oscuro
            modal.classList.add('bg-light', 'text-dark');     // Agregar clases del modo claro
        });

        document.querySelectorAll('.bg-footer h3, .bg-footer p, .bg-footer a').forEach(function(element) {
            element.style.setProperty('color', '#000000'); // Asegurarse de que los textos sean negros
        });

        this.style.backgroundColor = "transparent";
        this.style.color = "#fff";
        this.innerText = "Oscuro";

        document.querySelector('table').classList.remove('table-dark');
        document.querySelector('table').classList.add('table-white');
    } else {
        document.body.style.backgroundImage = "url('../static/img/2.jpeg')";
        document.querySelector('.bg-footer').style.backgroundColor = ""; 
        document.querySelector('.bg-footer').style.setProperty('color', '#fff'); 
        
        document.querySelectorAll('.modal-content').forEach(function(modal) {
            modal.classList.remove('bg-light', 'text-dark');  // Eliminar clases del modo claro
            modal.classList.add('bg-dark', 'text-white');     // Agregar clases del modo oscuro
        });

        document.querySelectorAll('.bg-footer h3, .bg-footer p, .bg-footer a').forEach(function(element) {
            element.style.setProperty('color', '#fff'); // Asegurarse de que los textos sean blancos en modo oscuro
        });

        this.style.backgroundColor = "transparent"; 
        this.style.color = "#fff";
        this.innerText = "Claro"; 

        document.querySelector('table').classList.remove('table-white');
        document.querySelector('table').classList.add('table-dark');
    }

    isDarkMode = !isDarkMode;
});