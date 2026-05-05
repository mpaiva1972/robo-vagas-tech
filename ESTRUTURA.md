# 🏗️ ESTRUTURA DO ROBÔ DE VAGAS

## 📁 ORGANIZAÇÃO DOS ARQUIVOS

## 🎯 O QUE CADA ARQUIVO FAZ

| Arquivo | O que faz | Você mexe? |
|---------|-----------|------------|
| `config.py` | Lista de cargos, tipo de trabalho, nível | ✅ **SIM** |
| `enviar_email.py` | Seu e-mail e senha do app | ✅ **SIM** (só a senha) |
| `linkedin.py` | Lógica de busca do LinkedIn | ⚠️ Raramente |
| `robo_principal.py` | Coordena a busca | ❌ Não |
| `base_scraper.py` | Código base para todos os sites | ❌ Não |
| `robo_diario.yml` | Agenda para rodar todo dia | ❌ Não |

## 🔧 COMO ADICIONAR UM NOVO SITE

Para adicionar Indeed, InfoJobs ou qualquer outro site:

1. **Crie** `sites/novo_site.py` seguindo o modelo do `linkedin.py`
2. **Ative** no `config.py` mudando para `True`
3. **Importe** no `robo_principal.py` (me avise que eu ajudo)

### Modelo para novo site:

```python
from .base_scraper import BaseScraper

class NovoSiteScraper(BaseScraper):
    
    def montar_url(self, cargo, tipo_trabalho, nivel):
        # Monte a URL de busca do site
        return f"https://www.site.com.br/busca?q={cargo}"
    
    def extrair_vagas(self, html, cargo_buscado):
        # Extraia os dados do HTML
        vagas = []
        # ... lógica de extração ...
        return vagas

1. GitHub Actions (roda às 6h)
         ↓
2. robo_principal.py (orquestrador)
         ↓
3. sites/linkedin.py (busca vagas)
         ↓
4. enviar_email.py (envia e-mail)
         ↓
5. Você recebe as vagas! 🎉


---

## 📝 FORMA 2: COMENTÁRIOS DENTRO DO PRÓPRIO CÓDIGO

Adicione blocos de comentário no início de cada arquivo explicando a estrutura.

### Exemplo: No início do `robo_principal.py`

```python
"""
================================================================================
ROBÔ DE VAGAS - ORQUESTRADOR PRINCIPAL
================================================================================

ESTRUTURA DO PROJETO:

robo-vagas-tech/
├── config.py              <- VOCÊ MUDA AQUI (cargos, filtros)
├── enviar_email.py        <- SUA SENHA DO GMAIL
├── robo_principal.py      <- Este arquivo (não mexa)
├── sites/
│   ├── linkedin.py        <- Lógica do LinkedIn
│   └── base_scraper.py    <- Classe base (não mexa)
└── .github/workflows/
    └── robo_diario.yml    <- Agendador

COMO FUNCIONA:
1. O GitHub Actions roda este arquivo todo dia às 6h
2. Ele busca as configurações no config.py
3. Chama o LinkedInScraper para buscar vagas
4. Envia o resultado por e-mail

PARA ADICIONAR UM NOVO SITE:
1. Crie sites/novo_site.py
2. Ative no config.py
3. Importe abaixo na função buscar_em_todos_sites()

================================================================================
"""
