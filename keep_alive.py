from flask import Flask
from threading import Thread
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "🤖 Bot Discord en ligne et fonctionnel!"

@app.route('/status')
def status():
    return {
        "status": "online",
        "message": "Le bot Discord est actif"
    }

def run():
    """Lance le serveur Flask sur le port spécifié"""
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    """Lance le serveur dans un thread séparé pour garder le bot en ligne"""
    server = Thread(target=run)
    server.daemon = True
    server.start()
    print("✅ Serveur keep-alive démarré")
