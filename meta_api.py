import os
import json
import httpx
from typing import Optional

BASE_URL = "https://graph.facebook.com/v21.0"
TOKEN = os.getenv("META_ACCESS_TOKEN")
AD_ACCOUNT = os.getenv("META_AD_ACCOUNT_ID")  # ex: act_123456789


def _get(path: str, params: dict = {}) -> dict:
    params["access_token"] = TOKEN
    r = httpx.get(f"{BASE_URL}/{path}", params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def _post(path: str, data: dict = {}, files=None) -> dict:
    if files:
        data["access_token"] = TOKEN
        r = httpx.post(f"{BASE_URL}/{path}", data=data, files=files, timeout=120)
    else:
        data["access_token"] = TOKEN
        r = httpx.post(f"{BASE_URL}/{path}", data=data, timeout=30)
    r.raise_for_status()
    return r.json()


# ─── CAMPANHA ────────────────────────────────────────────────────────────────

def create_campaign(name: str, daily_budget_cents: int) -> dict:
    """
    Cria campanha de Leads com CBO (orçamento no nível da campanha).
    Objetivo fixo: OUTCOME_LEADS. Compra: Leilão.
    """
    return _post(f"{AD_ACCOUNT}/campaigns", {
        "name": name,
        "objective": "OUTCOME_LEADS",
        "status": "PAUSED",
        "special_ad_categories": "[]",
        "daily_budget": daily_budget_cents,
        "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
    })


# ─── CONJUNTO DE ANÚNCIOS ─────────────────────────────────────────────────────

def _build_placement(age_max: int) -> dict:
    """
    Regra de posicionamento:
    - Faixa etária com máximo >= 55 → IG + FB
    - Faixa etária com máximo < 55  → Apenas IG
    """
    if age_max >= 55:
        return {
            "publisher_platforms": ["facebook", "instagram"],
            "facebook_positions": ["feed", "story", "reels"],
            "instagram_positions": ["stream", "story", "reels", "explore"],
        }
    else:
        return {
            "publisher_platforms": ["instagram"],
            "instagram_positions": ["stream", "story", "reels", "explore"],
        }


def create_ad_set(
    campaign_id: str,
    name: str,
    age_min: int,
    age_max: int,
    countries: list[str],
    cities: Optional[list[dict]] = None,
    interests: Optional[list[dict]] = None,
    excluded_custom_audiences: Optional[list[dict]] = None,
    flexible_spec: Optional[list[dict]] = None,
) -> dict:
    """
    Cria conjunto de anúncios para campanha de Leads imobiliária.
    - Conversão: Formulários Instantâneos (ON_AD)
    - Meta de desempenho: Maximizar leads (LEAD_GENERATION)
    - Cobrança: Impressões
    - Limite mínimo de gasto: R$10 (1000 centavos)
    - Posicionamento: automático baseado na idade
    - Gênero: todos (omitido = todos)
    """
    targeting: dict = {
        "age_min": age_min,
        "age_max": age_max,
        "geo_locations": {"countries": countries},
        **_build_placement(age_max),
    }

    if cities:
        targeting["geo_locations"]["cities"] = cities

    if interests:
        targeting["flexible_spec"] = [{"interests": interests}]

    if flexible_spec:
        targeting["flexible_spec"] = flexible_spec

    if excluded_custom_audiences:
        targeting["excluded_custom_audiences"] = excluded_custom_audiences

    return _post(f"{AD_ACCOUNT}/adsets", {
        "name": name,
        "campaign_id": campaign_id,
        "optimization_goal": "LEAD_GENERATION",
        "billing_event": "IMPRESSIONS",
        "destination_type": "ON_AD",
        "daily_min_spend_target": 1000,  # R$10 mínimo
        "targeting": json.dumps(targeting),
        "status": "PAUSED",
    })


# ─── MÍDIA ───────────────────────────────────────────────────────────────────

def upload_image_from_url(image_url: str) -> dict:
    img_bytes = httpx.get(image_url, timeout=60).content
    return _post(
        f"{AD_ACCOUNT}/adimages",
        files={"filename": ("image.jpg", img_bytes, "image/jpeg")},
    )


def upload_image_from_bytes(image_bytes: bytes, filename: str = "image.jpg") -> dict:
    return _post(
        f"{AD_ACCOUNT}/adimages",
        files={"filename": (filename, image_bytes, "image/jpeg")},
    )


def upload_video_from_url(video_url: str, title: str = "Video") -> dict:
    vid_bytes = httpx.get(video_url, timeout=180).content
    return _post(
        f"{AD_ACCOUNT}/advideos",
        data={"title": title},
        files={"source": ("video.mp4", vid_bytes, "video/mp4")},
    )


def upload_video_from_bytes(video_bytes: bytes, title: str = "Video") -> dict:
    return _post(
        f"{AD_ACCOUNT}/advideos",
        data={"title": title},
        files={"source": ("video.mp4", video_bytes, "video/mp4")},
    )


# ─── CRIATIVO ────────────────────────────────────────────────────────────────

def create_ad_creative(
    name: str,
    page_id: str,
    primary_text: str,
    headline: str,
    lead_gen_form_id: str,
    image_hash: Optional[str] = None,
    video_id: Optional[str] = None,
    description: Optional[str] = None,
) -> dict:
    """
    Cria criativo para anúncio de Lead com Formulário Instantâneo.
    CTA fixo: LEARN_MORE ("Saiba Mais").
    Advantage+ creative enhancements: desligados.
    """
    call_to_action = {
        "type": "LEARN_MORE",
        "value": {"lead_gen_form_id": lead_gen_form_id},
    }

    if video_id:
        object_story_spec = {
            "page_id": page_id,
            "video_data": {
                "video_id": video_id,
                "message": primary_text,
                "title": headline,
                "call_to_action": call_to_action,
            },
        }
    else:
        link_data: dict = {
            "message": primary_text,
            "name": headline,
            "call_to_action": call_to_action,
            "image_hash": image_hash,
        }
        if description:
            link_data["description"] = description

        object_story_spec = {
            "page_id": page_id,
            "link_data": link_data,
        }

    # Advantage+ enhancements todos desligados
    degrees_of_freedom_spec = {
        "creative_features_spec": {
            "standard_enhancements": {"enroll_status": "OPT_OUT"},
        }
    }

    return _post(f"{AD_ACCOUNT}/adcreatives", {
        "name": name,
        "object_story_spec": json.dumps(object_story_spec),
        "degrees_of_freedom_spec": json.dumps(degrees_of_freedom_spec),
    })


# ─── ANÚNCIO ─────────────────────────────────────────────────────────────────

def create_ad(name: str, ad_set_id: str, creative_id: str) -> dict:
    return _post(f"{AD_ACCOUNT}/ads", {
        "name": name,
        "adset_id": ad_set_id,
        "creative": json.dumps({"creative_id": creative_id}),
        "status": "PAUSED",
    })


# ─── ATIVAÇÃO ────────────────────────────────────────────────────────────────

def activate(object_id: str) -> dict:
    return _post(object_id, {"status": "ACTIVE"})


# ─── UTILITÁRIOS ─────────────────────────────────────────────────────────────

def get_pages() -> dict:
    return _get("me/accounts")


def get_lead_forms(page_id: str, page_access_token: str) -> dict:
    return _get(f"{page_id}/leadgen_forms", {"access_token": page_access_token})


def get_custom_audiences() -> dict:
    return _get(f"{AD_ACCOUNT}/customaudiences", {
        "fields": "id,name,subtype",
        "limit": "100",
    })
