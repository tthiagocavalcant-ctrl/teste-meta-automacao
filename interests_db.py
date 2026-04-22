"""
Base de interesses para campanhas imobiliárias.
O agente usa esses dados internamente — o usuário só precisa referenciar
o nome do conjunto (ex: "Padrão Médio", "Limitado Investidores").
"""

# ─── INTERESSES PADRÃO POR CLASSE ────────────────────────────────────────────

PADRAO_BAIXO = [
    "Apartamento/Casa/condomínio/lote",
    "imóveis",
    "investimento imobiliário",
    "Noivos",
    "Noivaram 3 meses",
    "Noivaram 6 meses",
    "recém casados 3 meses",
    "recém casados 6 meses",
    "noivaram recentemente 1 ano",
    "subsídio para compra da primeira casa",
    "primeira casa",
    "comprador de primeiro imóvel",
    "vestido de casamento",
    "noivado",
    "cerimônias de casamento",
    "Pais, mães ou responsáveis (até 12 meses)",
    "Pais com crianças pequenas (1 a 2 anos de idade)",
    "Pais com crianças em idade pré-escolar (de 3 a 5 anos)",
    "Consórcio",
    "Crédito (financiamento)",
    "Financiamento",
]

PADRAO_MEDIO = [
    "Apartamento/Casa/condomínio/lote",
    "imóveis",
    "clube de investimento imobiliário",
    "investimento imobiliário",
    "Pessoas no Brasil que preferem produtos de valor intermediário e alto",
    "comprador de primeiro imóvel",
    "Noivo",
    "Noivaram 3 meses",
    "Noivaram 6 meses",
    "recém casados 3 meses",
    "recém casados 6 meses",
    "noivaram recentemente 1 ano",
    "vestido de casamento",
    "noivado",
    "cerimônias de casamento",
    "Consórcio",
    "Crédito (financiamento)",
    "Financiamento",
    "Serviços de saúde e médicos",
    "faculdade de medicina (ensino superior)",
]

PADRAO_ALTO = [
    "Apartamento/Casa/condomínio/lote",
    "imóveis",
    "clube de investimento imobiliário",
    "investimento imobiliário",
    "Financiamento",
    "Pessoas no Brasil que preferem produtos de valor intermediário e alto",
    "Pessoas que preferem produtos de valor alto no Brasil",
    "Viajantes frequentes internacionais",
    "Gucci (marca de moda)",
    "Armani (vestuário)",
    "Proprietários de pequenas empresas",
    "Dono (cargos)",
    "Proprietário",
    "Serviços de saúde e médicos",
    "faculdade de medicina (ensino superior)",
    "advogado (interesses)",
    "viagem em primeira classe",
    "classe executiva",
]

# ─── PÚBLICOS PARA LIMITAR (Conjunto A) ──────────────────────────────────────

LIMITADO_PESSOAS_COM_GRANA = [
    "Pessoas que preferem produtos de valor alto no Brasil",
    "Viajantes frequentes internacionais",
    "classe executiva",
]

LIMITADO_LUGARES = [
    "Balneário Camboriú",
    "Alphaville",
    "Praia de Porto de Galinhas",
    "Guarujá",
    "Rio de Janeiro",
    "Natal (Capital do Rio Grande do Norte)",
]

LIMITADO_EMPRESARIOS = [
    "Proprietários de pequenas empresas",
    "Proprietário",
    "Dono (cargos)",
    "Gerente Proprietário",
    "Comerciante",
]

LIMITADO_LITORAL = [
    "Praias (lugares)",
    "Mar",
    "Barcos",
    "Lancha",
    "Jetski",
    "Surfing (water sport)",
    "prancha de surf",
    "Veículo Aquático Pessoal",
    "Marina",
]

LIMITADO_MARCAS_LUXO = [
    "Louis Vuitton (marca de moda)",
    "Chanel (marca de moda)",
    "H.Stern",
    "Alexandre Birman",
    "Casa Vogue Brasil",
    "Montblanc",
    "Gucci (marca de moda)",
    "Prada (marca de moda)",
    "Armani",
    "Tommy Hilfiger",
]

