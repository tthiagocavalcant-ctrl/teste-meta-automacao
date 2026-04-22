import os
import httpx

EVOLUTION_URL = os.getenv("EVOLUTION_API_URL", "").rstrip("/")
EVOLUTION_KEY = os.getenv("EVOLUTION_API_KEY", "")
INSTANCE = os.getenv("EVOLUTION_INSTANCE", "")

HEADERS = {"apikey": EVOLUTION_KEY, "Content-Type": "application/json"}


def send_text(to: str, message: str) -> dict:
    """Envia mensagem de texto pelo WhatsApp."""
    r = httpx.post(
        f"{EVOLUTION_URL}/message/sendText/{INSTANCE}",
        headers=HEADERS,
        json={"number": to, "text": message},
        timeout=15,
    )
    r.raise_for_status()
    return r.json()


def download_media(media_url: str) -> bytes:
    """Baixa mídia recebida via Evolution API."""
    r = httpx.get(media_url, headers=HEADERS, timeout=60)
    r.raise_for_status()
    return r.content


def get_media_url_from_message(message: dict) -> tuple[str | None, str | None]:
    """
    Extrai URL e tipo de mídia de uma mensagem Evolution API.
    Retorna (url, tipo) onde tipo é 'image' ou 'video'.
    """
    msg = message.get("message", {})
    if "imageMessage" in msg:
        return msg["imageMessage"].get("url"), "image"
    if "videoMessage" in msg:
        return msg["videoMessage"].get("url"), "video"
    return None, None
