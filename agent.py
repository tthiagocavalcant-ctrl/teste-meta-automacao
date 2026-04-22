import json
import anthropic
import meta_api
from tools import TOOLS
from interests_db import INTEREST_MAP, get_interests, list_available

client = anthropic.Anthropic()

def _build_interest_reference() -> str:
    """Gera bloco de referência de interesses para o system prompt."""
    from interests_db import (
        PADRAO_BAIXO, PADRAO_MEDIO, PADRAO_ALTO,
        LIMITADO_INVESTIDORES, LIMITADO_PESSOAS_COM_GRANA, LIMITADO_EMPRESARIOS,
        LIMITADO_LITORAL, LIMITADO_MARCAS_LUXO,
        SOLO_IMOVEIS, SOLO_CARGOS, SOLO_INVESTIDORES, SOLO_AGRICULTURA,
    )
    def fmt(lst): return " | ".join(lst)
    return f"""
════════════════════════════════════════
BASE DE INTERESSES (USE INTERNAMENTE)
════════════════════════════════════════

▸ PADRÃO BAIXO (Classe B/econômico):
  {fmt(PADRAO_BAIXO)}

▸ PADRÃO MÉDIO (Classe M):
  {fmt(PADRAO_MEDIO)}

▸ PADRÃO ALTO (Classe A/luxo):
  {fmt(PADRAO_ALTO)}

▸ LIMITADO — INVESTIDORES:
  {fmt(LIMITADO_INVESTIDORES)}

▸ LIMITADO — PESSOAS COM GRANA:
  {fmt(LIMITADO_PESSOAS_COM_GRANA)}

▸ LIMITADO — EMPRESÁRIOS:
  {fmt(LIMITADO_EMPRESARIOS)}

▸ LIMITADO — LITORAL:
  {fmt(LIMITADO_LITORAL)}

▸ LIMITADO — MARCAS DE LUXO:
  {fmt(LIMITADO_MARCAS_LUXO)}

▸ SOLO — IMÓVEIS:
  {fmt(SOLO_IMOVEIS)}

▸ SOLO — CARGOS:
  {fmt(SOLO_CARGOS)}

▸ SOLO — INVESTIDORES:
  {fmt(SOLO_INVESTIDORES)}

▸ SOLO — AGRICULTURA:
  {fmt(SOLO_AGRICULTURA)}
"""


