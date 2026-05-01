# ============================================
# CONFIGURAÇÕES DO ROBÔ DE VAGAS
# ============================================
# MUDE ESTAS INFORMAÇÕES COMO QUISER!

# LISTA DE CARGOS QUE VOCÊ QUER BUSCAR
# (Pode colocar quantos quiser, é só separar por vírgula)
CARGOS = [
    "Projetos",
    "Project",
    "PMO",
    "Delivery",
    "Transformação",
    "Enterprise",
    "Agilidade",
    "Agile",
    "RTE",
    "Coach"
]

# TIPO DE TRABALHO (escolha UMA das opções abaixo)
# "remoto" - só vagas remotas
# "hibrido" - só vagas híbridas  
# "presencial" - só vagas presenciais
# "" - vazio = qualquer tipo
TIPO_TRABALHO = "hibrido"

# NÍVEL DE EXPERIÊNCIA (escolha UMA opção)
# "junior" , "pleno", "senior", "especialista"
# "" - vazio = qualquer nível
NIVEL_EXPERIENCIA = ""

# SITES PARA BUSCAR (não mude a menos que saiba o que faz)
SITES_ATIVOS = ["linkedin", "indeed", "jobijoba", "infojobs"]

# LIMITE DE VAGAS POR SITE
LIMITE_VAGAS = 10

# ============================================
# NÃO MEXA DAQUI PARA BAIXO (configurações internas)
# ============================================
TIPO_TRABALHO_MAP = {
    "remoto": "remote",
    "hibrido": "hybrid", 
    "presencial": "onsite"
}

NIVEL_MAP = {
    "junior": "entry level",
    "pleno": "associate",
    "senior": "senior",
    "especialista": "expert"
}