LIMITADO_INVESTIDORES = [
    "Fundo de Investimento Imobiliário",
    "Estratégia de Investimento",
    "Mercado Financeiro",
    "Mercado de Ações",
    "Riqueza",
    "Bolsa de Valores",
    "Finanças",
    "Estoque (Investimento)",
    "Plano Financeiro",
    "XP Investimentos",
    "Grupo Financeiro",
    "Índice do Mercado de Ações",
    "Corretor da Bolsa",
    "Gestão Estratégica",
]

# ─── PÚBLICOS SOLOS ───────────────────────────────────────────────────────────

SOLO_IMOVEIS = [
    "Imóveis/Apartamentos/Condomínios/Lotes/Casa",
    "Investimento imobiliário",
    "clube do investimento imobiliário",
]

SOLO_CARGOS = [
    "Cirurgião Dentista Implantodontista (cargo)",
    "Dentist (cargo)",
    "Medical Doctor MD (cargo)",
    "Serviços de saúde e médicos",
    "advogado (interesses)",
    "Proprietário",
    "Gerente Proprietário",
    "Serviços jurídicos",
    "Tecnologia da Informação",
    "Serviços técnicos e de TI",
]

SOLO_MARCAS_LUXO = LIMITADO_MARCAS_LUXO

SOLO_INVESTIDORES = LIMITADO_INVESTIDORES

SOLO_AGRICULTURA = [
    "agricultor",
    "Agronomia",
    "Agrônomo",
    "Agronegócio",
    "Agriculture (Industry)",
    "Engenharia agronômica",
    "Pecuária",
]

# ─── ÍNDICE ───────────────────────────────────────────────────────────────────

INTEREST_MAP = {
    # Padrão
    "padrao baixo": PADRAO_BAIXO,
    "padrão baixo": PADRAO_BAIXO,
    "baixo padrão": PADRAO_BAIXO,
    "baixo padrao": PADRAO_BAIXO,
    "classe b": PADRAO_BAIXO,
    "padrao medio": PADRAO_MEDIO,
    "padrão médio": PADRAO_MEDIO,
    "médio padrão": PADRAO_MEDIO,
    "medio padrao": PADRAO_MEDIO,
    "classe m": PADRAO_MEDIO,
    "padrao alto": PADRAO_ALTO,
    "padrão alto": PADRAO_ALTO,
    "alto padrão": PADRAO_ALTO,
    "alto padrao": PADRAO_ALTO,
    "classe a": PADRAO_ALTO,
    # Limitado
    "limitado pessoas com grana": LIMITADO_PESSOAS_COM_GRANA,
    "limitado grana": LIMITADO_PESSOAS_COM_GRANA,
    "limitado lugares": LIMITADO_LUGARES,
    "limitado empresarios": LIMITADO_EMPRESARIOS,
    "limitado empresários": LIMITADO_EMPRESARIOS,
    "limitado litoral": LIMITADO_LITORAL,
    "limitado marcas luxo": LIMITADO_MARCAS_LUXO,
    "limitado luxo": LIMITADO_MARCAS_LUXO,
    "limitado investidores": LIMITADO_INVESTIDORES,
    "investidores": LIMITADO_INVESTIDORES,
    # Solo
    "solo imoveis": SOLO_IMOVEIS,
    "solo imóveis": SOLO_IMOVEIS,
    "solo cargos": SOLO_CARGOS,
    "solo marcas luxo": SOLO_MARCAS_LUXO,
    "solo luxo": SOLO_MARCAS_LUXO,
    "solo investidores": SOLO_INVESTIDORES,
    "solo agricultura": SOLO_AGRICULTURA,
    "agricultura": SOLO_AGRICULTURA,
}


def get_interests(key: str) -> list[str]:
    """Retorna lista de interesses pelo nome do conjunto."""
    return INTEREST_MAP.get(key.lower().strip(), [])


def list_available() -> list[str]:
    return sorted(set(INTEREST_MAP.keys()))
