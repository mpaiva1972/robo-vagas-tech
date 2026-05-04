"""
Classe base para todos os raspadores de sites.
Todo novo site deve herdar desta classe.
"""

import requests
from bs4 import BeautifulSoup
import time
from abc import ABC, abstractmethod

class BaseScraper(ABC):
    """Clase base para raspadores de vagas"""
    
    def __init__(self, config):
        self.config = config
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        self.vagas_encontradas = []
    
    @abstractmethod
    def montar_url(self, cargo, tipo_trabalho, nivel):
        """Cada site monta sua URL de busca de forma diferente"""
        pass
    
    @abstractmethod
    def extrair_vagas(self, html, cargo_buscado):
        """Cada site extrai os dados de forma diferente"""
        pass
    
    def buscar(self, cargo):
        """Método principal que busca vagas para um cargo"""
        url = self.montar_url(cargo, self.config.TIPO_TRABALHO, self.config.NIVEL_EXPERIENCIA)
        vagas_do_cargo = []
        
        try:
            print(f"      Acessando: {url[:80]}...")
            resposta = requests.get(url, headers=self.headers, timeout=15)
            
            if resposta.status_code == 200:
                vagas_do_cargo = self.extrair_vagas(resposta.text, cargo)
                print(f"      ✅ {len(vagas_do_cargo)} vagas encontradas")
            else:
                print(f"      ⚠️ Erro {resposta.status_code}")
                
        except Exception as e:
            print(f"      ❌ Erro: {str(e)[:50]}")
        
        time.sleep(2)  # Delay para não sobrecarregar
        return vagas_do_cargo
