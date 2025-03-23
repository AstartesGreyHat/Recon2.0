import os
import configparser  # Para leer el archivo .conf
from flask import Flask, Response, jsonify
from strawberry.flask.views import GraphQLView
from Recon import generate_frames, processor
from graphql_schema import schema
from base64 import b64encode
from waitress import serve  # Servidor WSGI para Windows

# -----------------------------
# Cargar Configuración desde server.conf
# -----------------------------
config = configparser.ConfigParser()
config.read("server.conf")

# Ahora obtenemos los valores desde la sección [SERVER]
HOST = config.get("SERVER", "HOST", fallback="0.0.0.0")
PORT = config.getint("SERVER", "PORT", fallback=5000)
WORKERS = config.getint("SERVER", "WORKERS", fallback=4)

# -----------------------------
# Configurar Flask
# -----------------------------
app = Flask(__name__)

@app.route('/video_feed')
def video_feed():
    """Devuelve el stream de video"""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/scan')
def scan():
    """Escanea la cámara durante 2 segundos y devuelve el texto del QR en base64."""
    qr_text = processor.processFrameForDuration(2)
    recognized_text = b64encode(qr_text.encode()).decode() if qr_text else ""
    return jsonify({"recognized_text": recognized_text})

# Registro de la ruta GraphQL
app.add_url_rule("/graphql", view_func=GraphQLView.as_view("graphql", schema=schema))

# -----------------------------
# Configuración WSGI
# -----------------------------
if __name__ != "__main__":
    app_wsgi = app  # Nombre de la app para Gunicorn

# -----------------------------
# Ejecutar Servidor
# -----------------------------
if __name__ == "__main__":
    try:
        print(f"🚀 Iniciando servidor en {HOST}:{PORT} con {WORKERS} workers...")

        if os.name == "nt":  # Windows → Usar Waitress
            serve(app, host=HOST, port=PORT)
        else:  # Linux → Instrucciones en el .conf para usar Gunicorn
            print("🛑 Para Linux, usa el siguiente comando en la terminal:")
            print(f"    gunicorn -w {WORKERS} -b {HOST}:{PORT} wsgi:app_wsgi")
            print("📄 Verifica que has descomentado la sección correcta en server.conf")
    finally:
        processor.release()
