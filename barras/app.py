from flask import Flask, jsonify, send_from_directory
import json
import os

app = Flask(__name__)

# Archivos
INVENTARIO_FILE = "inventario.json"
IMAGENES_FOLDER = "imagenes"

# Cargar inventario desde JSON
if os.path.exists(INVENTARIO_FILE):
    with open(INVENTARIO_FILE, "r", encoding="utf-8") as f:
        inventario = json.load(f)
else:
    inventario = []

# Rutas estáticas
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/styles.css')
def css():
    return send_from_directory('.', 'styles.css')

@app.route('/imagenes/<filename>')
def imagenes(filename):
    return send_from_directory(IMAGENES_FOLDER, filename)

# Buscar producto por código de barras
@app.route('/buscar/<codigo>')
def buscar_producto(codigo):
    producto = next((p for p in inventario if p["codigo_barras"] == codigo.strip()), None)
    
    if producto:
        producto_json = producto.copy()

        # Buscar imagen asociada
        imagen_path = os.path.join(IMAGENES_FOLDER, f"{codigo}.jpg")
        if os.path.exists(imagen_path):
            producto_json["imagen"] = f"/imagenes/{codigo}.jpg"
        else:
            imagen_file = next((f for f in os.listdir(IMAGENES_FOLDER) if codigo in f), None)
            producto_json["imagen"] = f"/imagenes/{imagen_file}" if imagen_file else None

        return jsonify(producto_json)
    else:
        return jsonify({"error": "Producto no encontrado"}), 404

if __name__ == '__main__':
    app.run(debug=True)
