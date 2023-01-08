function validateLoginForm() {
    let form = document.getElementById("loginForm");
    let username = form.username.value;
    let password = form.password.value;

    if (username.trim().length === 0 || password.trim().length === 0) {
        alert("Did not enter username or password.");
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
        alert("You must complete all fields.");
        return false;
    }

    if (password !== password2) {
        alert("Passwords do not match.");
        return false;
    }


    if (name.trim()[0] !== name.trim()[0].toUpperCase()) {
        alert("The name must start with a capital letter.");
        return false;
    }

    if (lastname.trim()[0] !== lastname.trim()[0].toUpperCase()) {
        alert("Last name must start with a capital letter.");
        return false;
    }

}

function topFunction() {
    document.body.scrollTop = 0;
    document.documentElement.scrollTop = 0;
}

function radioButtons(value) {
    if (value === "1") {
        document.getElementById("phrases").style.display = "block";
        document.getElementById("dates").style.display = "none";
        document.getElementById("episodes").style.display = "none";
    } else if (value === "2") {
        document.getElementById("phrases").style.display = "none";
        document.getElementById("dates").style.display = "block";
        document.getElementById("episodes").style.display = "none";
    } else if (value === "3") {
        document.getElementById("phrases").style.display = "none";
        document.getElementById("dates").style.display = "none";
        document.getElementById("episodes").style.display = "block";
    }

}

function validateFormsRadio(value) {
    if (value === "1") {
        const form = document.getElementById("phrases").getElementsByTagName("form")[0];
        let phrase = form.phrase.value;

        if (phrase.trim().length === 0) {
            alert("He did not enter a phrase");
            return false;
        }
    } else if (value === "2") {
        const form = document.getElementById("dates").getElementsByTagName("form")[0];
        let date_s = new Date(form.date_start.value);
        let date_e = new Date(form.date_end.value);

        if (date_e && date_s) {
            if (date_e < date_s) {
                alert("The end date must be greater than the start date");
                return false;
            }
        }

    }
}

function see(animeId){

}

function validateSearchForm() {
    let form = document.getElementById("search-form");
    let search = form.search.value;

    if (search.trim().length === 0) {
        alert("No introdujo nada en el campo de búsqueda");
        return false;
    }
}

async function loadAnimes() {

    let dialog = confirm("¿Do you want to load all 1000 animes? This process takes between 1 and 5 minutes depending on the internet connection");

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
            alert("The animes have been loaded successfully");
            window.location.href = '';
        } else {
            alert("Error loading anime");
            window.location.href = '';
        }
    }

}

function formSubmit(formId) {
    let thisForm = document.getElementById(formId);
    if (thisForm) {
        thisForm.submit();
    }
}

document.addEventListener("DOMContentLoaded", function () {
    window.addEventListener('scroll', function () {
        let navbar_height;
        if (window.scrollY > 50) {
            document.getElementById('navbar-top').classList.add('fixed-top');
            navbar_height = document.querySelector('.navbar').offsetHeight;
            document.body.style.paddingTop = navbar_height + 'px';
        } else {
            document.getElementById('navbar-top').classList.remove('fixed-top');
            document.body.style.paddingTop = '0';
        }
    });
});



