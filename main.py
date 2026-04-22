import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, Request
import evolution_api
import agent
import client_db

app = FastAPI(title="Meta Ads Agent")


@app.get("/")
def health():
    return {"status": "ok", "service": "meta-ads-agent"}


@app.post("/webhook")
async def webhook(request: Request):
    body = await request.json()

    event = body.get("event")
    if event != "messages.upsert":
        return {"ignored": True}

    data = body.get("data", {})
    message = data.get("message", {})
    key = data.get("key", {})

    if key.get("fromMe"):
        return {"ignored": True}

    sender = key.get("remoteJid", "")

    # Verifica se o número está autorizado
    if not client_db.is_authorized(sender):
        evolution_api.send_text(sender, "Você não tem permissão para usar este agente.")
        return {"unauthorized": True}

    # Extrai texto
    text = (
        message.get("conversation")
        or message.get("extendedTextMessage", {}).get("text")
        or ""
    )

    # Comandos especiais
    if text.strip().lower() in ["/reset", "/limpar", "/novo"]:
        agent.clear_history(sender)
        evolution_api.send_text(sender, "Histórico limpo! Pode começar uma nova campanha.")
        return {"ok": True}

    if text.strip().lower() == "/clientes":
        clientes = client_db.list_clients()
        msg = "Clientes cadastrados:\n" + "\n".join(f"• {c}" for c in clientes)
        evolution_api.send_text(sender, msg)
        return {"ok": True}

    # Extrai mídia
    media_url, media_type = evolution_api.get_media_url_from_message(data)

    # Agente processa
    reply = agent.chat(sender, text, media_url=media_url, media_type=media_type)

    evolution_api.send_text(sender, reply)

    return {"ok": True}
