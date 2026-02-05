from flask import Flask, jsonify
from threading import Thread
import os
from datetime import datetime
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('keep_alive')

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Variable globale pour stocker le statut du bot
bot_start_time = datetime.now()

@app.route('/')
def home():
    """Page d'accueil - Confirme que le bot est en ligne"""
    uptime = datetime.now() - bot_start_time
    hours, remainder = divmod(int(uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>LBB BOT - Status</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                text-align: center;
                padding: 50px;
                margin: 0;
            }}
            .container {{
                background: rgba(255,255,255,0.1);
                backdrop-filter: blur(10px);
                border-radius: 20px;
                padding: 40px;
                max-width: 600px;
                margin: 0 auto;
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            }}
            h1 {{ font-size: 3em; margin: 0; }}
            .status {{ 
                background: #00ff00;
                color: #000;
                padding: 10px 20px;
                border-radius: 25px;
                display: inline-block;
                margin: 20px 0;
                font-weight: bold;
            }}
            .uptime {{
                font-size: 1.5em;
                margin: 20px 0;
            }}
            .info {{
                background: rgba(255,255,255,0.2);
                padding: 20px;
                border-radius: 10px;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 LBB BOT</h1>
            <div class="status">● EN LIGNE</div>
            <div class="uptime">
                ⏱️ Uptime: {hours}h {minutes}m {seconds}s
            </div>
            <div class="info">
                <p>✅ Bot Discord opérationnel</p>
                <p>🔄 Actualisé: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
                <p>🌐 Serveur Flask actif sur port {os.environ.get('PORT', 8080)}</p>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/status')
def status():
    """Endpoint JSON pour UptimeRobot - Rapide et léger"""
    uptime_seconds = int((datetime.now() - bot_start_time).total_seconds())
    
    return jsonify({
        "status": "online",
        "uptime_seconds": uptime_seconds,
        "timestamp": datetime.now().isoformat(),
        "message": "Bot Discord LBB actif et fonctionnel"
    })

@app.route('/ping')
def ping():
    """Endpoint ultra-rapide pour les pings"""
    return "pong", 200

@app.route('/health')
def health():
    """Health check pour monitoring"""
    return jsonify({
        "healthy": True,
        "uptime": int((datetime.now() - bot_start_time).total_seconds())
    })

def run():
    """Lance le serveur Flask sur le port spécifié par Replit"""
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"🚀 Démarrage du serveur Flask sur port {port}")
    
    # Désactiver les logs Flask pour éviter le spam
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,
        use_reloader=False
    )

def keep_alive():
    """
    Lance le serveur web dans un thread séparé
    Ce serveur permet à UptimeRobot de garder le bot actif 24/7
    """
    server = Thread(target=run)
    server.daemon = True
    server.start()
    logger.info("✅ Serveur keep-alive démarré - Bot prêt pour UptimeRobot")
    logger.info("📡 URL à configurer dans UptimeRobot: https://<votre-repl>.replit.dev/ping")
