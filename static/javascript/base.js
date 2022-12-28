function validateLoginForm() {
    let form = document.getElementById("loginForm");
    let username = form.username.value;
    let password = form.password.value;

    if (username.trim().length === 0 || password.trim().length === 0) {
        alert("No introdujo usuario o contraseña");
        return false;
    }
}

function validateRegisterForm() {
    debugger;
    let form = document.getElementById("registerForm");
    let username = form.username.value;
    let password = form.password.value;
    let password2 = form.password2.value;
    let email = form.email.value;
    let name = form.first_name.value;
    let lastname = form.last_name.value;

    if (username.trim().length === 0 || password.trim().length === 0 || password2.trim().length === 0 || email.trim().length === 0 || name.trim().length === 0 || lastname.trim().length === 0) {
        alert("Debe de completar todos los campos");
        return false;
    }

    if (password !== password2) {
        alert("Las contraseñas no coinciden");
        return false;
    }


    if (name.trim()[0] !== name.trim()[0].toUpperCase()) {
        alert("El nombre debe de iniciar con mayúscula");
        return false;
    }

    if (lastname.trim()[0] !== lastname.trim()[0].toUpperCase()) {
        alert("El apellido debe de iniciar con mayúscula");
        return false;
    }

}

function topFunction() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}

async function loadAnimes() {

    let dialog = confirm("¿Desea cargar los animes? Este procesa tarda entre 1 y 5 minutos dependiendo de la conexión a internet");

    if (dialog) {

        document.getElementById("load-modal").ariaHidden = 'false';
        document.getElementById("load-modal").style.display = 'block';
        document.getElementById("load-modal").className = 'modal fade show';

        const response = await fetch('/load/',
            {
                method: 'GET',
                mode: 'cors',
                cache: 'no-cache',
                credentials: 'same-origin',

            });


        if (response.ok) {
            alert("Los animes se han cargado correctamente");
            window.location.href = '';
        } else {
            alert("Error al cargar los animes");
            window.location.href = '';
        }
    }

}

document.addEventListener("DOMContentLoaded", function () {
    window.addEventListener('scroll', function () {
        let navbar_height;
        if (window.scrollY > 50) {
            document.getElementById('navbar-top').classList.add('fixed-top');
            // add padding top to show content behind navbar
            navbar_height = document.querySelector('.navbar').offsetHeight;
            document.body.style.paddingTop = navbar_height + 'px';
        } else {
            document.getElementById('navbar-top').classList.remove('fixed-top');
            // remove padding top from body
            document.body.style.paddingTop = '0';
        }
    });
});



