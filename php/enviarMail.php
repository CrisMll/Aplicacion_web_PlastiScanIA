<?php

if ($_POST['nombre'] == "" || $_POST['email'] == "" || $_POST['asunto'] == "" || $_POST['mensaje'] == "") {
    echo "Revisa los campos, faltan datos";
    die();
}

// Recibimos los datos del formulario en variables
$nombre = $_POST['nombre'];
$destinatario = "hola@plastiscan.org";
$asunto = $_POST['asunto'];
$mensaje_mail = $_POST['mensaje'];

$headers = "MIME-VERSION: 1.0\r\n";
$headers .= "Content-type: text/html; charset=UTF-8\r\n";
$headers .= "From: Prueba Email <hola@plastiscan.org>\r\n";

//Enviamos correo
mail($destinatario, $asunto, $mensaje_mail, $headers);

echo '<div style="display: flex; justify-content: center; align-items: center; height: 100vh; font-size:40px ;color: green;">';
echo 'Mensaje enviado correctamente';
echo '</div>';

header("Refresh: 3; URL=../index.html#contacto");
exit;


