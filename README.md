---
# ReconQL
# Servicio de Reconocimiento/Streaming con OpenCV y GraphQL

Este proyecto implementa un microservicio en Python que:
- Captura video en tiempo real desde una cámara usando OpenCV.
- Provee un stream en vivo en formato MJPEG a través del endpoint `/video_feed`.
- Permite realizar un escaneo prolongado de 2 segundos (Por Defecto pero se puede ajustar) para detectar códigos QR , retornando el texto reconocido (codificado en base64) mediante el endpoint `/scan`.
- Expone un endpoint GraphQL (`/graphql`) para realizar consultas y mutaciones (por ejemplo, validar acceso, habilitar/deshabilitar la cámara, o procesar una imagen).
---




## Características

- **Streaming de Video en Tiempo Real:**  
  El servicio captura continuamente video y lo transmite en formato MJPEG a través de `/video_feed`.

- **Escaneo de QR:**  
  Mediante el endpoint `/scan`, se escanea la cámara para detectar códigos QR. Si se encuentra un QR, se devuelve el texto reconocido (codificado en base64) en formato JSON.

- **GraphQL:**  
  Se expone un endpoint `/graphql` para manejar consultas y mutaciones. Por ejemplo:
  - Habilitar o deshabilitar la cámara.
  - Procesar imagen (escaneo QR).

- **Sincronización de Acceso a la Cámara:**  
  Se utiliza un lock para compartir de forma segura la cámara entre el streaming en tiempo real y el proceso de escaneo.

---


## Instalación (futuro despliegue en docker)

1. **Clona el repositorio** (o descarga el código fuente):
   ```bash
   git clone https://github.com/AstartesGreyHat/Recon2.0.git
   cd Recon2.0
   ```

2. **Instala las dependencias necesarias:**
   ```bash
   pip install -r requirements.txt
   ```
3. **(Opcional) Configura server.conf**

4. **Ejecuta:**
   ```python
   python main.py
   ```

---


---

## Uso y Endpoints

### 1. Streaming de Video en Vivo

- **URL:** `http://localhost:5000/video_feed`
- **Método:** GET
- **Descripción:** Devuelve el video en vivo en formato MJPEG. Útil para mostrar el stream en una vista HTML (por ejemplo, usando un `<img src="http://localhost:5000/video_feed">`).

### 2. Escaneo QR

- **URL:** `http://localhost:5000/scan`
- **Método:** GET
- **Descripción:** Escanea la cámara durante 2 segundos y devuelve el texto reconocido en formato JSON, codificado en base64.
- **Ejemplo de respuesta:**
  ```json
  {
    "recognized_text": "U29tZV9UUklN"
  }
  ```

### 3. Endpoint GraphQL

- **URL:** `http://localhost:5000/graphql`
- **Método:** POST (y GET, si se configura)
- **Descripción:** Permite realizar consultas y mutaciones GraphQL.
  
  **Ejemplo de consulta para validar acceso:**
  ```graphql
  query {
    validate_access(user_id: "admin") {
      is_authorized
      message
    }
  }
  ```
  
  **Ejemplo de mutación para procesar imagen (escaneo QR):**
  ```graphql
  mutation {
    process_image {
      recognized_text
    }
  }
  ```

---



## Notas Adicionales

- **Sincronización de la Cámara:**  
  Se utiliza un lock en la clase `Processor` para evitar conflictos al usar la misma cámara para el streaming y el escaneo QR.

- **Reinicio de la Cámara:**  
  Los endpoints GraphQL para `disable_camera` y `enable_camera` permiten gestionar el estado de la cámara desde el esquema GraphQL.

- **Despliegue en Producción:**  
  Se recomienda contenerizar el servicio (por ejemplo, usando Docker) y configurar un proxy inverso (como Nginx) para exponer los endpoints a través de un dominio.

---

## Licencia

Este proyecto se distribuye bajo la [Licencia MIT](LICENSE).

---

