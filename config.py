# ============================================
# CONFIGURAÇÕES DO ROBÔ DE VAGAS - LINKEDIN
# ============================================

# ---------- O QUE VOCÊ MUDA ----------
# LISTA DE CARGOS (pode colocar quantos quiser)
CARGOS = [
    "Enterprise Agile Coach",
    "Consultor de Transformação Organizacional",
    "Consultor de Agilidade e Transformação",
    "Gerente de Estratégia e Transformação",
    "Head de Delivery Transformation",
    "Lean Portfolio Execution Lead",
    "PMO Estratégico",
    "Transformation PMO",
    "Gerente PMO",
    "Delivery Manager"
]

# TIPO DE TRABALHO (opções: "remoto", "hibrido", "presencial", "")
TIPO_TRABALHO = "remoto"

# NÍVEL DE EXPERIÊNCIA (opções: "junior", "pleno", "senior", "especialista", "")
NIVEL_EXPERIENCIA = "senior"

# ---------- CONFIGURAÇÕES TÉCNICAS (NÃO MEXA) ----------
# URL base do LinkedIn
LINKEDIN_BASE_URL = "https://www.linkedin.com/jobs/search"

# Mapeamento para os filtros do LinkedIn
TIPO_TRABALHO_MAP = {
    "remoto": "2",      # 2 = Remote
    "hibrido": "1",     # 1 = Hybrid
    "presencial": "3"   # 3 = On-site
}

NIVEL_MAP = {
    "junior": "1",
    "pleno": "2", 
    "senior": "3",
    "especialista": "4"
}

# Limite de vagas por busca
LIMITE_VAGAS = 20

# Sites ativos (para desligar um, mude para False)
SITES_ATIVOS = {
    "linkedin": True,
    "indeed": False,
    "jobijoba": False,
    "infojobs": False
}
