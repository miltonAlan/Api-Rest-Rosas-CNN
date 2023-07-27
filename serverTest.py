from flask import Flask, request, jsonify

app = Flask(__name__)

# Datos de ejemplo: una lista para almacenar elementos
data = [{"id": 1, "nombre": "Ejemplo 1"}, {"id": 2, "nombre": "Ejemplo 2"}]

# Ruta para obtener todos los elementos (GET)


@app.route('/elementos', methods=['GET'])
def obtener_elementos():
    return jsonify(data)

# Ruta para obtener un elemento por su ID (GET)


@app.route('/elementos/<int:id>', methods=['GET'])
def obtener_elemento(id):
    elemento = next((item for item in data if item["id"] == id), None)
    if elemento:
        return jsonify(elemento)
    else:
        return jsonify({"mensaje": "Elemento no encontrado"}), 404

# Ruta para agregar un nuevo elemento (POST)


@app.route('/elementos', methods=['POST'])
def agregar_elemento():
    nuevo_elemento = request.json
    nuevo_elemento["id"] = len(data) + 1
    data.append(nuevo_elemento)
    return jsonify(nuevo_elemento), 201

# Ruta para actualizar un elemento existente (PUT)


@app.route('/elementos/<int:id>', methods=['PUT'])
def actualizar_elemento(id):
    elemento = next((item for item in data if item["id"] == id), None)
    if elemento:
        elemento_actualizado = request.json
        elemento.update(elemento_actualizado)
        return jsonify(elemento)
    else:
        return jsonify({"mensaje": "Elemento no encontrado"}), 404

# Ruta para eliminar un elemento por su ID (DELETE)


@app.route('/elementos/<int:id>', methods=['DELETE'])
def eliminar_elemento(id):
    elemento = next((item for item in data if item["id"] == id), None)
    if elemento:
        data.remove(elemento)
        return jsonify({"mensaje": "Elemento eliminado correctamente"})
    else:
        return jsonify({"mensaje": "Elemento no encontrado"}), 404


if __name__ == '__main__':
    app.run(debug=True)
    flask_app.run(host="0.0.0.0", port=8000)
