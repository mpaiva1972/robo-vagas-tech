import requests
from bs4 import BeautifulSoup
import time
import re
from datetime import datetime
import urllib.parse

# Importa as configurações que você fez
from config import *

def buscar_linkedin(cargo):
    """Busca vagas no LinkedIn"""
    vagas = []
    
    # Monta a URL de busca
    cargo_url = cargo.replace(" ", "%20")
    url = f"https://www.linkedin.com/jobs/search/?keywords={cargo_url}&location=Brasil"
    
    # Adiciona filtro de tipo de trabalho se configurado
    if TIPO_TRABALHO and TIPO_TRABALHO in TIPO_TRABALHO_MAP:
        tipo_en = TIPO_TRABALHO_MAP[TIPO_TRABALHO]
        url += f"&f_WT={tipo_en}"
    
    # Adiciona filtro de nível se configurado
    if NIVEL_EXPERIENCIA and NIVEL_EXPERIENCIA in NIVEL_MAP:
        nivel_en = NIVEL_MAP[NIVEL_EXPERIENCIA]
        url += f"&f_E={nivel_en}"
    
    try:
        # Simula um navegador real
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        resposta = requests.get(url, headers=headers, timeout=15)
        
        if resposta.status_code == 200:
            soup = BeautifulSoup(resposta.text, 'html.parser')
            
            # Procura os cards de vagas
            cards = soup.find_all('div', class_='job-card-container')
            
            for card in cards[:LIMITE_VAGAS]:
                try:
                    # Título da vaga
                    titulo_elem = card.find('a', class_='job-card-list__title')
                    titulo = titulo_elem.text.strip() if titulo_elem else "N/A"
                    
                    # Empresa
                    empresa_elem = card.find('h4', class_='base-search-card__subtitle')
                    empresa = empresa_elem.text.strip() if empresa_elem else "N/A"
                    
                    # Local
                    local_elem = card.find('span', class_='job-card-container__metadata-item')
                    local = local_elem.text.strip() if local_elem else "N/A"
                    
                    # Link
                    link = titulo_elem.get('href') if titulo_elem else ""
                    
                    vagas.append({
                        "titulo": titulo,
                        "empresa": empresa,
                        "local": local,
                        "link": link,
                        "site": "LinkedIn",
                        "cargo_buscado": cargo
                    })
                except:
                    pass
    except:
        print(f"  ⚠️ Erro ao buscar no LinkedIn para {cargo}")
    
    return vagas

def buscar_indeed(cargo):
    """Busca vagas no Indeed"""
    vagas = []
    
    cargo_url = cargo.replace(" ", "+")
    url = f"https://www.indeed.com.br/empregos?q={cargo_url}&l=Brasil"
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        resposta = requests.get(url, headers=headers, timeout=15)
        
        if resposta.status_code == 200:
            soup = BeautifulSoup(resposta.text, 'html.parser')
            
            cards = soup.find_all('div', class_='job_seen_beacon')
            
            for card in cards[:LIMITE_VAGAS]:
                try:
                    titulo_elem = card.find('h2', class_='jobTitle')
                    titulo = titulo_elem.text.strip() if titulo_elem else "N/A"
                    
                    empresa_elem = card.find('span', class_='companyName')
                    empresa = empresa_elem.text.strip() if empresa_elem else "N/A"
                    
                    local_elem = card.find('div', class_='companyLocation')
                    local = local_elem.text.strip() if local_elem else "N/A"
                    
                    link_elem = card.find('a')
                    link = "https://www.indeed.com.br" + link_elem.get('href') if link_elem else ""
                    
                    vagas.append({
                        "titulo": titulo,
                        "empresa": empresa,
                        "local": local,
                        "link": link,
                        "site": "Indeed",
                        "cargo_buscado": cargo
                    })
                except:
                    pass
    except:
        print(f"  ⚠️ Erro ao buscar no Indeed para {cargo}")
    
    return vagas

