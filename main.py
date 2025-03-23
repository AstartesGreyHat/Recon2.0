from flask import Flask, Response, jsonify
from strawberry.flask.views import GraphQLView
from Recon import generate_frames, processor  # Asegúrate de que Recon.py está en el PATH adecuado
from graphql_schema import schema
from base64 import b64encode

app = Flask(__name__)

@app.route('/video_feed')
def video_feed():
    """Devuelve el stream de video"""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/scan')
def scan():
    """
    Escanea la cámara durante 2 segundos y devuelve en formato JSON el texto reconocido.
    El texto se codifica en base64.
    """
    qr_text = processor.processFrameForDuration(2)
    recognized_text = b64encode(qr_text.encode()).decode() if qr_text else ""
    return jsonify({"recognized_text": recognized_text})

# Registro de la ruta GraphQL
app.add_url_rule("/graphql", view_func=GraphQLView.as_view("graphql", schema=schema))

if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=5000, debug=True)
    finally:
        processor.release()
