import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, Request, HTTPException
import evolution_api
import agent

app = FastAPI(title="Meta Ads Agent")


@app.get("/")
def health():
    return {"status": "ok", "service": "meta-ads-agent"}


@app.post("/webhook")
async def webhook(request: Request):
    """Recebe eventos da Evolution API."""
    body = await request.json()

    # Evolution API envia evento "messages.upsert"
    event = body.get("event")
    if event != "messages.upsert":
        return {"ignored": True}

    data = body.get("data", {})
    message = data.get("message", {})
    key = data.get("key", {})

    # Ignora mensagens enviadas pelo próprio bot
    if key.get("fromMe"):
        return {"ignored": True}

    sender = key.get("remoteJid", "")  # ex: 5511999999999@s.whatsapp.net

    # Extrai texto
    text = (
        message.get("conversation")
        or message.get("extendedTextMessage", {}).get("text")
        or ""
    )

    # Comando para limpar histórico
    if text.strip().lower() in ["/reset", "/limpar", "/novo"]:
        agent.clear_history(sender)
        evolution_api.send_text(sender, "Histórico limpo! Pode começar uma nova campanha.")
        return {"ok": True}

    # Extrai mídia (imagem ou vídeo)
    media_url, media_type = evolution_api.get_media_url_from_message(data)

    # Agente processa
    reply = agent.chat(sender, text, media_url=media_url, media_type=media_type)

    # Envia resposta
    evolution_api.send_text(sender, reply)

    return {"ok": True}
