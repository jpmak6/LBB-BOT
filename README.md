# 🤖 Bot Discord LBB - V2 Complète

Bot Discord ultra-simple et professionnel pour PME de 80 personnes avec système de tickets avancé, panel admin et hébergement 24/7.

## ✨ Fonctionnalités V2

### 🎫 **Système de Tickets Avancé**
- 2 panneaux séparés : **Demandes/Problèmes** et **Maintenances**
- Workflow complet : Fermer → Confirmation → Transcrire/Réouvrir/Supprimer
- Transcripts automatiques avec historique complet
- Boutons persistants (fonctionnent après redémarrage)

### 🔐 **Panel Admin Ultra-Sécurisé**
- Whitelist stricte par ID Discord
- 6 fonctions : Sondage, Kick, Ban, Timeout, Clear, Panneaux tickets
- Interface intuitive avec boutons

### 📊 **Communication**
- Système de sondages avec réactions automatiques
- Modération complète (kick, ban, timeout)

### 🌐 **Hébergement 24/7**
- Compatible Replit + UptimeRobot
- Serveur Flask intégré pour keep-alive
- 4 endpoints : `/`, `/ping`, `/status`, `/health`

---

## 📋 Commandes disponibles

### Tickets
- `!setup_demande` - Créer le panneau Demandes/Problèmes
- `!setup_maintenance` - Créer le panneau Maintenance

### Admin (Whitelist uniquement)
- `!panel_admin` - Afficher le panel admin complet
- `!pollcreate` - Créer un sondage (admin)

### Modération
- Via panel admin (boutons interactifs)

---

## 🚀 Installation & Hébergement

### 📖 **Guide complet Replit + UptimeRobot**
👉 **Lis le guide détaillé** : [`HEBERGEMENT_REPLIT.md`](HEBERGEMENT_REPLIT.md)

### ⚡ **Installation rapide (local)**

1. **Cloner le projet**
```bash
git clone https://github.com/jpmak6/LBB-BOT.git
cd "LBB BOT"
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Configurer le token**
Crée un fichier `.env` :
```env
DISCORD_TOKEN=ton_token_discord_ici
```

4. **Lancer le bot**
```bash
python bot.py
```

---

## 🌐 Hébergement Replit (Gratuit 24/7)
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```

4. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

5. **Configurer le token**
Créez un fichier `.env` avec:
```
DISCORD_TOKEN=votre_token_ici
```

6. **Lancer le bot**
```bash
python bot.py
```

## ☁️ Hébergement en ligne

### Option 1: Railway (Recommandé - Gratuit)

1. Créez un compte sur [Railway.app](https://railway.app)
2. Connectez votre dépôt GitHub
3. Ajoutez la variable d'environnement `DISCORD_TOKEN`
4. Railway détectera automatiquement le projet Python
5. Le bot se lancera automatiquement !

### Option 2: Heroku

1. Créez un compte sur [Heroku](https://heroku.com)
2. Installez Heroku CLI
3. Commandes:
```bash
heroku login
heroku create nom-de-votre-bot
heroku config:set DISCORD_TOKEN=votre_token
git push heroku main
```

### Option 3: Replit

1. Importez le projet sur [Replit](https://replit.com)
2. Ajoutez `DISCORD_TOKEN` dans les Secrets
3. Décommentez `keep_alive()` dans bot.py
4. Utilisez UptimeRobot pour le garder actif

## 🔒 Sécurité

- ✅ Token stocké dans `.env` (jamais dans le code)
- ✅ `.gitignore` configuré pour protéger les fichiers sensibles
- ✅ Logging des erreurs
- ✅ Gestion des permissions

## 📝 Logs

Les logs sont enregistrés dans `bot.log` et affichés dans la console.

## 🤝 Contribution

N'hésitez pas à améliorer le bot!

## 📄 License

MIT License

## 💡 Support

En cas de problème, vérifiez:
1. Que le token est correct dans `.env`
2. Que les intents sont activés sur le Discord Developer Portal
3. Que les dépendances sont installées
4. Les logs dans `bot.log`

---

Fait avec ❤️ pour la communauté Discord
