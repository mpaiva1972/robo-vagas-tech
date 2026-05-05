"""
Raspador específico para o LinkedIn
Herda da classe BaseScraper
"""

from .base_scraper import BaseScraper
from bs4 import BeautifulSoup
import time
import requests

class LinkedInScraper(BaseScraper):
    """Raspador de vagas do LinkedIn"""
    
    def montar_url(self, cargo, tipo_trabalho, nivel):
        """
        Monta a URL de busca do LinkedIn com todos os filtros
        """
        # Codifica o cargo para a URL (espaços viram %20)
        cargo_codificado = cargo.replace(' ', '%20')
        
        # Começa a montar a URL
        url = f"{self.config.LINKEDIN_BASE_URL}?keywords={cargo_codificado}&location=Brasil"
        
        # Adiciona filtro de tipo de trabalho (se foi configurado)
        if tipo_trabalho and tipo_trabalho in self.config.TIPO_TRABALHO_MAP:
            tipo_codigo = self.config.TIPO_TRABALHO_MAP[tipo_trabalho]
            url += f"&f_WT={tipo_codigo}"
        
        # Adiciona filtro de nível de experiência (se foi configurado)
        if nivel and nivel in self.config.NIVEL_MAP:
            nivel_codigo = self.config.NIVEL_MAP[nivel]
            url += f"&f_E={nivel_codigo}"
        
        # Sempre busca vagas de tempo integral
        url += "&f_JT=FULL_TIME"
        
        return url
    
    def extrair_vagas(self, html, cargo_buscado):
        """
        Extrai as vagas do HTML do LinkedIn
        """
        soup = BeautifulSoup(html, 'html.parser')
        vagas = []
        
        # Encontra todos os cards de vagas
        cards = soup.find_all('div', class_='job-card-container')
        
        for card in cards[:self.config.LIMITE_VAGAS]:
            try:
                # TÍTULO DA VAGA
                titulo_elem = card.find('a', class_='job-card-list__title')
                titulo = titulo_elem.text.strip() if titulo_elem else "N/A"
                
                # NOME DA EMPRESA
                empresa_elem = card.find('h4', class_='base-search-card__subtitle')
                if not empresa_elem:
                    empresa_elem = card.find('span', class_='job-card-container__company-name')
                empresa = empresa_elem.text.strip() if empresa_elem else "N/A"
                
                # LOCALIZAÇÃO
                local_elem = card.find('span', class_='job-card-container__metadata-item')
                if not local_elem:
                    local_elem = card.find('div', class_='job-card-container__metadata-wrapper')
                local = local_elem.text.strip() if local_elem else "N/A"
                
                # LINK DA VAGA
                link = ""
                if titulo_elem and titulo_elem.get('href'):
                    link = titulo_elem.get('href')
                
                # DATA DA PUBLICAÇÃO
                data_elem = card.find('time')
                data_publicacao = data_elem.get('datetime') if data_elem else ""
                
                # Verifica se a vaga parece ser relevante
                titulo_lower = titulo.lower()
                cargo_lower = cargo_buscado.lower()
                
                # Palavras que indicam vaga executiva
                palavras_executivas = ['leader', 'lead', 'head', 'director', 'manager', 'coach', 'consultor']
                is_executiva = any(palavra in titulo_lower for palavra in palavras_executivas)
                
                vaga = {
                    "titulo": titulo,
                    "empresa": empresa,
                    "local": local,
                    "link": link,
                    "data_publicacao": data_publicacao,
                    "site": "LinkedIn",
                    "cargo_buscado": cargo_buscado,
                    "score_executivo": "⭐" if is_executiva else ""
                }
                vagas.append(vaga)
                    
            except Exception as e:
                continue
        
        return vagas

def buscar_vagas_linkedin(cargos):
    """
    Função principal que coordena a busca no LinkedIn
    Agora recebe apenas a lista de cargos (usa config internamente)
    """
    # Importa config aqui para ter acesso às configurações
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import config
    
    scraper = LinkedInScraper(config)
    todas_vagas = []
    
    for i, cargo in enumerate(cargos, 1):
        print(f"    [{i}/{len(cargos)}] Buscando: {cargo}")
        vagas = scraper.buscar(cargo)
        todas_vagas.extend(vagas)
        time.sleep(2)  # Delay entre cargos
    
    return todas_vagas
