import json
import os
from typing import Optional

_DB_PATH = os.path.join(os.path.dirname(__file__), "clients.json")


def _load() -> dict:
    with open(_DB_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def is_authorized(phone: str) -> bool:
    """Verifica se o número tem permissão para usar o agente."""
    phone = _normalize(phone)
    db = _load()
    return phone in [_normalize(p) for p in db.get("gestores_autorizados", [])]


def get_client(name: str) -> Optional[dict]:
    """Busca credenciais do cliente pelo nome (case-insensitive)."""
    db = _load()
    return db.get("clientes", {}).get(name.lower().strip())


def list_clients() -> list[str]:
    """Lista nomes de clientes cadastrados."""
    db = _load()
    return [v["nome"] for v in db.get("clientes", {}).values()]


def add_client(name: str, meta_token: str, ad_account_id: str, page_id: str) -> None:
    """Adiciona ou atualiza um cliente."""
    db = _load()
    db["clientes"][name.lower().strip()] = {
        "nome": name,
        "meta_token": meta_token,
        "ad_account_id": ad_account_id,
        "page_id": page_id,
    }
    _save(db)


def add_gestor(phone: str) -> None:
    db = _load()
    phone = _normalize(phone)
    if phone not in db["gestores_autorizados"]:
        db["gestores_autorizados"].append(phone)
    _save(db)


def _save(db: dict) -> None:
    with open(_DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)


def _normalize(phone: str) -> str:
    """Remove @s.whatsapp.net e espaços."""
    return phone.replace("@s.whatsapp.net", "").replace(" ", "").strip()
