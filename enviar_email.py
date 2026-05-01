import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# ============================================
# CONFIGURAÇÕES DE E-MAIL (VOCÊ MUDA AQUI)
# ============================================
SEU_EMAIL = "paiva.consult@gmail.com"  # ← MUDE PARA SEU E-MAIL
SENHA_APP_GMAIL = ""  # ← VAMOS CRIAR NO PASSO 4
EMAIL_DESTINO = "paiva.consult@gmail.com"  # ← PARA ONDE ENVIAR

def formatar_email_html(vagas):
    """Cria um e-mail bonito com as vagas"""
    
    if not vagas:
        return """
        <html>
        <body>
            <h2>🔍 Relatório de Vagas</h2>
            <p>Nenhuma vaga foi encontrada hoje com os filtros selecionados.</p>
            <p>Tente ajustar os critérios de busca no arquivo <b>config.py</b></p>
        </body>
        </html>
        """
    
    # Agrupa vagas por site
    por_site = {}
    for vaga in vagas:
        site = vaga['site']
        if site not in por_site:
            por_site[site] = []
        por_site[site].append(vaga)
    
    # Monta o HTML
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 800px; margin: auto; padding: 20px; }}
            .header {{ background: #4CAF50; color: white; padding: 20px; text-align: center; border-radius: 10px; }}
            .site-block {{ margin: 20px 0; border: 1px solid #ddd; border-radius: 8px; overflow: hidden; }}
            .site-title {{ background: #f5f5f5; padding: 10px 15px; font-size: 18px; font-weight: bold; border-bottom: 2px solid #4CAF50; }}
            .vaga {{ padding: 12px 15px; border-bottom: 1px solid #eee; }}
            .vaga:last-child {{ border-bottom: none; }}
            .titulo {{ font-size: 16px; font-weight: bold; color: #333; }}
            .empresa {{ color: #666; margin: 5px 0; }}
            .local {{ color: #888; font-size: 13px; }}
            .link {{ margin-top: 5px; }}
            .link a {{ color: #4CAF50; text-decoration: none; }}
            .footer {{ text-align: center; margin-top: 30px; padding: 15px; background: #f9f9f9; border-radius: 8px; font-size: 12px; }}
            .resumo {{ background: #e8f5e9; padding: 15px; border-radius: 8px; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h2>🤖 RELATÓRIO DE VAGAS DE TECNOLOGIA</h2>
            <p>{datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}</p>
        </div>
        
        <div class="resumo">
            <b>📊 RESUMO:</b> Total de {len(vagas)} vagas encontradas
        </div>
    """
    
    for site, vagas_site in por_site.items():
        html += f"""
        <div class="site-block">
            <div class="site-title">
                🌐 {site} ({len(vagas_site)} vagas)
            </div>
        """
        for vaga in vagas_site:
            html += f"""
            <div class="vaga">
                <div class="titulo">📌 {vaga['titulo']}</div>
                <div class="empresa">🏢 {vaga['empresa']}</div>
                <div class="local">📍 {vaga['local']}</div>
                <div class="link">🔗 <a href="{vaga['link']}" target="_blank">Clique para se candidatar</a></div>
            </div>
            """
        html += "</div>"
    
    html += """
        <div class="footer">
            <p>🤖 Robô de Vagas Automático | Executado diariamente às 6h</p>
            <p>💡 Configure seus filtros no arquivo <b>config.py</b></p>
        </div>
    </body>
    </html>
    """
    
    return html

def enviar_relatorio(vagas):
    """Envia o relatório por e-mail"""
    
    if not vagas:
        assunto = f"📭 Nenhuma vaga encontrada - {datetime.now().strftime('%d/%m')}"
    else:
        assunto = f"🎯 {len(vagas)} vagas de tecnologia - {datetime.now().strftime('%d/%m')}"
    
    html_content = formatar_email_html(vagas)
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = assunto
    msg['From'] = SEU_EMAIL
    msg['To'] = EMAIL_DESTINO
    
    # Anexa o HTML
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))
    
    try:
        # Conecta ao Gmail
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SEU_EMAIL, SENHA_APP_GMAIL)
        server.send_message(msg)
        server.quit()
        
        print(f"\n✅ E-mail enviado com sucesso para {EMAIL_DESTINO}")
        return True
        
    except Exception as e:
        print(f"\n❌ Erro ao enviar e-mail: {e}")
        print("\nVerifique se você configurou a SENHA_APP_GMAIL corretamente.")
        return False

if __name__ == "__main__":
    # Teste com vagas fictícias
    teste = [
        {
            "titulo": "Desenvolvedor Python (Teste)",
            "empresa": "Tech Company",
            "local": "Remoto",
            "link": "https://exemplo.com/vaga",
            "site": "LinkedIn",
            "cargo_buscado": "Python"
        }
    ]
    enviar_relatorio(teste)
