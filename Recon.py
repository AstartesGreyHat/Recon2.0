import cv2
import numpy as np
from time import time
from base64 import b64encode
import threading

# -------------------------------
# Clase Processor: Detector QR
# -------------------------------
class Processor:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            raise Exception("No se pudo abrir la cámara")
        self.detector = cv2.QRCodeDetector()
        self.last_detection_time = 0
        self.cooldown = 2  # segundos
        self.lock = threading.Lock()  # Lock para sincronizar acceso a la cámara

    def processFrame(self):
        with self.lock:
            ret, frame = self.cap.read()
            if not ret:
                return None
            
            # Convertir a escala de grises
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            qrText, points, _ = self.detector.detectAndDecode(gray)
            current_time = time()

            if qrText and points is not None and (current_time - self.last_detection_time) >= self.cooldown:
                self.last_detection_time = current_time
                # Dibujar el contorno en el frame (opcional, para debug)
                points = np.int32(points).reshape(-1, 2)
                cv2.polylines(frame, [points], isClosed=True, color=(0, 255, 0), thickness=2)
                return qrText
            return None

    def processFrameForDuration(self, duration=2):
        """
        Escanea la cámara continuamente durante 'duration' segundos y devuelve
        el primer código QR detectado. Si no se detecta nada, devuelve None.
        """
        start_time = time()
        result = None
        while time() - start_time < duration:
            # Llama a processFrame, que ya adquiere el lock
            result = self.processFrame()
            if result:
                return result
        return result

    def release(self):
        with self.lock:
            self.cap.release()

    def enable_camera(self):
        with self.lock:
            self.cap = cv2.VideoCapture(self.camera_index)
            if not self.cap.isOpened():
                raise Exception("No se pudo abrir la cámara")

# Instanciar el detector globalmente
processor = Processor()

# -------------------------------
# Funcionalidad OPENCV (Streaming)
# -------------------------------
def generate_frames():
    # En este caso, usamos el objeto processor para leer de la cámara
    while True:
        with processor.lock:
            ret, frame = processor.cap.read()
        if not ret:
            break
        
        # Convertir frame a JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        
        # Enviar frame en formato MJPEG
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    with processor.lock:
        processor.cap.release()
