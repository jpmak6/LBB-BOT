# 🎮 GUIDE HÉBERGEMENT FPS.MS / PTERODACTYL

## 🚀 HÉBERGEMENT SUR FPS.MS

### 📋 **Prérequis**
- Compte sur https://fps.ms
- Bot Discord créé sur https://discord.com/developers
- Token Discord
- Dépôt GitHub : https://github.com/jpmak6/LBB-BOT

---

## ⚙️ ÉTAPE 1 : CONFIGURATION DU SERVEUR

### 1.1 Créer le serveur
1. Connecte-toi sur **FPS.MS**
2. Va dans **Créer un serveur**
3. Choisis :
   - **Type** : Bot Discord
   - **Langage** : Python
   - **Version** : Python 3.11

### 1.2 Paramètres de démarrage
Dans **Startup** → **Variables**, vérifie que :
```
PY_FILE = app.py
REQUIREMENTS_FILE = requirements.txt
```

✅ **Le fichier `app.py` existe déjà dans le projet** (lanceur automatique)

---

## 📦 ÉTAPE 2 : IMPORT DU BOT

### **Option A : Via GitHub (RECOMMANDÉ)**

1. Dans le **File Manager** de FPS.MS, supprime tout
2. Clique sur **Git Clone**
3. Entre l'URL : `https://github.com/jpmak6/LBB-BOT.git`
4. Clique sur **Clone**
5. ✅ Tous les fichiers sont importés automatiquement !

### **Option B : Upload manuel**

1. Télécharge le projet depuis GitHub
2. Upload tous les fichiers dans FPS.MS :
   - `app.py` (IMPORTANT !)
   - `bot.py`
   - `requirements.txt`
   - `.env`
   - Dossier `cogs/`
   - `keep_alive.py`

---

## 🔐 ÉTAPE 3 : CONFIGURER LE TOKEN

### Via Variables d'environnement (RECOMMANDÉ)

1. Va dans **Startup** → **Variables**
2. Ajoute une nouvelle variable :
   - **Nom** : `DISCORD_TOKEN`
   - **Valeur** : Ton token Discord
3. Sauvegarde

### Via fichier .env

1. Dans **File Manager**, ouvre `.env`
2. Modifie :
```env
DISCORD_TOKEN=ton_token_discord_ici
```
3. Sauvegarde

⚠️ **ATTENTION** : Ne partage JAMAIS ton token !

---

## 🚀 ÉTAPE 4 : LANCER LE BOT

### 4.1 Installer les dépendances

Le serveur installera automatiquement les dépendances depuis `requirements.txt` au premier lancement.

Contenu de `requirements.txt` :
```
discord.py>=2.4.0
python-dotenv==1.0.0
aiohttp>=3.9.1
PyNaCl>=1.5.0
Flask==3.0.0
```

### 4.2 Démarrer le bot

1. Clique sur **Start** (bouton vert)
2. Attends quelques secondes
3. Dans la console, tu devrais voir :
```
✅ Connecté en tant que LBB BOT#1402
🌐 Connecté à 1 serveur(s)
✅ Module chargé: simple
✅ Module chargé: v3_admin
🎉 Bot prêt et opérationnel! (V3.1)
```

✅ **LE BOT EST EN LIGNE ! 🎉**

---

## 🔍 ÉTAPE 5 : VÉRIFICATION

### Tester le bot sur Discord

1. Va sur ton serveur Discord
2. Tape `!ping`
3. Le bot doit répondre avec la latence
4. Tape `!sondage` (si tu es admin)
5. Le bouton doit apparaître

---

## 🛠️ DÉPANNAGE

### **Erreur : "can't open file '/home/container/app.py'"**

**Cause** : Le fichier `app.py` est manquant

**Solution** :
1. Vérifie que `app.py` existe dans le File Manager
2. Si absent, crée-le avec ce contenu :
```python
if __name__ == "__main__":
    import bot
```

---

### **Erreur : "No module named 'discord'"**

**Cause** : Dependencies pas installées

**Solution** :
1. Vérifie que `requirements.txt` existe
2. Dans la console, tape :
```bash
pip install -r requirements.txt
```
3. Redémarre le serveur

---

### **Erreur : "Token invalide"**

**Cause** : Token Discord incorrect ou manquant

**Solution** :
1. Va sur https://discord.com/developers
2. Sélectionne ton bot
3. Va dans **Bot** → **Reset Token**
4. Copie le nouveau token
5. Mets-le dans **Startup Variables** ou `.env`
6. Redémarre

---

### **Bot se déconnecte après quelques minutes**

**Cause** : Serveur gratuit avec limitations

**Solution** :
1. **Option A** : Upgrade vers un plan payant FPS.MS
2. **Option B** : Utilise un autre hébergeur (Railway, Replit)
3. **Option C** : Configure un keep-alive (déjà intégré avec Flask)

---

### **Logs : "Erreur lors du chargement de embeds"**

**Cause** : Bug connu dans le module embeds (non-critique)

