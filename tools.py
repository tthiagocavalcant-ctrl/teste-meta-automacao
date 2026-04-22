"""Ferramentas do agente — metodologia imobiliária Meta Ads."""

TOOLS = [
    {
        "name": "get_pages",
        "description": "Lista as Páginas do Facebook disponíveis na conta. Use para obter page_id e page_access_token.",
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "get_custom_audiences",
        "description": (
            "Lista os públicos personalizados da conta de anúncios. "
            "Use para encontrar o ID do público 'Enviaram Forms nos últimos 90 dias' (exclusão obrigatória) "
            "e o público limitado do Conjunto A."
        ),
        "input_schema": {"type": "object", "properties": {}, "required": []},
    },
    {
        "name": "get_lead_forms",
        "description": "Lista os formulários de lead disponíveis na Página do Facebook.",
        "input_schema": {
            "type": "object",
            "properties": {
                "page_id": {"type": "string", "description": "ID da Página do Facebook"},
                "page_access_token": {"type": "string", "description": "Token de acesso da página"},
            },
            "required": ["page_id", "page_access_token"],
        },
    },
    {
        "name": "create_campaign",
        "description": (
            "Cria a campanha de Leads com CBO (orçamento no nível da campanha). "
            "Objetivo fixo: Leads. Compra: Leilão. Retorna campaign_id."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Nome da campanha (consta no planejamento)"},
                "daily_budget_cents": {
                    "type": "integer",
                    "description": "Orçamento diário total da campanha em centavos. Ex: R$100 = 10000",
                },
            },
            "required": ["name", "daily_budget_cents"],
        },
    },
    {
        "name": "create_ad_set",
        "description": (
            "Cria um conjunto de anúncios dentro da campanha. "
            "Conversão: Formulários Instantâneos. Meta: Maximizar leads. "
            "Posicionamento automático: IG+FB se age_max >= 55, só IG se < 55. "
            "Exclusão de 'Enviaram Forms nos últimos 90 dias' já incluída via excluded_audience_ids. "
            "Retorna ad_set_id."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "campaign_id": {"type": "string"},
                "name": {"type": "string", "description": "Nome do conjunto (consta no planejamento)"},
                "age_min": {"type": "integer", "description": "Idade mínima"},
                "age_max": {"type": "integer", "description": "Idade máxima"},
                "countries": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Países ISO 3166-1 alpha-2, ex: ['BR']",
                },
                "cities": {
                    "type": "array",
                    "description": "Cidades específicas. Cada item: {key: string, name: string, region: string, country: string}",
                    "items": {"type": "object"},
                },
                "interests": {
                    "type": "array",
                    "description": "Lista de interesses do direcionamento detalhado. Cada item: {id: string, name: string}",
                    "items": {"type": "object"},
                },
                "flexible_spec": {
                    "type": "array",
                    "description": "Spec completo de direcionamento flexível para Conjunto A (Padrão + Limitado). Use quando precisar combinar públicos personalizados com interesses.",
                    "items": {"type": "object"},
                },
                "excluded_audience_ids": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "IDs dos públicos personalizados a excluir (obrigatório: incluir ID do público 'Enviaram Forms 90 dias')",
                },
            },
            "required": ["campaign_id", "name", "age_min", "age_max", "countries"],
        },
    },
    {
        "name": "upload_image",
        "description": "Sobe imagem para o Meta Ads a partir de URL. Retorna image_hash.",
        "input_schema": {
            "type": "object",
            "properties": {
                "image_url": {"type": "string"},
                "label": {"type": "string", "description": "Identificador para referência, ex: 'Anúncio A'"},
            },
            "required": ["image_url"],
        },
    },
    {
        "name": "upload_video",
        "description": "Sobe vídeo para o Meta Ads a partir de URL. Retorna video_id.",
        "input_schema": {
            "type": "object",
            "properties": {
                "video_url": {"type": "string"},
                "title": {"type": "string"},
                "label": {"type": "string", "description": "Identificador para referência, ex: 'Anúncio C'"},
            },
            "required": ["video_url"],
        },
    },
    {
        "name": "create_ad_creative",
        "description": (
            "Cria criativo do anúncio com Formulário Instantâneo. "
            "CTA fixo: 'Saiba Mais'. Advantage+ enhancements: todos desligados. "
            "Retorna creative_id."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Nome do criativo"},
                "page_id": {"type": "string"},
                "primary_text": {"type": "string", "description": "Texto principal do anúncio"},
                "headline": {"type": "string", "description": "Título do anúncio"},
                "lead_gen_form_id": {"type": "string", "description": "ID do formulário de lead"},
                "image_hash": {"type": "string", "description": "Hash da imagem (se anúncio de imagem)"},
                "video_id": {"type": "string", "description": "ID do vídeo (se anúncio de vídeo)"},
                "description": {"type": "string", "description": "Descrição opcional"},
            },
            "required": ["name", "page_id", "primary_text", "headline", "lead_gen_form_id"],
        },
    },
    {
        "name": "create_ad",
        "description": "Cria anúncio vinculando conjunto e criativo. Retorna ad_id.",
        "input_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Nome do anúncio (consta no arquivo)"},
                "ad_set_id": {"type": "string"},
                "creative_id": {"type": "string"},
            },
            "required": ["name", "ad_set_id", "creative_id"],
        },
    },
    {
        "name": "activate_all",
        "description": (
            "Ativa campanha, todos os conjuntos e todos os anúncios. "
            "Só execute após confirmação explícita do usuário."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "campaign_id": {"type": "string"},
                "ad_set_ids": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "IDs dos 3 conjuntos",
                },
                "ad_ids": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "IDs de todos os anúncios",
                },
            },
            "required": ["campaign_id", "ad_set_ids", "ad_ids"],
        },
    },
]
