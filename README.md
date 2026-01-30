# 🤖 Bot Discord LBB

Bot Discord professionnel avec système de bienvenue, commandes d'administration et gestion d'erreurs.

## 🚀 Fonctionnalités

- ✅ Messages de bienvenue avec embeds élégants
- 📊 Commandes d'information (serveur, utilisateur, bot)
- 🛡️ Gestion des erreurs complète
- 📝 Système de logging
- 🎨 Embeds Discord professionnels
- 🧹 Commande de modération (clear)
- 🏓 Vérification de latence

## 📋 Commandes disponibles

### Informations
- `!aide` / `!help` - Menu d'aide
- `!regles` / `!rules` - Règles du serveur
- `!ping` - Latence du bot
- `!info` - Informations sur le bot

### Serveur
- `!serveurinfo` / `!si` - Informations du serveur
- `!userinfo [@user]` - Informations d'un membre

### Modération
- `!clear [nombre]` - Supprimer des messages (admin)

## 🛠️ Installation locale

### Prérequis
- Python 3.11+
- pip

### Étapes

1. **Cloner le projet**
```bash
git clone <votre-repo>
cd "LBB BOT"
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
```

3. **Activer l'environnement**
- Windows:
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
