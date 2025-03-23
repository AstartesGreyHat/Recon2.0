
---

# **ReconQL**  
## **Servicio de Reconocimiento y Streaming con OpenCV y GraphQL**  

Este proyecto implementa un microservicio en Python que:  
- Captura video en tiempo real desde una cámara usando OpenCV.  
- Provee un stream en vivo en formato **MJPEG** a través del endpoint `/video_feed`.  
- Permite realizar un **escaneo configurable** (por defecto 2 segundos) para detectar códigos QR, retornando el texto reconocido (codificado en base64) mediante el endpoint `/scan`.  
- Expone un endpoint **GraphQL** (`/graphql`) para realizar consultas y mutaciones, como validar acceso, habilitar/deshabilitar la cámara o procesar imágenes.  

---

## **Características**  

✔ **Streaming de Video en Tiempo Real:**  
El servicio captura continuamente video y lo transmite en formato MJPEG a través del endpoint `/video_feed`.  

✔ **Escaneo de QR:**  
Mediante el endpoint `/scan`, se escanea la cámara en busca de códigos QR. Si se detecta uno, el texto reconocido se devuelve en formato **JSON** (codificado en base64).  

✔ **GraphQL:**  
Se expone un endpoint `/graphql` para manejar consultas y mutaciones. Ejemplos:  
- Habilitar o deshabilitar la cámara.  
- Procesar imágenes y obtener datos de códigos QR.  

✔ **Sincronización de Acceso a la Cámara:**  
Se utiliza un **lock** para evitar conflictos entre el streaming y el escaneo QR.  

---

## **Instalación y Configuración**  

> 📌 **Nota:** Este servicio está diseñado para **futuro despliegue en Docker**.  

### **1️⃣ Clona el repositorio**  
```bash
git clone https://github.com/AstartesGreyHat/Recon2.0.git
cd Recon2.0
```

### **2️⃣ Instala las dependencias necesarias**  
```bash
pip install -r requirements.txt
```

### **3️⃣ (Opcional) Configura `server.conf`**  
Puedes personalizar el **host**, **puerto** y **workers** en el archivo `server.conf`.  

### **4️⃣ Ejecuta el servicio**  
```bash
python main.py
```

---

## **Uso y Endpoints**  

### 📡 **1. Streaming de Video en Vivo**  
- **URL:** `http://localhost:5000/video_feed`  
- **Método:** `GET`  
- **Descripción:** Devuelve el video en vivo en formato **MJPEG**.  
- **Ejemplo de uso en HTML:**  
  ```html
  <img src="http://localhost:5000/video_feed">
  ```

### 🔍 **2. Escaneo QR**  
- **URL:** `http://localhost:5000/scan`  
- **Método:** `GET`  
- **Descripción:** Escanea la cámara y devuelve el texto reconocido en formato **JSON** (base64).  
- **Ejemplo de respuesta:**  
  ```json
  {
    "recognized_text": "U29tZV9UUklN"
  }
  ```

### 🔗 **3. Endpoint GraphQL**  
- **URL:** `http://localhost:5000/graphql`  
- **Método:** `POST` (y `GET` si se configura)  
- **Descripción:** Permite realizar consultas y mutaciones GraphQL.  

📌 **Ejemplo de consulta para validar acceso:**  
```graphql
query {
  validate_access(user_id: "admin") {
    is_authorized
    message
  }
}
```

📌 **Ejemplo de mutación para procesar imagen (escaneo QR):**  
```graphql
mutation {
  process_image {
    recognized_text
  }
}
```

---

## **Notas Adicionales**  

✔ **Sincronización de la Cámara:**  
Se utiliza un **lock** en la clase `Processor` para evitar que el streaming y el escaneo se ejecuten al mismo tiempo.  

✔ **Reinicio de la Cámara:**  
Los endpoints GraphQL `disable_camera` y `enable_camera` permiten controlar el estado de la cámara.  

✔ **Despliegue en Producción:**  
Se recomienda contenerizar el servicio con **Docker** y usar un **proxy inverso** (como Nginx) para exponer los endpoints de manera segura.  

---

## **Licencia**  

Este proyecto se distribuye bajo la [Licencia MIT](LICENSE).  

---
