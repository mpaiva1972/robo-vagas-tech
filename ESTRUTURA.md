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
