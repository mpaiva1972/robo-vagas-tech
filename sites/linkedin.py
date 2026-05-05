"""
Raspador do LinkedIn - Busca palavras-chave na URL e no HTML
"""

import requests
import re
import time
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

class LinkedInScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
            'Accept-Language': 'pt-BR,pt;q=0.9'
        }
    
    def montar_url_com_palavras_chave(self, cargo):
        """
        PASSO 1: Monta URL com as palavras-chave do cargo
        Isso faz o LinkedIn já retornar vagas relacionadas
        """
        cargo_codificado = cargo.replace(' ', '%20')
        
        # URL base com a palavra-chave principal
        url = f"https://www.linkedin.com/jobs/search/?keywords={cargo_codificado}&location=Brasil"
        
        # Adiciona filtro de tipo de trabalho se configurado
        if config.TIPO_TRABALHO and config.TIPO_TRABALHO in config.TIPO_TRABALHO_MAP:
            url += f"&f_WT={config.TIPO_TRABALHO_MAP[config.TIPO_TRABALHO]}"
        
        # Adiciona filtro de nível se configurado
        if config.NIVEL_EXPERIENCIA and config.NIVEL_EXPERIENCIA in config.NIVEL_MAP:
            url += f"&f_E={config.NIVEL_MAP[config.NIVEL_EXPERIENCIA]}"
        
        return url
    
    def extrair_palavras_chave(self, cargo):
        """
        Divide o cargo em palavras-chave individuais para busca no HTML
        Ex: "Enterprise Agile Coach" -> ["enterprise", "agile", "coach"]
        """
        palavras = cargo.lower().split()
        # Remove palavras muito comuns que podem dar falso positivo
        palavras_comuns = ['de', 'da', 'do', 'e', 'para', 'com', 'um', 'uma']
        palavras_filtradas = [p for p in palavras if p not in palavras_comuns and len(p) > 2]
        return palavras_filtradas
    
    def vaga_contem_palavras_chave(self, texto_vaga, palavras_chave):
        """
        Verifica se o texto da vaga contém as palavras-chave
        Retorna quantas palavras encontrou e quais foram
        """
        texto_lower = texto_vaga.lower()
        palavras_encontradas = []
        
        for palavra in palavras_chave:
            if palavra in texto_lower:
                palavras_encontradas.append(palavra)
        
        return palavras_encontradas
    
    def extrair_vagas_do_html(self, html, cargo_original):
        """
        PASSO 2: Extrai vagas do HTML e verifica se contêm as palavras-chave
        """
        vagas_encontradas = []
        palavras_chave = self.extrair_palavras_chave(cargo_original)
        
        # ESTRATÉGIA 1: Buscar JSON embutido no LinkedIn
        # Procura padrão de jobPosting no HTML
        padrao_jobs = r'{"jobPosting"[^}]+"title":"([^"]+)"[^}]+"companyName":"([^"]+)"[^}]+"formattedLocation":"([^"]+)"[^}]+"url":"([^"]+)"'
        
        matches = re.findall(padrao_jobs, html, re.IGNORECASE)
        
        if matches:
            print(f"        Encontrados {len(matches)} jobs no JSON")
            
            for match in matches[:config.LIMITE_VAGAS]:
                titulo = match[0] if len(match) > 0 else ""
                empresa = match[1] if len(match) > 1 else ""
                local = match[2] if len(match) > 2 else ""
                link = match[3] if len(match) > 3 else ""
                
                # Limpa caracteres especiais
                titulo = titulo.replace('\\u0026', '&').replace('\\u00e7', 'ç').replace('\\u00e1', 'á')
                
                # VERIFICA PALAVRAS-CHAVE NO TÍTULO
                palavras_titulo = self.vaga_contem_palavras_chave(titulo, palavras_chave)
                
                # Só adiciona se tiver pelo menos 1 palavra-chave
                if palavras_titulo:
                    vaga = {
                        "titulo": titulo[:100],
                        "empresa": empresa[:60],
                        "local": local[:60] if local else "Brasil",
                        "link": link if link.startswith('http') else f"https://www.linkedin.com{link}",
                        "site": "LinkedIn",
                        "cargo_buscado": cargo_original,
                        "palavras_encontradas": f"[{', '.join(palavras_titulo[:3])}]",
                        "score": len(palavras_titulo)
                    }
                    vagas_encontradas.append(vaga)
        
        # ESTRATÉGIA 2: Se não encontrou JSON, busca elementos HTML
        if not vagas_encontradas:
            vagas_encontradas = self._extrair_por_html(html, cargo_original, palavras_chave)
        
        # Ordena por relevância (mais palavras-chave primeiro)
        vagas_encontradas.sort(key=lambda x: x.get('score', 0), reverse=True)
        
        return vagas_encontradas
    
    def _extrair_por_html(self, html, cargo_original, palavras_chave):
        """Extrai vagas do HTML estruturado"""
        vagas = []
        
        # Padrões para encontrar cards de vagas
        card_patterns = [
            r'<div[^>]*class="[^"]*job-card[^"]*"[^>]*>(.*?)</div>\s*</div>\s*</div>',
            r'<li[^>]*class="[^"]*jobs-search__result[^"]*"[^>]*>(.*?)</li>',
            r'<div[^>]*data-job-id="[^"]+"[^>]*>(.*?)</div>\s*</div>'
        ]
        
        for pattern in card_patterns:
            cards = re.findall(pattern, html, re.DOTALL)
            
            for card in cards[:config.LIMITE_VAGAS]:
                # Extrai título
                titulo_match = re.search(r'<h[1-3][^>]*>([^<]+)</h[1-3]>', card, re.IGNORECASE)
                titulo = titulo_match.group(1).strip() if titulo_match else ""
                
                # Extrai empresa
                empresa_match = re.search(r'<h4[^>]*>([^<]+)</h4>', card, re.IGNORECASE)
                empresa = empresa_match.group(1).strip() if empresa_match else ""
                
                # Extrai link
                link_match = re.search(r'href="([^"]*\/jobs\/[^"]+)"', card)
                link = link_match.group(1) if link_match else ""
                
                if titulo and empresa:
                    # Verifica palavras-chave
                    palavras_encontradas = self.vaga_contem_palavras_chave(titulo, palavras_chave)
                    
                    if palavras_encontradas:
                        vaga = {
                            "titulo": titulo[:100],
                            "empresa": empresa[:60],
                            "local": "Brasil",
                            "link": link if link.startswith('http') else f"https://www.linkedin.com{link}",
                            "site": "LinkedIn",
                            "cargo_buscado": cargo_original,
                            "palavras_encontradas": f"[{', '.join(palavras_encontradas[:3])}]",
                            "score": len(palavras_encontradas)
                        }
                        vagas.append(vaga)
            
            if vagas:
                break
        
        return vagas
    
    def _gerar_link_busca_garantido(self, cargo):
        """Fallback: gera link de busca com todas as palavras-chave"""
        cargo_url = cargo.replace(' ', '%20')
        
        url_busca = f"https://www.linkedin.com/jobs/search/?keywords={cargo_url}&location=Brasil"
        
        if config.TIPO_TRABALHO and config.TIPO_TRABALHO in config.TIPO_TRABALHO_MAP:
            url_busca += f"&f_WT={config.TIPO_TRABALHO_MAP[config.TIPO_TRABALHO]}"
        
        palavras = self.extrair_palavras_chave(cargo)
        
        vaga = {
            "titulo": f"🔍 BUSCA: {cargo}",
            "empresa": "LinkedIn",
            "local": "Clique para ver vagas",
            "link": url_busca,
            "site": "LinkedIn",
            "cargo_buscado": cargo,
            "palavras_encontradas": f"[{', '.join(palavras[:4])}]",
            "score": len(palavras),
            "tipo": "link_busca"
        }
        
        return [vaga]
    
    def buscar(self, cargo):
        """
        Busca principal - prioriza extração real, fallback para links
        """
        print(f"        🔎 Buscando: {cargo}")
        
        # PASSO 1: Monta URL com as palavras-chave
        url = self.montar_url_com_palavras_chave(cargo)
        print(f"        📍 URL: {url[:100]}...")
        
        try:
            resposta = requests.get(url, headers=self.headers, timeout=20)
            
            if resposta.status_code == 200:
                # PASSO 2: Extrai e filtra por palavras-chave no HTML
                vagas = self.extrair_vagas_do_html(resposta.text, cargo)
                
                if vagas:
                    # Mostra quantas vagas encontrou e a melhor
                    print(f"        ✅ {len(vagas)} vagas encontradas")
                    melhor_vaga = vagas[0]
                    print(f"           Ex: {melhor_vaga['titulo'][:60]}...")
                    print(f"           Palavras: {melhor_vaga['palavras_encontradas']}")
                    return vagas
                else:
                    print(f"        ⚠️ Nenhuma vaga com palavras-chave encontrada")
                    print(f"        🔗 Usando link de busca garantido")
                    return self._gerar_link_busca_garantido(cargo)
            else:
                print(f"        ⚠️ Erro HTTP {resposta.status_code}")
                return self._gerar_link_busca_garantido(cargo)
                
        except Exception as e:
            print(f"        ❌ Erro: {str(e)[:50]}")
            return self._gerar_link_busca_garantido(cargo)

def buscar_vagas_linkedin(cargos):
    """Função principal que coordena a busca"""
    scraper = LinkedInScraper()
    todas_vagas = []
    
    print(f"\n  🌐 LinkedIn - Buscando {len(cargos)} cargos:")
    print("  " + "-" * 50)
    
    for i, cargo in enumerate(cargos, 1):
        print(f"\n    [{i}/{len(cargos)}] {cargo}")
        vagas = scraper.buscar(cargo)
        todas_vagas.extend(vagas)
        time.sleep(3)  # Delay entre cargos
    
    return todas_vagas
