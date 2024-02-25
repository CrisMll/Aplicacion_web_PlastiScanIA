from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
import json

app = Flask(__name__)
model = load_model('plastiScan_app.h5')

def cargar_y_preprocesar_imagen(imagen_path, target_size=(299, 299)):
    img = image.load_img(imagen_path, target_size=target_size)
    img_array = image.img_to_array(img)
    img_array_expanded = np.expand_dims(img_array, axis=0)
    return img_array_expanded / 255.0

def obtener_etiquetas_salida_con_probabilidad(prediccion, mapeo_forma, mapeo_color, mapeo_componente, mapeo_categoria):
    mapeo_forma = ['Fibra', 'Fragmento', 'Lámina']
    mapeo_color = ['Blanco', 'Negro', 'Azul', 'Marrón', 'Verde', 'Multicolor', 'Rojo', 'Transparente', 'Amarillo']
    mapeo_componente = ['No Plástico', 'Nylon', 'PE', 'PET', 'PP', 'PS', 'Otros']
    mapeo_categoria = ['Macroplástico', 'Mesoplástico', 'Microplástico']
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
def home():
    return render_template('index.html')

@app.route('/pruebalo', methods=['POST'])
def pruebalo():
    if 'file' not in request.files:
        return 'No se encontró ningún archivo'
    file = request.files['file']
    if file.filename == '':
        return 'No se seleccionó ningún archivo'
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join('intranet/uploads', filename))
        return procesar_imagen(filename)

def procesar_imagen(filename):
    image_path = os.path.join('intranet/uploads', filename)
    image = cargar_y_preprocesar_imagen(image_path)
    prediccion = model.predict(image)
    forma, color, componente, categoria = obtener_etiquetas_salida_con_probabilidad(prediccion, mapeo_forma, mapeo_color, mapeo_componente, mapeo_categoria)
    resultados_dict = {
        "forma": forma,
        "color": color,
        "componente": componente,
        "categoria": categoria
    }
    with open('resultados_prediccion.json', 'w') as json_file:
        json.dump(resultados_dict, json_file)
    return render_template('resultados.html')

@app.route('/resultados')
def resultados():
    with open('resultados_prediccion.json', 'r') as json_file:
        resultados = json.load(json_file)
    return render_template('resultados.html', resultados=resultados)

if __name__ == '__main__':
    app.run(debug=True)