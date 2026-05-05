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

# FILTRO DE TECNOLOGIA (True = só vagas de TI, False = todas as vagas)
APENAS_TI = True  # ← NOVO! Mude para False se quiser todas as vagas

# ---------- CONFIGURAÇÕES TÉCNICAS (NÃO MEXA) ----------
LINKEDIN_BASE_URL = "https://www.linkedin.com/jobs/search"

TIPO_TRABALHO_MAP = {
    "remoto": "2",
    "hibrido": "1",
    "presencial": "3"
}

NIVEL_MAP = {
    "junior": "1",
    "pleno": "2",
    "senior": "3",
    "especialista": "4"
}

LIMITE_VAGAS = 15  # Aumentei para 15

SITES_ATIVOS = {
    "linkedin": True,
    "indeed": False,
    "jobijoba": False,
    "infojobs": False
}
