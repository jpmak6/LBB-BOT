# 🚀 GUIDE V3.1 - SIMON&CO

## ✨ NOUVEAUTÉS V3.1

### 🎯 **Philosophie V3.1**
**"Moins de commandes = Plus de simplicité"**

- ❌ Suppression des commandes d'aide (plus de spam)
- ✅ Seulement 2 commandes admin ultra-simples
- 🔐 Whitelist stricte : Seuls 2 admins peuvent créer sondages et embeds
- 👥 Tous les membres peuvent voter aux sondages
- 🔒 Seuls les admins voient qui a voté

---

## 🎮 COMMANDES V3.1 (ADMINS UNIQUEMENT)

### 📊 **SONDAGE** - `!sondage`

**Qui peut l'utiliser ?**
- ✅ Admin 1 : `1184303630250164239`
- ✅ Admin 2 : `1391756912823107716`
- ❌ Tous les autres : Commande ignorée silencieusement

**Comment ça marche ?**
1. Tape `!sondage` dans n'importe quel salon
2. Un bouton apparaît : **"📊 Créer le sondage"**
3. Clique dessus → Un formulaire s'ouvre
4. Remplis :
   - ❓ Question du sondage
   - 🅰️ Option 1 (obligatoire)
   - 🅱️ Option 2 (obligatoire)
   - 🅲 Option 3 (optionnelle)
   - 🅳 Option 4 (optionnelle)
5. Valide → Le sondage est publié !

**Résultat :**
- 📊 Embed professionnel avec ta question
- 🅰️🅱️🅲🅳 Réactions automatiques pour voter
- 👥 Bouton "Voir qui a voté" (admin uniquement)
- ✅ Tout le monde peut voter en cliquant sur les réactions

**Exemple :**
```
Question : Préférez-vous le café ou le thé ?
🅰️ Café
🅱️ Thé
🅲 Chocolat chaud
```

---

### ✨ **EMBED** - `!embed`

**Qui peut l'utiliser ?**
- ✅ Admin 1 : `1184303630250164239`
- ✅ Admin 2 : `1391756912823107716`
- ❌ Tous les autres : Commande ignorée silencieusement

**Comment ça marche ?**
1. Tape `!embed` dans n'importe quel salon
2. Un bouton apparaît : **"✨ Créer l'embed"**
3. Clique dessus → Un formulaire s'ouvre
4. Remplis :
   - 📌 Titre (obligatoire)
   - 📝 Description/Message (obligatoire)
   - 🎨 Couleur : bleu/rouge/vert/jaune/violet/orange (optionnel)
   - 📄 Texte en bas (optionnel)
   - 📢 Mentionner @everyone ? oui/non (optionnel)
5. Valide → L'embed est publié !

**Résultat :**
- ✨ Message embed professionnel avec ta couleur
- 👤 Affiche ton nom comme auteur
- 📄 Footer personnalisable
- 📢 Possibilité de mentionner @everyone

**Exemple d'utilisation :**
```
Titre : Réunion Importante
Message : RDV mercredi à 14h dans la salle 2 pour discuter du projet Q1
Couleur : rouge
Footer : Direction SIMON&CO
Mention : oui
```

**Couleurs disponibles :**
- 🔵 `bleu` (par défaut)
- 🔴 `rouge`
- 🟢 `vert`
- 🟡 `jaune`
- 🟣 `violet`
- 🟠 `orange`

---

## 🔐 SÉCURITÉ V3.1

### **Whitelist Ultra-Stricte**
- Fichier : [`cogs/v3_admin.py`](cogs/v3_admin.py) ligne 8
- Seuls 2 IDs peuvent utiliser `!sondage` et `!embed`
- Tous les autres : Commande supprimée silencieusement (pas de notification)

### **Votes des sondages**
- ✅ Tout le monde peut voter (réactions publiques)
- 🔒 Seuls les admins voient QUI a voté (bouton caché)
- 📊 Résultats en temps réel

---

## 🎫 SYSTÈME DE TICKETS (Inchangé)

Les tickets V2 restent actifs :
- `!setup_demande` - Panneau Demandes/Problèmes
- `!setup_maintenance` - Panneau Maintenances
- `!panel_admin` - Panel admin complet

---

