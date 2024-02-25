//Función para copiar el email haciendo clic en el icono del portapapeles para mayor rapidez
function copiarEmail() {
    var email = document.getElementById("email-copia");
    navigator.clipboard.writeText(email.value).then(function() {
        alert('Email copiado: ' + email.value);
    }, function(err) {
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

document.getElementById('predecir').addEventListener('click', function() {
    document.getElementById('resultados_prediccion').classList.remove('oculto');
});

document.getElementById('borrar').addEventListener('click', function() {
    document.getElementById('resultados_prediccion').classList.add('oculto');
});