robo-vagas-tech/
│
├── config.py              # Configurações gerais (você personaliza)
├── requirements.txt       # Bibliotecas necessárias
├── robo_principal.py      # Orquestrador principal
├── enviar_email.py        # Envio de e-mail
│
└── sites/                 # 📁 PASTA DE COMPONENTES POR SITE
    ├── __init__.py        # Torna a pasta um módulo Python
    ├── base_scraper.py    # Classe base (não mexa)
    ├── linkedin.py        # ✅ Componente LinkedIn
    ├── indeed.py          # (futuro)
    ├── jobijoba.py        # (futuro)
    └── infojobs.py        # (futuro)
