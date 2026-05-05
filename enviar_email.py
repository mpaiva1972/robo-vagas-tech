import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import config  # ← IMPORTANTE: importa o config.py

# ============================================
# CONFIGURAÇÕES DE E-MAIL (VOCÊ MUDA AQUI)
# ============================================
SEU_EMAIL = "paiva.consult@gmail.com"  # ← MUDE PARA SEU E-MAIL
SENHA_APP_GMAIL = "vvar oeao difv jgqg"  # ← COLE A SENHA DO APP
EMAIL_DESTINO = "paiva.consult@gmail.com"  # ← PARA ONDE ENVIAR

def formatar_email_html(vagas):
    """Cria e-mail mostrando as palavras-chave encontradas"""
    
    if not vagas:
        return f"""
        <html>
        <body>
            <h2>🔍 Relatório de Busca - {datetime.now().strftime('%d/%m/%Y')}</h2>
            <p>Nenhuma vaga encontrada com os filtros selecionados.</p>
            <hr>
            <p><b>Filtros aplicados:</b></p>
            <ul>
                <li>Tipo de trabalho: {config.TIPO_TRABALHO or 'Qualquer'}</li>
                <li>Nível: {config.NIVEL_EXPERIENCIA or 'Qualquer'}</li>
            </ul>
        </body>
        </html>
        """
    
    # Separa links de busca de vagas reais
    vagas_reais = [v for v in vagas if v.get('tipo') != 'link_busca']
    links_busca = [v for v in vagas if v.get('tipo') == 'link_busca']
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial; max-width: 800px; margin: auto; padding: 20px; }}
            .header {{ background: #0073b1; color: white; padding: 20px; text-align: center; border-radius: 10px; }}
            .vaga-real {{ background: #e8f5e9; border-left: 4px solid #4caf50; padding: 10px; margin: 10px 0; }}
            .link-busca {{ background: #fff3e0; border-left: 4px solid #ff9800; padding: 10px; margin: 10px 0; }}
            .palavras {{ color: #666; font-size: 12px; font-family: monospace; }}
            .titulo {{ font-size: 16px; font-weight: bold; }}
            .link {{ margin-top: 5px; }}
            .badge {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; }}
            .badge-real {{ background: #4caf50; color: white; }}
            .badge-link {{ background: #ff9800; color: white; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h2>🤖 VAGAS ENCONTRADAS</h2>
            <p>{datetime.now().strftime('%d/%m/%Y às %H:%M')}</p>
        </div>
    """
    
    if vagas_reais:
        html += f"""
        <h3>✅ VAGAS REAIS ENCONTRADAS ({len(vagas_reais)})</h3>
        """
        for vaga in vagas_reais[:20]:
            html += f"""
            <div class="vaga-real">
                <div class="titulo">📌 {vaga['titulo']}</div>
                <div>🏢 {vaga['empresa']} | 📍 {vaga['local']}</div>
                <div class="palavras">🔤 Palavras-chave encontradas: {vaga.get('palavras_encontradas', 'N/A')}</div>
                <div class="link">🔗 <a href="{vaga['link']}">Candidatar-se</a></div>
            </div>
            """
    
    if links_busca:
        html += f"""
        <h3>🔍 LINKS DE BUSCA ({len(links_busca)})</h3>
        <p>Clique nos links abaixo para ver as vagas diretamente no LinkedIn:</p>
        """
        for link in links_busca[:10]:
            html += f"""
            <div class="link-busca">
                <div class="titulo">🎯 {link['titulo']}</div>
                <div class="palavras">🔤 Buscando por: {link.get('palavras_encontradas', 'N/A')}</div>
                <div class="link">🔗 <a href="{link['link']}" target="_blank">Buscar no LinkedIn</a></div>
            </div>
            """
    
    html += f"""
        <hr>
        <div style="background: #f5f5f5; padding: 15px; border-radius: 8px; margin-top: 20px;">
            <p><b>📊 RESUMO:</b></p>
            <ul>
                <li>Vagas reais extraídas: {len(vagas_reais)}</li>
                <li>Links de busca gerados: {len(links_busca)}</li>
                <li>Total: {len(vagas)}</li>
            </ul>
            <p><b>🎯 FILTROS ATIVOS:</b><br>
            • Tipo de trabalho: {config.TIPO_TRABALHO or 'Qualquer'}<br>
            • Nível: {config.NIVEL_EXPERIENCIA or 'Qualquer'}</p>
        </div>
        <p style="text-align: center; font-size: 12px; color: #888; margin-top: 20px;">
            🤖 Robô de Vagas | Busca por palavras-chave na URL e no HTML
        </p>
    </body>
    </html>
    """
    
    return html

def enviar_relatorio(vagas):
    """Envia o relatório por e-mail"""
    
    if not vagas:
        assunto = f"📭 Nenhuma vaga - {datetime.now().strftime('%d/%m')}"
    else:
        vagas_reais = len([v for v in vagas if v.get('tipo') != 'link_busca'])
        links = len([v for v in vagas if v.get('tipo') == 'link_busca'])
        assunto = f"🎯 {vagas_reais} vagas + {links} links - {datetime.now().strftime('%d/%m')}"
    
    html_content = formatar_email_html(vagas)
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = assunto
    msg['From'] = SEU_EMAIL
    msg['To'] = EMAIL_DESTINO
    
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SEU_EMAIL, SENHA_APP_GMAIL)
        server.send_message(msg)
        server.quit()
        print(f"✅ E-mail enviado!")
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False
