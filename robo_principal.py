from buscar_vagas import buscar_todas_vagas
from enviar_email import enviar_relatorio
from datetime import datetime

def main():
    print("=" * 60)
    print("🤖 ROBÔ DE VAGAS DE TECNOLOGIA")
    print(f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 60)
    
    # Passo 1: Buscar as vagas
    print("\n🔍 Iniciando busca de vagas...")
    vagas_encontradas = buscar_todas_vagas()
    
    print("\n" + "=" * 60)
    print(f"📊 RESULTADO FINAL: {len(vagas_encontradas)} vagas encontradas")
    print("=" * 60)
    
    # Passo 2: Mostrar resumo por site
    if vagas_encontradas:
        sites_count = {}
        for vaga in vagas_encontradas:
            site = vaga['site']
            sites_count[site] = sites_count.get(site, 0) + 1
        
        print("\n📈 Vagas por site:")
        for site, qtd in sites_count.items():
            print(f"   • {site}: {qtd} vagas")
    
    # Passo 3: Enviar e-mail
    print("\n📧 Enviando relatório por e-mail...")
    enviar_relatorio(vagas_encontradas)
    
    print("\n🏁 Robô finalizado com sucesso!")

if __name__ == "__main__":
    main()
