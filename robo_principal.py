"""
ROBÔ PRINCIPAL - Orquestra todos os sites
Versão fracionada por componentes
"""

from config import *
from sites.linkedin import buscar_vagas_linkedin
from enviar_email import enviar_relatorio
from datetime import datetime

def mostrar_configuracoes():
    """Mostra as configurações atuais antes de buscar"""
    print("\n" + "=" * 60)
    print("📋 CONFIGURAÇÕES ATUAIS")
    print("=" * 60)
    print(f"   Cargos: {len(CARGOS)}")
    for cargo in CARGOS:
        print(f"     • {cargo}")
    print(f"\n   Tipo de trabalho: {TIPO_TRABALHO or 'Qualquer'}")
    print(f"   Nível: {NIVEL_EXPERIENCIA or 'Qualquer'}")
    print("=" * 60)

def buscar_em_todos_sites():
    """Busca vagas em todos os sites ativos"""
    todas_vagas = []
    
    # LinkedIn
    if SITES_ATIVOS.get("linkedin", False):
        vagas_linkedin = buscar_vagas_linkedin(config, CARGOS)
        todas_vagas.extend(vagas_linkedin)
        print(f"\n  📊 LinkedIn: {len(vagas_linkedin)} vagas encontradas")
    
    # Futuros sites serão adicionados aqui:
    # if SITES_ATIVOS.get("indeed", False):
    #     from sites.indeed import buscar_vagas_indeed
    #     vagas_indeed = buscar_vagas_indeed(config, CARGOS)
    #     todas_vagas.extend(vagas_indeed)
    
    return todas_vagas

def formatar_resumo(vagas):
    """Gera um resumo para mostrar no console"""
    if not vagas:
        return "  ⚠️ Nenhuma vaga encontrada"
    
    resumo = f"\n  📈 Total: {len(vagas)} vagas\n"
    por_site = {}
    for vaga in vagas:
        site = vaga['site']
        por_site[site] = por_site.get(site, 0) + 1
    
    for site, qtd in por_site.items():
        executivas = sum(1 for v in vagas if v['site'] == site and v.get('score_executivo'))
        resumo += f"\n     • {site}: {qtd} vagas"
        if executivas:
            resumo += f" (⭐ {executivas} executivas)"
    
    return resumo

def main():
    print("\n" + "🤖" * 30)
    print("ROBÔ DE VAGAS EXECUTIVAS - LINKEDIN")
    print(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("🤖" * 30)
    
    # Mostra as configurações atuais
    mostrar_configuracoes()
    
    # Busca as vagas
    print("\n🔍 Iniciando busca...")
    vagas_encontradas = buscar_em_todos_sites()
    
    # Mostra resumo
    print(formatar_resumo(vagas_encontradas))
    
    # Envia e-mail
    print("\n📧 Enviando relatório...")
    enviar_relatorio(vagas_encontradas)
    
    print("\n" + "✅" * 20)
    print("ROBÔ FINALIZADO COM SUCESSO!")
    print("✅" * 20)

if __name__ == "__main__":
    main()
