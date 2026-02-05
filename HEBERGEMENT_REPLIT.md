# 🚀 GUIDE HÉBERGEMENT REPLIT + UPTIMEROBOT

## 📋 ÉTAPE 1 : PRÉPARER REPLIT

### 1.1 Créer un nouveau Repl
1. Va sur https://replit.com
2. Clique sur **"+ Create Repl"**
3. **Template** : Python
4. **Title** : `LBB-BOT-Discord`
5. Clique sur **"Create Repl"**

### 1.2 Importer les fichiers
**Option A - Via GitHub (RECOMMANDÉ) :**
1. Dans Replit, clique sur l'icône GitHub (à gauche)
2. Clique sur **"Import from GitHub"**
3. Colle l'URL : `https://github.com/jpmak6/LBB-BOT.git`
4. Clique sur **"Import"**
5. ✅ Tous les fichiers sont automatiquement importés !

**Option B - Upload manuel :**
1. Glisse-dépose tous les fichiers du projet dans Replit
2. Vérifie que tu as bien :
   - `bot.py`
   - `keep_alive.py`
   - `requirements.txt`
   - `.env`
   - Dossier `cogs/`

### 1.3 Configurer les variables d'environnement (SECRETS)
1. Dans Replit, clique sur l'icône **🔒 Secrets** (cadenas, à gauche)
2. Ajoute un secret :
   - **Key** : `DISCORD_TOKEN`
   - **Value** : Ton token Discord (celui dans `.env`)
3. Clique sur **"Add secret"**

⚠️ **IMPORTANT** : Supprime le fichier `.env` de Replit après avoir créé le Secret !

---

## 📦 ÉTAPE 2 : INSTALLER LES DÉPENDANCES

### 2.1 Vérifier requirements.txt
Dans Replit, ouvre `requirements.txt` et vérifie que tu as :
```
discord.py>=2.4.0
python-dotenv==1.0.0
Flask==3.0.0
```

### 2.2 Installer
Replit installe automatiquement les dépendances au premier lancement.
Si besoin, tu peux forcer l'installation dans le **Shell** :
```bash
pip install -r requirements.txt
```

---

## 🚀 ÉTAPE 3 : LANCER LE BOT

### 3.1 Premier lancement
1. Clique sur le bouton **▶️ Run** (en haut)
2. Tu devrais voir dans la console :
   ```
   🌐 Mode Replit détecté - Activation du keep-alive
   ✅ Serveur keep-alive démarré
   🚀 Démarrage du bot...
   ✅ Connecté en tant que LBB BOT#1402
   ```

### 3.2 Obtenir l'URL du Repl
1. Une fois le bot lancé, tu verras une fenêtre **"Webview"** s'ouvrir
2. En haut de cette fenêtre, clique sur **"Open in new tab"** 🗗
3. Copie l'URL complète, exemple :
   ```
   https://lbb-bot-discord.votreusername.repl.co
   ```
4. **SAUVEGARDE CETTE URL** - Tu en auras besoin pour UptimeRobot !

### 3.3 Tester le serveur web
Ajoute `/ping` à la fin de ton URL et ouvre-la dans un navigateur :
```
https://lbb-bot-discord.votreusername.repl.co/ping
```

Tu devrais voir : `pong`

✅ Si tu vois "pong", le serveur fonctionne parfaitement !

---

## ⏰ ÉTAPE 4 : CONFIGURER UPTIMEROBOT

### 4.1 Créer un compte (GRATUIT)
1. Va sur https://uptimerobot.com
2. Clique sur **"Sign Up"** (inscription gratuite)
3. Vérifie ton email et connecte-toi

### 4.2 Ajouter un nouveau monitor
1. Une fois connecté, clique sur **"+ Add New Monitor"**
2. Remplis les informations :

**Monitor Type** : `HTTP(s)`

**Friendly Name** : `LBB BOT Discord`

**URL (or IP)** : Colle ton URL Replit avec `/ping` à la fin
```
https://lbb-bot-discord.votreusername.repl.co/ping
```

**Monitoring Interval** : `5 minutes` (gratuit, suffisant)

**Monitor Timeout** : `30 seconds`

**Alert Contacts** : Ton email (pour être notifié si le bot tombe)

