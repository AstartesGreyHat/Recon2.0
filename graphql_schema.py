import strawberry
from typing import Optional
from base64 import b64encode
from Recon import processor  # Asegúrate de que este import apunte al Processor modificado

@strawberry.type
class AccessResponse:
    is_authorized: bool
    message: str

@strawberry.type
class ImageResponse:
    recognized_text: Optional[str]

@strawberry.type
class Query:
    @strawberry.field
    def validate_access(self, user_id: str) -> AccessResponse:
        is_authorized = user_id == "admin"
        message = "Acceso permitido" if is_authorized else "Acceso denegado"
        return AccessResponse(is_authorized=is_authorized, message=message)
    
    @strawberry.field
    def disable_camera(self) -> str:
        processor.release()  # Libera la cámara
        return "Cámara desactivada"
    
    @strawberry.field
    def enable_camera(self) -> str:
        processor.enable_camera()  # Reactiva la cámara
        return "Cámara activada"

@strawberry.type
class Mutation:
    @strawberry.mutation
    def process_image(self) -> ImageResponse:
        """
        Escanea la cámara durante 2 segundos y procesa la imagen para detectar un QR.
        Devuelve el texto reconocido codificado en base64, o una cadena vacía si no se detecta nada.
        """
        qr_text = processor.processFrameForDuration(2)
        encoded_text = b64encode(qr_text.encode()).decode() if qr_text else ""
        return ImageResponse(recognized_text=encoded_text)

schema = strawberry.Schema(query=Query, mutation=Mutation)
