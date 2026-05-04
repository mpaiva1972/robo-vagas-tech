import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# ============================================
# CONFIGURAÇÕES DE E-MAIL (VOCÊ MUDA AQUI)
# ============================================
SEU_EMAIL = "seuemail@gmail.com"  # ← MUDE PARA SEU E-MAIL
SENHA_APP_GMAIL = ""  # ← COLE A SENHA DO APP
EMAIL_DESTINO = "seuemail@gmail.com"  # ← PARA ONDE ENVIAR

def formatar_email_html(vagas):
    """Cria um e-mail bonito com as vagas encontradas"""
    
    if not vagas:
        return f"""
        <html>
        <body style="font-family: Arial;">
            <h2>🔍 RELATÓRIO DE VAGAS - {datetime.now().strftime('%d/%m/%Y')}</h2>
            <p>Nenhuma vaga foi encontrada hoje com os filtros selecionados.</p>
            <hr>
            <p><b>Filtros atuais:</b> {config.TIPO_TRABALHO or 'Qualquer tipo'} | {config.NIVEL_EXPERIENCIA or 'Qualquer nível'}</p>
            <p>💡 Dica: Tente ajustar os critérios no arquivo <b>config.py</b></p>
        </body>
        </html>
        """
    
    # Agrupa vagas por site
    por_site = {}
    for vaga in vagas:
        site = vaga.get('site', 'Outros')
        if site not in por_site:
            por_site[site] = []
        por_site[site].append(vaga)
    
    # Conta vagas executivas
    executivas = [v for v in vagas if v.get('score_executivo')]
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 800px; margin: auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #0073b1 0%, #005582 100%); color: white; padding: 20px; text-align: center; border-radius: 10px; }}
            .stats {{ background: #f5f5f5; padding: 15px; border-radius: 8px; margin: 20px 0; text-align: center; }}
            .stats-number {{ font-size: 24px; font-weight: bold; color: #0073b1; }}
            .site-block {{ margin: 20px 0; border: 1px solid #ddd; border-radius: 8px; overflow: hidden; }}
            .site-title {{ background: #f9f9f9; padding: 12px 15px; font-size: 18px; font-weight: bold; border-bottom: 2px solid #0073b1; }}
            .vaga {{ padding: 12px 15px; border-bottom: 1px solid #eee; }}
            .vaga:last-child {{ border-bottom: none; }}
            .titulo {{ font-size: 16px; font-weight: bold; color: #333; }}
            .executivo {{ background: #e8f5e9; padding: 2px 8px; border-radius: 12px; font-size: 11px; margin-left: 8px; }}
            .empresa {{ color: #666; margin: 5px 0; }}
            .local {{ color: #888; font-size: 13px; }}
            .link {{ margin-top: 5px; }}
            .link a {{ color: #0073b1; text-decoration: none; font-weight: bold; }}
            .footer {{ text-align: center; margin-top: 30px; padding: 15px; background: #f9f9f9; border-radius: 8px; font-size: 12px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h2>🤖 AGENTE DE VAGAS</h2>
            <p>Relatório de vagas executivas</p>
            <p style="font-size: 14px;">{datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}</p>
        </div>
        
        <div class="stats">
            <span class="stats-number">{len(vagas)}</span> vagas encontradas
            {' | ⭐ ' + str(len(executivas)) + ' vagas executivas' if executivas else ''}
        </div>
    """
    
    for site, vagas_site in por_site.items():
        html += f"""
        <div class="site-block">
            <div class="site-title">
                🌐 {site.upper()} ({len(vagas_site)} vagas)
            </div>
        """
        for vaga in vagas_site:
            exec_badge = f'<span class="executivo">⭐ Executiva</span>' if vaga.get('score_executivo') else ''
            html += f"""
            <div class="vaga">
                <div class="titulo">
                    📌 {vaga['titulo']}
                    {exec_badge}
                </div>
                <div class="empresa">🏢 {vaga['empresa']}</div>
                <div class="local">📍 {vaga['local']}</div>
                <div class="link">🔗 <a href="{vaga['link']}" target="_blank">Clique para se candidatar</a></div>
            </div>
            """
        html += "</div>"
    
    html += f"""
        <div class="footer">
            <p>🤖 Robô de Vagas Automático | Executado diariamente às 6h</p>
            <p>💡 Filtros ativos: {config.TIPO_TRABALHO or 'Qualquer tipo'} | {config.NIVEL_EXPERIENCIA or 'Qualquer nível'}</p>
            <p>🔧 Para ajustar os filtros, edite o arquivo <b>config.py</b></p>
        </div>
    </body>
    </html>
    """
    
    return html

def enviar_relatorio(vagas):
    """Envia o relatório por e-mail"""
    
    if not vagas:
        assunto = f"📭 VAGAS - Nenhuma encontrada - {datetime.now().strftime('%d/%m')}"
    else:
        assunto = f"🎯 {len(vagas)} vagas de tecnologia - {datetime.now().strftime('%d/%m')}"
    
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
        
        print(f"✅ E-mail enviado para {EMAIL_DESTINO}")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao enviar e-mail: {e}")
        print("\nVerifique a SENHA_APP_GMAIL no arquivo enviar_email.py")
        return False

# Import config para usar no email (para mostrar filtros)
import config