SYSTEM_PROMPT = """Você é um especialista em tráfego pago para imobiliárias, responsável por criar campanhas no Meta Ads seguindo uma metodologia específica e obrigatória.

════════════════════════════════════════
METODOLOGIA IMOBILIÁRIA — SIGA RIGOROSAMENTE
════════════════════════════════════════

▸ NÍVEL DE CAMPANHA
  - Objetivo: Leads
  - Tipo de compra: Leilão
  - Orçamento: CBO (budget no nível da campanha, não no conjunto)
  - Status inicial: PAUSADO

▸ ESTRUTURA DE CONJUNTOS (sempre 3 conjuntos)

  Conjunto A | Região A (maior) | Público Padrão + Limitado | Faixa etária | Posicionamento
  Conjunto B | Região A (maior) | Público Padrão             | Faixa etária | Posicionamento
  Conjunto C | Região B (menor) | Público Padrão             | Faixa etária | Posicionamento

  Observações:
  - Região A é SEMPRE maior que Região B (ex: estado vs cidade, cidade vs bairro)
  - Conjunto A tem direcionamento detalhado (interesses/comportamentos limitando o público padrão)
  - Conjuntos B e C são Público Padrão (sem interesses — apenas localização, idade e gênero)

▸ CONFIGURAÇÕES OBRIGATÓRIAS DE CADA CONJUNTO
  - Local de conversão: Formulários Instantâneos (ON_AD)
  - Meta de desempenho: Maximizar número de leads (LEAD_GENERATION)
  - Limite de gasto mínimo: R$10,00 por conjunto
  - Exclusão obrigatória: público personalizado "Enviaram Forms nos últimos 90 dias"
  - Gênero: Todos

▸ REGRA DE POSICIONAMENTO (baseada na faixa etária)
  - age_max >= 55 → Instagram + Facebook (feed, story, reels de ambos)
  - age_max < 55  → Apenas Instagram (stream, story, reels, explore)

▸ ESTRUTURA DE ANÚNCIOS (sempre 4 anúncios no total)
  Conjunto A → Anúncio A + Anúncio B  (mesmos criativos do Conj B)
  Conjunto B → Anúncio A + Anúncio B  (mesmos criativos do Conj A)
  Conjunto C → Anúncio C + Anúncio D  (criativos diferentes)

  Cada anúncio tem:
  - Anúncios com Vários Anunciantes: Sim
  - Destino: Formulário Instantâneo (deixar em branco o link)
  - CTA: "Saiba Mais" (LEARN_MORE)
  - Aprimoramento de Criativos Advantage+: TODOS desligados
  - Aprimoramentos Essenciais: Desativados

════════════════════════════════════════
COMO INTERPRETAR O PLANEJAMENTO
════════════════════════════════════════

O usuário vai enviar um planejamento neste formato padrão. Extraia os dados automaticamente:

  CAMPANHA
    Nome da Campanha → nome da campanha
    Orçamento Diário → daily_budget_cents (converter R$ para centavos)
    Classe do Empreendimento → define os interesses padrão (Baixo/Médio/Alto)

  CONTA
    Página do Facebook → page_id (buscar via get_pages pelo nome)
    Formulário de Lead → lead_gen_form_id (buscar via get_lead_forms pelo nome)

  CONJUNTO A → nome, Região A, idade mínima, idade máxima, público limitado
  CONJUNTO B → nome, Região A (mesma do A), idade mínima, idade máxima
  CONJUNTO C → nome, Região B, idade mínima, idade máxima

  TEXTOS → Texto 1 e Texto 2
  TÍTULOS → Título 1, 2, 3, 4

  ANÚNCIOS → nome, criativo (URL ou arquivo enviado), qual texto, qual título

▸ REGRA DOS INTERESSES:
  - "Classe do Empreendimento" define o público padrão (Baixo/Médio/Alto da base interna)
  - "Público Limitado a" no Conjunto A define qual lista da base usar para restringir
  - O agente usa a BASE DE INTERESSES interna — nunca precisa perguntar quais são os interesses

════════════════════════════════════════
FLUXO DE EXECUÇÃO OBRIGATÓRIO
════════════════════════════════════════

Passo 0 — LEITURA DO PLANEJAMENTO
  Ao receber o planejamento, extraia todos os dados e apresente um resumo confirmando o que entendeu.
  Só pergunte o que estiver genuinamente faltando (ex: criativos não enviados ainda).

Passo 1 — get_pages → confirmar page_id e page_access_token pelo nome da página
Passo 2 — get_custom_audiences → encontrar ID do público "Enviaram Forms nos últimos 90 dias"
Passo 3 — get_lead_forms → confirmar formulário correto pelo nome
Passo 4 — upload das mídias A, B, C, D
Passo 5 — create_campaign (CBO, Leads)
Passo 6 — create_ad_set Conjunto A (Região A + interesses padrão + limitado)
Passo 7 — create_ad_set Conjunto B (Região A + interesses padrão)
Passo 8 — create_ad_set Conjunto C (Região B + interesses padrão)
Passo 9 — create_ad_creative para A, B, C, D
Passo 10 — create_ad: Conj A → Anúncio A + B | Conj B → Anúncio A + B | Conj C → Anúncio C + D
Passo 11 — Exibir RESUMO COMPLETO e aguardar confirmação
Passo 12 — activate_all (somente após "sim" explícito)

════════════════════════════════════════
REGRAS GERAIS
════════════════════════════════════════
- Responda SEMPRE em português brasileiro
- Ao receber o planejamento, confirme o que entendeu antes de executar
- Ao subir mídias, identifique pelo label (Anúncio A, B, C, D)
- Se o usuário enviar imagem/vídeo via WhatsApp, use a URL para upload
- Nunca ative sem confirmação explícita ("sim", "pode ativar", "ativa")
- Ao final de cada passo, informe o que foi criado e o ID
- Use /reset para limpar e iniciar nova campanha
""" + _build_interest_reference()

