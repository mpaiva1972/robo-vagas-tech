"""
Raspador específico para o LinkedIn - Versão com seletores atualizados
"""

from bs4 import BeautifulSoup
import time
import requests
import re
import sys
import os

# Adiciona o diretório pai para importar config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

class LinkedInScraper:
    """Raspador de vagas do LinkedIn - Versão simplificada e robusta"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }
        self.vagas_encontradas = []
    
    def montar_url(self, cargo, tipo_trabalho, nivel):
        """Monta a URL de busca do LinkedIn"""
        cargo_codificado = cargo.replace(' ', '%20')
        
        url = f"https://www.linkedin.com/jobs/search/?keywords={cargo_codificado}&location=Brasil"
        
        # Filtro de tipo de trabalho
        if tipo_trabalho and tipo_trabalho in config.TIPO_TRABALHO_MAP:
            url += f"&f_WT={config.TIPO_TRABALHO_MAP[tipo_trabalho]}"
        
        # Filtro de nível
        if nivel and nivel in config.NIVEL_MAP:
            url += f"&f_E={config.NIVEL_MAP[nivel]}"
        
        # Tempo integral
        url += "&f_JT=FULL_TIME"
        
        # Ordenar por data (mais recentes primeiro)
        url += "&sortBy=DD"
        
        return url
    
    def extrair_vagas(self, html, cargo_buscado):
        """Extrai vagas usando múltiplas estratégias"""
        soup = BeautifulSoup(html, 'html.parser')
        vagas = []
        
        # ESTRATÉGIA 1: Buscar pelos cards de jobs (mais comum)
        cards = soup.find_all(['div', 'li'], class_=re.compile(r'job-card|job-card-container|jobs-search__result'))
        
        if not cards:
            # ESTRATÉGIA 2: Buscar por elementos com data-job-id (estrutura alternativa)
            cards = soup.find_all(attrs={'data-job-id': re.compile(r'.*')})
        
        if not cards:
            # ESTRATÉGIA 3: Buscar por links de vagas
            cards = soup.find_all('a', href=re.compile(r'/jobs/view/'))
        
        print(f"      Encontrados {len(cards)} cards de vagas no HTML")
        
        for card in cards[:config.LIMITE_VAGAS]:
            vaga = self._extrair_dados_vaga(card, soup, cargo_buscado)
            if vaga and self._is_ti_vaga(vaga['titulo']):
                vagas.append(vaga)
        
        return vagas
    
    def _extrair_dados_vaga(self, card, soup, cargo_buscado):
        """Extrai dados de um card de vaga usando múltiplos seletores"""
        try:
            titulo = None
            empresa = None
            local = None
            link = None
            
            # ESTRATÉGIAS PARA TÍTULO
            seletores_titulo = [
                ('h3', {'class': re.compile(r'job-title|base-search-card__title|job-card-list__title')}),
                ('a', {'class': re.compile(r'job-title|base-search-card__title')}),
                ('span', {'class': re.compile(r'sr-only')}),
                ('strong', {})
            ]
            
            for tag, attrs in seletores_titulo:
                elem = card.find(tag, attrs) if attrs else card.find(tag)
                if elem:
                    titulo = elem.get_text(strip=True)
                    break
            
            if not titulo:
                # Tenta por texto bruto
                texto = card.get_text(strip=True)
                linhas = texto.split('\n')
                if linhas:
                    titulo = linhas[0][:100]
            
            # ESTRATÉGIAS PARA EMPRESA
            seletores_empresa = [
                ('h4', {'class': re.compile(r'base-search-card__subtitle|company-name')}),
                ('span', {'class': re.compile(r'company-name|job-card-container__company-name')}),
                ('div', {'class': re.compile(r'company-name')}),
                ('a', {'class': re.compile(r'company')})
            ]
            
            for tag, attrs in seletores_empresa:
                elem = card.find(tag, attrs) if attrs else card.find(tag)
                if elem:
                    empresa = elem.get_text(strip=True)
                    break
            
            # ESTRATÉGIAS PARA LOCAL
            seletores_local = [
                ('span', {'class': re.compile(r'location|job-card-container__metadata-item')}),
                ('div', {'class': re.compile(r'location')}),
                ('span', {'class': re.compile(r'metadata')})
            ]
            
            for tag, attrs in seletores_local:
                elem = card.find(tag, attrs) if attrs else card.find(tag)
                if elem:
                    local = elem.get_text(strip=True)
                    break
            
            # ESTRATÉGIAS PARA LINK
            link_elem = card.find('a', href=re.compile(r'/jobs/view/|/jobs/search/view/'))
            if link_elem:
                link = link_elem.get('href')
                if link and not link.startswith('https'):
                    link = 'https://www.linkedin.com' + link
            else:
                link_elem = card.find('a')
                if link_elem and link_elem.get('href'):
                    link = link_elem.get('href')
                    if '/jobs/' in link and not link.startswith('https'):
                        link = 'https://www.linkedin.com' + link
            
            if not titulo or not empresa:
                return None
            
            # Verifica se parece uma vaga de TI
            is_ti = self._is_ti_vaga(titulo)
            
            return {
                "titulo": titulo[:120],
                "empresa": empresa[:80],
                "local": local[:60] if local else "Não informado",
                "link": link or "",
                "site": "LinkedIn",
                "cargo_buscado": cargo_buscado,
                "score_executivo": "⭐ TI" if is_ti else ""
            }
            
        except Exception as e:
            return None
    
    def _is_ti_vaga(self, titulo):
        """Verifica se a vaga é de Tecnologia da Informação"""
        titulo_lower = titulo.lower()
        
        # Palavras-chave de TI
        palavras_ti = [
            'tech', 'technology', 'tecnologia', 'tecnológico',
            'software', 'engenheiro', 'engineer', 'engineering',
            'desenvolvedor', 'developer', 'development',
            'programador', 'programmer', 'coding',
            'sistemas', 'systems', 'it', 'informática',
            'cloud', 'dados', 'data', 'analytics',
            'devops', 'agile', 'scrum', 'product',
            'frontend', 'backend', 'fullstack', 'full stack',
            'python', 'java', 'javascript', 'react', 'node',
            'sql', 'database', 'api', 'microservices'
        ]
        
        return any(palavra in titulo_lower for palavra in palavras_ti)
    
    def buscar(self, cargo):
        """Busca vagas para um cargo"""
        url = self.montar_url(cargo, config.TIPO_TRABALHO, config.NIVEL_EXPERIENCIA)
        
        print(f"        URL: {url[:100]}...")
        
        try:
            resposta = requests.get(url, headers=self.headers, timeout=20)
            
            if resposta.status_code == 200:
                vagas = self.extrair_vagas(resposta.text, cargo)
                print(f"        ✅ {len(vagas)} vagas de TI encontradas")
                return vagas
            else:
                print(f"        ⚠️ Erro HTTP {resposta.status_code}")
                return []
                
        except Exception as e:
            print(f"        ❌ Erro: {str(e)[:60]}")
            return []

def buscar_vagas_linkedin(cargos):
    """Função principal que coordena a busca no LinkedIn"""
    scraper = LinkedInScraper()
    todas_vagas = []
    
    for i, cargo in enumerate(cargos, 1):
        print(f"    [{i}/{len(cargos)}] Buscando: {cargo}")
        vagas = scraper.buscar(cargo)
        todas_vagas.extend(vagas)
        time.sleep(3)  # Delay entre cargos
    
    return todas_vagas
