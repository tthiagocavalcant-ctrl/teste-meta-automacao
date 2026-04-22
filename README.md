# Meta Ads Agent via WhatsApp

Agente de IA que cria campanhas no Meta Ads via WhatsApp (Evolution API).

## Configuração

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente
```bash
cp .env.example .env
# Edite o .env com suas credenciais
```

### 3. Rodar o servidor
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 4. Configurar webhook na Evolution API
No painel da Evolution API, configure o webhook apontando para:
```
https://SEU_DOMINIO/webhook
```
Eventos: `messages.upsert`

## Variáveis necessárias

| Variável | Descrição |
|---|---|
| `ANTHROPIC_API_KEY` | Chave da API da Anthropic |
| `META_ACCESS_TOKEN` | Token de acesso do Meta (deve ter permissão `ads_management`) |
| `META_AD_ACCOUNT_ID` | ID da conta de anúncios (formato: `act_XXXXXXXXX`) |
| `EVOLUTION_API_URL` | URL da sua instância Evolution API |
| `EVOLUTION_API_KEY` | Chave de autenticação da Evolution API |
| `EVOLUTION_INSTANCE` | Nome da instância WhatsApp |

## Como usar

Envie mensagens no WhatsApp descrevendo a campanha:

> "Cria uma campanha de tráfego para o site minhaloja.com.br, orçamento de R$100 por dia, público de 25 a 45 anos no Brasil"

> "Adiciona essa imagem como criativo e ativa a campanha"

### Comandos especiais
- `/reset` ou `/limpar` — limpa o histórico e começa uma nova campanha

## Fluxo da campanha

1. `get_pages` → descobre o page_id
2. `create_campaign` → cria a campanha
3. `create_ad_set` → define público e orçamento
4. `upload_image` / `upload_video` → sobe a mídia
5. `create_ad_creative` → cria o criativo
6. `create_ad` → cria o anúncio
7. `activate_campaign` → ativa tudo