_conversations: dict[str, list] = {}


def _execute_tool(tool_name: str, tool_input: dict) -> str:
    try:
        if tool_name == "get_pages":
            result = meta_api.get_pages()

        elif tool_name == "get_custom_audiences":
            result = meta_api.get_custom_audiences()

        elif tool_name == "get_lead_forms":
            result = meta_api.get_lead_forms(
                tool_input["page_id"],
                tool_input["page_access_token"],
            )

        elif tool_name == "create_campaign":
            result = meta_api.create_campaign(
                name=tool_input["name"],
                daily_budget_cents=tool_input["daily_budget_cents"],
            )

        elif tool_name == "create_ad_set":
            excluded = None
            if tool_input.get("excluded_audience_ids"):
                excluded = [{"id": aid} for aid in tool_input["excluded_audience_ids"]]

            result = meta_api.create_ad_set(
                campaign_id=tool_input["campaign_id"],
                name=tool_input["name"],
                age_min=tool_input["age_min"],
                age_max=tool_input["age_max"],
                countries=tool_input["countries"],
                cities=tool_input.get("cities"),
                interests=tool_input.get("interests"),
                flexible_spec=tool_input.get("flexible_spec"),
                excluded_custom_audiences=excluded,
            )

        elif tool_name == "upload_image":
            result = meta_api.upload_image_from_url(tool_input["image_url"])
            result["label"] = tool_input.get("label", "")

        elif tool_name == "upload_video":
            result = meta_api.upload_video_from_url(
                tool_input["video_url"],
                title=tool_input.get("title", "Video"),
            )
            result["label"] = tool_input.get("label", "")

        elif tool_name == "create_ad_creative":
            result = meta_api.create_ad_creative(
                name=tool_input["name"],
                page_id=tool_input["page_id"],
                primary_text=tool_input["primary_text"],
                headline=tool_input["headline"],
                lead_gen_form_id=tool_input["lead_gen_form_id"],
                image_hash=tool_input.get("image_hash"),
                video_id=tool_input.get("video_id"),
                description=tool_input.get("description"),
            )

        elif tool_name == "create_ad":
            result = meta_api.create_ad(
                name=tool_input["name"],
                ad_set_id=tool_input["ad_set_id"],
                creative_id=tool_input["creative_id"],
            )

        elif tool_name == "activate_all":
            meta_api.activate(tool_input["campaign_id"])
            for aid in tool_input.get("ad_set_ids", []):
                meta_api.activate(aid)
            for aid in tool_input.get("ad_ids", []):
                meta_api.activate(aid)
            result = {
                "status": "ACTIVE",
                "campaign": tool_input["campaign_id"],
                "ad_sets": tool_input.get("ad_set_ids"),
                "ads": tool_input.get("ad_ids"),
                "message": "Campanha, conjuntos e anúncios ativados com sucesso!",
            }

        else:
            result = {"error": f"Ferramenta desconhecida: {tool_name}"}

    except Exception as e:
        result = {"error": str(e)}

    return json.dumps(result, ensure_ascii=False)


def chat(sender: str, user_message: str, media_url: str = None, media_type: str = None) -> str:
    history = _conversations.setdefault(sender, [])

    content = user_message or ""
    if media_url and media_type == "image":
        content += f"\n[Imagem recebida via WhatsApp — URL para upload: {media_url}]"
    elif media_url and media_type == "video":
        content += f"\n[Vídeo recebido via WhatsApp — URL para upload: {media_url}]"

    history.append({"role": "user", "content": content})

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=8096,
            system=SYSTEM_PROMPT,
            tools=TOOLS,
            messages=history,
        )

        history.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            text_blocks = [b.text for b in response.content if hasattr(b, "text")]
            return "\n".join(text_blocks)

        if response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = _execute_tool(block.name, block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    })
            history.append({"role": "user", "content": tool_results})
            continue

        break

    return "Ocorreu um erro inesperado. Tente novamente."


def clear_history(sender: str):
    _conversations.pop(sender, None)
