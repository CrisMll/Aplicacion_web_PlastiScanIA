<?php

//Recibimos los datos de la imagen por el formulario. En este caso nombre, tipo y tamaño
$nombre_imagen = $_FILES['archivo']['name'];
$tipo_imagen = $_FILES['archivo']['type'];
$size_imagen = $_FILES['archivo']['size'];

//comprobamos antes de subir los archivos al servidor que son imagenes y que no tienen un tamaño mayor a 5MB
if($size_imagen <= 5000000){
    if($tipo_imagen == "image/jpeg" || $tipo_imagen == "image/jpg" || $tipo_imagen == "image/png" || $tipo_imagen == "image/gif" || $tipo_imagen == "image/svg"){
    
    //Ruta de carpeta destino en el server
    $carpeta_destino = $_SERVER['DOCUMENT_ROOT'].'/intranet/uploads/';

    //Guarda la imagen en la carpeta destino desde el directorio temporal
    move_uploaded_file($_FILES['archivo']['tmp_name'],$carpeta_destino.$nombre_imagen);
    echo '<div style="display: flex; justify-content: center; align-items: center; height: 100vh; font-size:20px ;color: green;">';
    echo 'Imagen subida correctamente';
    echo '</div>';

    //refresca la página
    header("Refresh: 3; URL=../index.html#pruebalo");
    exit;
    }
}else{
    echo 'El tamaño de la imagen no debe ser mayor a 5MB';
}




?>