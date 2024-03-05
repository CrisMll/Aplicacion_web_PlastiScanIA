//Función para copiar el email haciendo clic en el icono del portapapeles para mayor rapidez
function copiarEmail() {
    let emailElement = document.getElementById("email-copia");
    let email = emailElement.textContent || emailElement.innerText;

    navigator.clipboard.writeText(email).then(function () {
        alert('Email copiado: ' + email);
    }, function (err) {
        alert('Error al copiar el email: ' + err);
    });
}

//Controladores del menú hamburguesa
const nav = document.querySelector("#nav");
const abrir = document.querySelector("#abrir");
const cerrar = document.querySelector("#cerrar");

abrir.addEventListener("click",() =>{
    nav.classList.add("visible");
})

cerrar.addEventListener("click", () => {
    nav.classList.remove("visible");
})
