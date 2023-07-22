from flask import Flask, request, jsonify
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)


@app.route('/procesar_imagen', methods=['POST'])
def procesar_imagen():
    # Obtener la imagen desde la solicitud POST
    imagen = request.files['imagen']
    # Obtener la leyenda desde la solicitud POST (opcional)
    leyenda = request.form.get('leyenda', '')

    # Procesar la imagen aquí (por ejemplo, aplicar filtros, reconocimiento de objetos, etc.)
    # Guardar la imagen procesada
    imagen_procesada_path = "./imagen_procesada.png"
    imagen.save(imagen_procesada_path)

    # Agregar la leyenda a la imagen procesada
    if leyenda:
        imagen_procesada = Image.open(imagen_procesada_path)
        draw = ImageDraw.Draw(imagen_procesada)
        width, height = imagen_procesada.size
        # Calcula el tamaño de la fuente en base al alto de la imagen
        font_size = int(height / 2)
        font = ImageFont.truetype("arial.ttf", font_size)
        text_width, text_height = draw.textsize(leyenda, font)
        # Centra el texto en la imagen
        text_position = ((width - text_width) // 2,
                         (height - text_height) // 2)
        draw.text(text_position, leyenda, fill=(255, 255, 255), font=font)
        imagen_procesada.save(imagen_procesada_path)

    # Devolver la ruta de la imagen procesada como respuesta
    return jsonify({'imagen_procesada': imagen_procesada_path})


if __name__ == '__main__':
    app.run(debug=True)