**Solution** :
- ⚠️ C'est normal et n'affecte pas le fonctionnement
- Le bot fonctionne quand même
- Pour désactiver, retire `embeds` de la liste dans `bot.py` ligne 84

---

## 📊 MONITORING & MAINTENANCE

### Voir les logs en temps réel

Dans la console FPS.MS, les logs s'affichent automatiquement :
```
INFO - ✅ Connecté en tant que LBB BOT
INFO - ✅ Module chargé: v3_admin
INFO - 🎉 Bot prêt et opérationnel!
```

### Redémarrer le bot

1. Clique sur **Stop** (bouton rouge)
2. Attends 5 secondes
3. Clique sur **Start** (bouton vert)

### Mettre à jour le bot

**Via Git (si tu as cloné depuis GitHub) :**
1. Push tes modifications sur GitHub
2. Dans FPS.MS console, tape :
```bash
git pull origin main
```
3. Redémarre le serveur

**Via Upload manuel :**
1. Upload les fichiers modifiés
2. Redémarre le serveur

---

## ⚡ OPTIMISATIONS FPS.MS

### 1. Activer Auto-Restart

Dans **Startup Settings** :
- **Auto Restart** : ON
- Le bot redémarre automatiquement en cas de crash

### 2. Configurer les Ports

Si tu utilises le keep-alive Flask :
1. Va dans **Network** → **Allocations**
2. Note le port assigné (ex: `25565`)
3. Le serveur Flask utilisera ce port automatiquement

### 3. Gestion de la RAM

- **Bot Discord basique** : 256-512 MB suffisent
- **Avec keep-alive Flask** : 512 MB recommandés
- Surveille l'utilisation dans **Resources**

---

## 📋 CHECKLIST DE DÉPLOIEMENT

Avant de déclarer le bot "en production" :

- [ ] Fichier `app.py` présent
- [ ] `requirements.txt` présent
- [ ] Token Discord configuré
- [ ] Dossier `cogs/` uploadé
- [ ] Bot démarre sans erreur
- [ ] Console affiche "✅ Connecté en tant que..."
- [ ] Commande `!ping` fonctionne sur Discord
- [ ] Commande `!sondage` fonctionne (admin)
- [ ] Commande `!embed` fonctionne (admin)
- [ ] Panneaux tickets créés (`!setup_demande`, `!setup_maintenance`)

---

## 🔗 LIENS UTILES

- **FPS.MS** : https://fps.ms
- **Panel** : https://panel.fps.ms
- **Discord Bot Portal** : https://discord.com/developers
- **GitHub Projet** : https://github.com/jpmak6/LBB-BOT
- **Support FPS.MS** : https://discord.gg/fps (serveur Discord)

---

## 💡 CONSEILS PRO

1. **Backup régulier** : Télécharge ton dossier `transcripts/` chaque semaine
2. **Logs** : Vérifie les logs 1x/jour pour détecter les erreurs
3. **Mise à jour** : Pull depuis GitHub chaque semaine
4. **Monitoring** : Configure un service comme UptimeRobot si besoin
5. **Sécurité** : Ne partage JAMAIS ton token Discord

---

## 🆚 FPS.MS vs REPLIT

### **FPS.MS (Pterodactyl)**
- ✅ Plus stable
- ✅ Meilleure performance
- ✅ Accès SSH/SFTP
- ✅ Logs détaillés
- ❌ Configuration plus technique

### **Replit**
- ✅ Plus simple pour débutants
- ✅ Interface web intuitive
- ✅ Gratuit avec limitations
- ❌ Besoin d'UptimeRobot pour keep-alive
- ❌ Moins de contrôle

**Recommandation** : FPS.MS pour production, Replit pour test/dev

---

## 🎯 COMMANDES SPÉCIFIQUES FPS.MS

Dans la console FPS.MS, tu peux utiliser :

```bash
# Installer une dépendance
pip install nom_du_package

# Voir les packages installés
pip list

# Mettre à jour discord.py
pip install --upgrade discord.py

# Vérifier la version Python
python --version

# Lancer le bot manuellement
python app.py
```

---

## 🚨 EN CAS DE CRASH

1. Regarde les dernières lignes de la console
2. Note l'erreur exacte
3. Vérifie le **Exit code** :
   - `Exit code: 0` = Arrêt normal
   - `Exit code: 1` = Erreur Python
   - `Exit code: 2` = Fichier manquant
4. Cherche l'erreur dans ce guide
5. Si pas résolu, demande de l'aide sur le Discord FPS.MS

---

## ✅ RÉSUMÉ EN 5 ÉTAPES

1. **Clone depuis GitHub** dans FPS.MS
2. **Configure le token** dans Variables ou .env
3. **Vérifie que `app.py` existe**
4. **Clique sur Start**
5. **Teste `!ping` sur Discord**

---

**🎉 TON BOT EST MAINTENANT HÉBERGÉ 24/7 ! 🚀**

**Support SIMON&CO** : Si problème, ouvre une issue sur GitHub
