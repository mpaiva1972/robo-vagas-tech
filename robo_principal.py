"""
ROBÔ PRINCIPAL - Orquestrador com filtro de TI
"""

from config import *
import sys
import os

# Adiciona o diretório atual para importações
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sites.linkedin import buscar_vagas_linkedin
from enviar_email import enviar_relatorio
from datetime import datetime

def mostrar_configuracoes():
    """Mostra as configurações atuais"""
    print("\n" + "=" * 60)
    print("📋 CONFIGURAÇÕES ATUAIS")
    print("=" * 60)
    print(f"   Cargos: {len(CARGOS)}")
    for cargo in CARGOS:
        print(f"     • {cargo}")
    print(f"\n   Tipo de trabalho: {TIPO_TRABALHO or 'Qualquer'}")
    print(f"   Nível: {NIVEL_EXPERIENCIA or 'Qualquer'}")
    print(f"   Apenas vagas de TI: {'Sim ✅' if APENAS_TI else 'Não'}")
    print("=" * 60)

def buscar_em_todos_sites():
    """Busca vagas em todos os sites ativos"""
    todas_vagas = []
    
    if SITES_ATIVOS.get("linkedin", False):
        print("\n  🌐 LinkedIn:")
        vagas_linkedin = buscar_vagas_linkedin(CARGOS)
        
        # Aplica filtro de TI se necessário
        if APENAS_TI:
            vagas_linkedin = [v for v in vagas_linkedin if v.get('score_executivo') == '⭐ TI']
        
        todas_vagas.extend(vagas_linkedin)
        print(f"\n  📊 LinkedIn: {len(vagas_linkedin)} vagas de TI encontradas")
    
    return todas_vagas

def mostrar_exemplos(vagas):
    """Mostra exemplos das vagas encontradas"""
    if vagas:
        print("\n  📌 EXEMPLOS DE VAGAS ENCONTRADAS:")
        for vaga in vagas[:5]:
            print(f"     • {vaga['titulo'][:60]}")
            print(f"       {vaga['empresa']} - {vaga['local']}")
            print()

def main():
    print("\n" + "🤖" * 30)
    print("ROBÔ DE VAGAS DE TI - LINKEDIN")
    print(f"📅 {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("🤖" * 30)
    
    mostrar_configuracoes()
    
    print("\n🔍 Iniciando busca...")
    vagas_encontradas = buscar_em_todos_sites()
    
    if vagas_encontradas:
        print(f"\n  ✅ TOTAL: {len(vagas_encontradas)} vagas de TI encontradas!")
        mostrar_exemplos(vagas_encontradas)
    else:
        print("\n  ⚠️ Nenhuma vaga de TI encontrada com os filtros atuais.")
        print("  💡 Dicas:")
        print("     • Verifique se os cargos estão escritos corretamente")
        print("     • Tente TIPO_TRABALHO = '' (remova o filtro)")
        print("     • Tente APENAS_TI = False para ver todas as vagas")
    
    print("\n📧 Enviando relatório...")
    enviar_relatorio(vagas_encontradas)
    
    print("\n" + "✅" * 20)
    print("ROBÔ FINALIZADO!")
    print("✅" * 20)

if __name__ == "__main__":
    main()