## ❌ COMMANDES DÉSACTIVÉES EN V3.1

Ces commandes ne fonctionnent plus :
- ❌ `!aide` / `!help` / `!h`
- ❌ `!regles` / `!rules`

**Pourquoi ?**
- Moins de spam
- Interface ultra-simple
- Seuls les admins ont besoin de commandes

---

## 📋 COMMANDES TOUJOURS ACTIVES

### **Informations** (Tout le monde)
```
!ping              → Latence du bot
!info              → Infos du bot
!serveurinfo       → Stats du serveur
!userinfo @user    → Infos d'un membre
```

### **Modération** (Staff)
```
!kick @user raison     → Expulser
!ban @user raison      → Bannir
!unban ID              → Débannir
!timeout @user durée   → Timeout
!untimeout @user       → Retirer timeout
!clear nombre          → Supprimer messages
```

---

## 🎯 UTILISATION RECOMMANDÉE

### **Pour les Admins SIMON&CO :**

**Créer un sondage :**
```
1. !sondage
2. Clique sur le bouton
3. Remplis le formulaire
4. C'est tout !
```

**Créer une annonce :**
```
1. !embed
2. Clique sur le bouton
3. Remplis le formulaire
4. Choisis la couleur rouge
5. Mentionne @everyone si important
```

**Voir qui a voté :**
```
1. Va sur un sondage
2. Clique sur "👥 Voir qui a voté"
3. Liste complète s'affiche (en privé)
```

### **Pour les Employés :**

**Voter à un sondage :**
```
1. Clique sur 🅰️, 🅱️, 🅲 ou 🅳
2. C'est tout !
```

**Créer un ticket :**
```
1. Clique sur le bouton du panneau
2. Ticket créé automatiquement
```

---

## 🔧 PERSONNALISATION

### **Ajouter un nouvel admin**
Ouvre [`cogs/v3_admin.py`](cogs/v3_admin.py) ligne 8 :
```python
ADMINS_AUTORISES = [
    1184303630250164239,  # Admin 1
    1391756912823107716,  # Admin 2
    123456789012345678    # Nouvel admin (ajoute son ID)
]
```

### **Changer les couleurs disponibles**
Ouvre [`cogs/v3_admin.py`](cogs/v3_admin.py) ligne 186 :
```python
couleurs = {
    "bleu": discord.Color.blue(),
    "rouge": discord.Color.red(),
    # Ajoute tes couleurs ici
}
```

---

## 📊 STATISTIQUES V3.1

**Commandes supprimées :** 2 (!aide, !regles)
**Nouvelles commandes :** 2 (!sondage, !embed)
**Admins autorisés :** 2 IDs
**Simplicité :** 1000% 🚀

---

## 🆘 DÉPANNAGE

### **Problème : Un non-admin peut utiliser !sondage**
**Solution :** Vérifie que son ID n'est pas dans la whitelist (ligne 8 de v3_admin.py)

### **Problème : Le bouton "Voir qui a voté" est visible par tous**
**Solution :** Normal ! Mais seuls les admins peuvent cliquer dessus. Les autres ont un message d'erreur.

### **Problème : Le sondage n'a pas de réactions**
**Solution :** Le bot doit avoir la permission "Ajouter des réactions" dans le salon.

### **Problème : L'embed ne mentionne pas @everyone**
**Solution :** 
1. Vérifie que tu as écrit "oui" dans le champ mention
2. Le bot doit avoir la permission "Mentionner @everyone"

---

## 🎉 CHANGELOG V3.1

**AJOUTÉ :**
- ✅ Commande `!sondage` avec formulaire interactif
- ✅ Commande `!embed` avec formulaire interactif
- ✅ Bouton "Voir qui a voté" (admin uniquement)
- ✅ Whitelist stricte par ID
- ✅ Votes publics, résultats privés

**SUPPRIMÉ :**
- ❌ Commande `!aide` / `!help`
- ❌ Commande `!regles` / `!rules`

**MODIFIÉ :**
- 🔄 Activité du bot : "SIMON&CO - V3.1"
- 🔄 Chargement du module `v3_admin`

---

**DÉVELOPPÉ AVEC ❤️ POUR SIMON&CO**

🚀 **Profitez de la V3.1 !**