def buscar_jobijoba(cargo):
    """Busca vagas no Jobijoba"""
    vagas = []
    
    cargo_url = cargo.replace(" ", "%20")
    url = f"https://www.jobijoba.com.br/emprego?search={cargo_url}&where=Brasil"
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        resposta = requests.get(url, headers=headers, timeout=15)
        
        if resposta.status_code == 200:
            soup = BeautifulSoup(resposta.text, 'html.parser')
            
            cards = soup.find_all('div', class_='job')
            
            for card in cards[:LIMITE_VAGAS]:
                try:
                    titulo_elem = card.find('a', class_='job__title')
                    titulo = titulo_elem.text.strip() if titulo_elem else "N/A"
                    
                    empresa_elem = card.find('span', class_='job__company')
                    empresa = empresa_elem.text.strip() if empresa_elem else "N/A"
                    
                    local_elem = card.find('div', class_='job__location')
                    local = local_elem.text.strip() if local_elem else "N/A"
                    
                    link = titulo_elem.get('href') if titulo_elem else ""
                    
                    vagas.append({
                        "titulo": titulo,
                        "empresa": empresa,
                        "local": local,
                        "link": link,
                        "site": "Jobijoba",
                        "cargo_buscado": cargo
                    })
                except:
                    pass
    except:
        print(f"  ⚠️ Erro ao buscar no Jobijoba para {cargo}")
    
    return vagas

def buscar_infojobs(cargo):
    """Busca vagas no InfoJobs"""
    vagas = []
    
    cargo_url = cargo.replace(" ", "+")
    url = f"https://www.infojobs.com.br/vagas.aspx?Palavra={cargo_url}"
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        resposta = requests.get(url, headers=headers, timeout=15)
        
        if resposta.status_code == 200:
            soup = BeautifulSoup(resposta.text, 'html.parser')
            
            cards = soup.find_all('div', class_='vaga')
            
            for card in cards[:LIMITE_VAGAS]:
                try:
                    titulo_elem = card.find('a', class_='vaga-title')
                    titulo = titulo_elem.text.strip() if titulo_elem else "N/A"
                    
                    empresa_elem = card.find('span', class_='vaga-company')
                    empresa = empresa_elem.text.strip() if empresa_elem else "N/A"
                    
                    local_elem = card.find('span', class_='vaga-location')
                    local = local_elem.text.strip() if local_elem else "N/A"
                    
                    link = "https://www.infojobs.com.br" + titulo_elem.get('href') if titulo_elem else ""
                    
                    vagas.append({
                        "titulo": titulo,
                        "empresa": empresa,
                        "local": local,
                        "link": link,
                        "site": "InfoJobs",
                        "cargo_buscado": cargo
                    })
                except:
                    pass
    except:
        print(f"  ⚠️ Erro ao buscar no InfoJobs para {cargo}")
    
    return vagas

def buscar_todas_vagas():
    """Busca vagas em todos os sites configurados"""
    todas_vagas = []
    total_cargos = len(CARGOS)
    
    print(f"🔍 Buscando {total_cargos} cargos em {len(SITES_ATIVOS)} sites...")
    
    for i, cargo in enumerate(CARGOS, 1):
        print(f"\n📌 ({i}/{total_cargos}) Buscando: {cargo}")
        
        for site in SITES_ATIVOS:
            print(f"   • {site.capitalize()}...", end=" ")
            
            if site == "linkedin":
                resultado = buscar_linkedin(cargo)
            elif site == "indeed":
                resultado = buscar_indeed(cargo)
            elif site == "jobijoba":
                resultado = buscar_jobijoba(cargo)
            elif site == "infojobs":
                resultado = buscar_infojobs(cargo)
            else:
                continue
            
            print(f"{len(resultado)} vagas")
            todas_vagas.extend(resultado)
            time.sleep(1)  # Pausa para não sobrecarregar os sites
        
        time.sleep(2)
    
    return todas_vagas

if __name__ == "__main__":
    # Teste rápido
    vagas = buscar_todas_vagas()
    print(f"\n📊 Total de vagas encontradas: {len(vagas)}")