3. Clique sur **"Create Monitor"**

### 4.3 Vérifier que ça marche
1. Attends 5 minutes
2. Sur UptimeRobot, tu devrais voir :
   - **Status** : ✅ Up (vert)
   - **Uptime** : 100%
   - **Response Time** : ~200-500ms

✅ **C'EST FAIT !** Ton bot restera actif 24/7 ! 🎉

---

## 🔍 ÉTAPE 5 : DÉPANNAGE

### Problème 1 : "Module 'keep_alive' not found"
**Solution** :
- Vérifie que `keep_alive.py` est bien dans le dossier racine de Replit
- Vérifie que Flask est installé : `pip install Flask`

### Problème 2 : "Token invalide"
**Solution** :
- Va dans **Secrets** (🔒) dans Replit
- Vérifie que `DISCORD_TOKEN` contient bien ton token Discord
- Pas d'espaces avant/après le token

### Problème 3 : Le bot se déconnecte après quelques heures
**Solution** :
- Vérifie que UptimeRobot ping bien toutes les 5 minutes
- Dans UptimeRobot, regarde les **logs** pour voir si les pings fonctionnent
- Assure-toi que l'URL dans UptimeRobot se termine par `/ping`

### Problème 4 : "Replit says resource limits exceeded"
**Solution** :
- Tu as dépassé les limites gratuites de Replit
- **Option A** : Passe à Replit Hacker (payant, 7$/mois)
- **Option B** : Utilise un autre hébergeur (Railway, Heroku, AWS Free Tier)

### Problème 5 : Le serveur web ne démarre pas
**Solution** :
```bash
# Dans le Shell Replit, vérifie les logs :
python bot.py

# Si erreur Flask, réinstalle :
pip uninstall Flask
pip install Flask==3.0.0
```

---

## 📊 ÉTAPE 6 : MONITORING AVANCÉ (OPTIONNEL)

### 6.1 Endpoints disponibles

**Page d'accueil (belle interface)** :
```
https://ton-repl.repl.co/
```

**Status JSON (pour monitoring)** :
```
https://ton-repl.repl.co/status
```

**Ping rapide (pour UptimeRobot)** :
```
https://ton-repl.repl.co/ping
```

**Health check** :
```
https://ton-repl.repl.co/health
```

### 6.2 Ajouter plusieurs monitors UptimeRobot
Pour plus de sécurité, crée 2 monitors :

**Monitor 1** : `/ping` (check toutes les 5 minutes)
**Monitor 2** : `/status` (check toutes les 15 minutes)

---

## ✅ CHECKLIST FINALE

Avant de tout laisser tourner, vérifie :

- [ ] Bot se lance sans erreur dans Replit
- [ ] Console affiche : "✅ Connecté en tant que LBB BOT"
- [ ] Console affiche : "✅ Serveur keep-alive démarré"
- [ ] L'URL du Repl fonctionne (affiche la page HTML)
- [ ] `/ping` retourne "pong"
- [ ] UptimeRobot est configuré avec l'URL `/ping`
- [ ] UptimeRobot affiche "Up" en vert
- [ ] Le bot répond aux commandes Discord (`!setup_demande`)

**Si tous les points sont cochés : FÉLICITATIONS ! 🎉**

Ton bot Discord est maintenant hébergé 24/7 gratuitement ! 🚀

---

## 💡 CONSEILS PRO

1. **Surveille ton uptime** : Connecte-toi à UptimeRobot 1x/semaine pour vérifier
2. **Backup régulier** : Push sur GitHub chaque modification (`git push`)
3. **Logs** : Dans Replit, vérifie les logs si le bot bug
4. **Optimisation** : Replit gratuit = 500MB RAM max, garde ton code léger
5. **Alternatives** : Si Replit devient payant, migre vers Railway ou Render

---

## 🆘 BESOIN D'AIDE ?

- **Replit Doc** : https://docs.replit.com
- **UptimeRobot Doc** : https://uptimerobot.com/help/
- **Discord.py Doc** : https://discordpy.readthedocs.io

**Support GitHub** : Ouvre une issue sur https://github.com/jpmak6/LBB-BOT

---

**BON HÉBERGEMENT ! 🚀**
