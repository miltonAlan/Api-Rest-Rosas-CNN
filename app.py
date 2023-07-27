from flask import Flask, request, jsonify, send_file
from scipy.spatial.distance import euclidean
from imutils import perspective
from imutils import contours
import numpy as np
import imutils
import cv2
import io

app = Flask(__name__)


def process_image(image):
    # Aquí va el código de la función process_image() que procesa la imagen
    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Aplicar filtro Gaussiano para reducir el ruido
    blur = cv2.GaussianBlur(gray, (9, 9), 0)

    # Detectar bordes en la imagen
    edged = cv2.Canny(blur, 50, 100)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)

    # Encontrar contornos en la imagen
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)

    # Ordenar los contornos de izquierda a derecha, donde el contorno izquierdo es el objeto de referencia
    (cnts, _) = contours.sort_contours(cnts)

    # Eliminar contornos que no son lo suficientemente grandes
    cnts = [x for x in cnts if cv2.contourArea(x) > 100]

    # Dimensiones del objeto de referencia
    # Aquí, por referencia, se utiliza un cuadrado de 2 cm x 2 cm
    ref_object = cnts[0]
    box = cv2.minAreaRect(ref_object)
    box = cv2.boxPoints(box)
    box = np.array(box, dtype="int")
    box = perspective.order_points(box)
    (tl, tr, br, bl) = box
    dist_in_pixel = euclidean(tl, tr)
    dist_in_cm = 2
    pixel_per_cm = dist_in_pixel / dist_in_cm

    # Dibujar los contornos restantes y medir los objetos
    for cnt in cnts:
        box = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(box)
        box = np.array(box, dtype="int")
        box = perspective.order_points(box)
        (tl, tr, br, bl) = box
        cv2.drawContours(image, [box.astype("int")], -1, (0, 0, 255), 2)
        mid_pt_horizontal = (
            tl[0] + int(abs(tr[0] - tl[0]) / 2), tl[1] + int(abs(tr[1] - tl[1]) / 2))
        mid_pt_verticle = (tr[0] + int(abs(tr[0] - br[0]) / 2),
                           tr[1] + int(abs(tr[1] - br[1]) / 2))
        wid = euclidean(tl, tr) / pixel_per_cm
        ht = euclidean(tr, br) / pixel_per_cm
        cv2.putText(image, "{:.1f}cm".format(wid), (int(mid_pt_horizontal[0] - 15), int(mid_pt_horizontal[1] - 10)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)
        cv2.putText(image, "{:.1f}cm".format(ht), (int(mid_pt_verticle[0] + 10), int(mid_pt_verticle[1])),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 2)

    # Devolver la imagen procesada
    return image


@app.route('/api/process-image', methods=['POST'])
def process_image_api():
    # Leer la imagen enviada en la solicitud POST
    image_file = request.files['file']
    if not image_file or not allowed_file(image_file.filename):
        return jsonify({"message": "Formato de imagen no válido"}), 400

    # Leer la imagen con OpenCV y convertirla en una imagen en formato NumPy
    image = cv2.imdecode(np.fromstring(
        image_file.read(), np.uint8), cv2.IMREAD_COLOR)

    # Procesar la imagen llamando a la función process_image()
    processed_image = process_image(image)

    # Convertir la imagen procesada en bytes para enviarla como respuesta
    image_bytes = cv2.imencode('.png', processed_image)[1].tobytes()

    # Enviar la imagen procesada como respuesta
    return send_file(io.BytesIO(image_bytes), mimetype='image/png')


def allowed_file(filename):
    # Verificar que el archivo tenga una extensión de imagen válida
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}


if __name__ == '__main__':
    app.run(debug=True)
