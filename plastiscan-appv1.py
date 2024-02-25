from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import tensorflow as tf
from PIL import Image
import numpy as np

app = Flask(__name__)

# Cargar el modelo directamente
plastiscan = tf.keras.models.load_model('PlastiScan_V1.5 json - CNN.h5')

# Mapeo para la clasificación
mapeo_forma = ['Fibra', 'Fragmento', 'Lámina']
mapeo_color = ['Blanco', 'Negro', 'Azul', 'Marrón', 'Verde', 'Multicolor', 'Rojo', 'Transparente', 'Amarillo']
mapeo_componente = ['No Plástico', 'Nylon', 'PE', 'PET', 'PP', 'PS', 'Otros']
mapeo_categoria = ['Macroplástico', 'Mesoplástico', 'Microplástico']

# Carpeta para almacenar las imágenes cargadas
UPLOAD_FOLDER = 'intranet/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def cargar_y_preprocesar_imagen(imagen_path, target_size=(299, 299)):
    img = Image.open(imagen_path)
    img = img.resize(target_size)
    img_array = np.array(img)
    img_array_expanded = np.expand_dims(img_array, axis=0)
    return img_array_expanded / 255.0

def obtener_etiquetas_salida_con_probabilidad(prediccion, mapeo_forma, mapeo_color, mapeo_componente, mapeo_categoria):
    forma_idx = np.argmax(prediccion[0])
    color_idx = np.argmax(prediccion[1])
    componente_idx = np.argmax(prediccion[2])
    categoria_idx = np.argmax(prediccion[3])

    forma_probabilidad = prediccion[0][0][forma_idx]
    color_probabilidad = prediccion[1][0][color_idx]
    componente_probabilidad = prediccion[2][0][componente_idx]
    categoria_probabilidad = prediccion[3][0][categoria_idx]

    forma = {
        "nombre": mapeo_forma[forma_idx],
        "probabilidad": float(forma_probabilidad)
    }
    color = {
        "nombre": mapeo_color[color_idx],
        "probabilidad": float(color_probabilidad)
    }
    componente = {
        "nombre": mapeo_componente[componente_idx],
        "probabilidad": float(componente_probabilidad)
    }
    categoria = {
        "nombre": mapeo_categoria[categoria_idx],
        "probabilidad": float(categoria_probabilidad)
    }

    return forma, color, componente, categoria

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Verificar si la solicitud tiene la parte del archivo
        if 'file' not in request.files:
            return jsonify({'error': 'No se encontró el archivo'})

        file = request.files['file']

        # Verificar si se ha seleccionado un archivo
        if file.filename == '':
            return jsonify({'error': 'No se seleccionó ningún archivo'})

        # Verificar la extensión del archivo (puedes ajustar esto según tus necesidades)
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            return jsonify({'error': 'Extensión de archivo no permitida'})

        # Guardar el archivo en la carpeta de carga
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        # Cargar y preprocesar la imagen
        img_preprocesada = cargar_y_preprocesar_imagen(file_path)

        # Realizar la predicción
        predicciones = plastiscan.predict(img_preprocesada)

        # Obtener las etiquetas de salida con probabilidades
        forma, color, componente, categoria = obtener_etiquetas_salida_con_probabilidad(
            predicciones, mapeo_forma, mapeo_color, mapeo_componente, mapeo_categoria
        )

        # Guardar los resultados en un diccionario
        resultados_dict = {
            "forma": forma,
            "color": color,
            "componente": componente,
            "categoria": categoria
        }

        # Devolver la predicción como JSON
        return render_template('results.html', filename=file.filename, prediction=resultados_dict)

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/clear_memory')
def clear_memory():
    # Limpiar la variable global de resultados de predicción
    global resultados_prediccion
    resultados_prediccion = None
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)