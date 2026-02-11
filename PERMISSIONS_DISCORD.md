# 🔐 CONFIGURATION DES PERMISSIONS DISCORD

## 📋 Permissions nécessaires pour le bot

### ⚡ Option 1 : ADMINISTRATEUR (RECOMMANDÉ - Plus simple)
Sur https://discord.com/developers/applications :

1. Va dans ton application bot
2. **OAuth2** → **URL Generator**
3. **Scopes** : Coche `bot`
4. **Bot Permissions** : Coche `Administrator`
5. Copie le lien généré et réinvite le bot

✅ **Avantage** : Toutes les fonctionnalités marchent sans configuration supplémentaire

---

### 🔧 Option 2 : Permissions spécifiques (Plus sécurisé)

Si tu ne veux pas donner admin au bot, coche ces permissions :

#### **Permissions générales :**
- ✅ `View Channels` (Voir les salons)
- ✅ `Manage Channels` (Gérer les salons - pour créer tickets)
- ✅ `Manage Roles` (Gérer les rôles - pour permissions tickets)

#### **Permissions textuelles :**
- ✅ `Send Messages` (Envoyer des messages)
- ✅ `Send Messages in Threads` (Envoyer dans les fils)
- ✅ `Embed Links` (Intégrer des liens)
- ✅ `Attach Files` (Joindre des fichiers - pour transcripts)
- ✅ `Read Message History` (Lire l'historique - pour transcripts)
- ✅ `Add Reactions` (Ajouter des réactions - pour sondages)
- ✅ `Manage Messages` (Gérer les messages - pour clear)

#### **Permissions de modération :**
- ✅ `Kick Members` (Expulser des membres)
- ✅ `Ban Members` (Bannir des membres)
- ✅ `Timeout Members` (Timeout des membres)

---

## 🎫 Configuration des SALONS pour les tickets

### 1. Créer les catégories :
- Crée une catégorie `🎫 DEMANDES`
- Crée une catégorie `🎫 MAINTENANCES`

### 2. Permissions des catégories :
Dans les paramètres de chaque catégorie :

**@everyone (rôle par défaut) :**
- ❌ `Voir le salon` : DÉSACTIVÉ

**Ton bot (LBB BOT) :**
- ✅ `Voir le salon` : ACTIVÉ
- ✅ `Gérer les salons` : ACTIVÉ
- ✅ `Envoyer des messages` : ACTIVÉ
- ✅ `Gérer les messages` : ACTIVÉ
   /§%;fsqùmlbd;fb 
---

## 🔐 Configuration du SALON ADMIN (RECOMMANDÉ)

### Pour sécuriser ton panel admin :

1. **Crée un salon privé** `#admin-panel`

2. **Permissions du salon** :

**@everyone :**
- ❌ `Voir le salon` : DÉSACTIVÉ

**@Administrateurs (rôle admin) :**
- ✅ `Voir le salon` : ACTIVÉ
- ✅ `Envoyer des messages` : ACTIVÉ

**Ton bot :**
- ✅ `Voir le salon` : ACTIVÉ
- ✅ `Envoyer des messages` : ACTIVÉ

3. **Utilisation** :
   - Tape `!panel_admin` dans `#admin-panel`
   - Seuls les admins verront le panel
   - Les non-admins ne peuvent même pas voir le salon

---

## ✅ VÉRIFICATION RAPIDE

Teste ces commandes dans ton serveur :

```
!setup_demande      → Crée le panel demandes
!setup_maintenance  → Crée le panel maintenance
!panel_admin        → Affiche le panel admin (admin only)
!pollcreate         → Crée un sondage (admin only)
```

Si une commande ne marche pas, vérifie les permissions du bot sur Discord Developer Portal.

---

## 🔗 Lien de réinvitation avec toutes les permissions

https://discord.com/developers/applications

1. Sélectionne ton bot
2. OAuth2 → URL Generator
3. Scopes : `bot`
4. Permissions : `Administrator` (ou coche toutes les permissions listées ci-dessus)
5. Copie le lien et clique dessus
6. Réinvite le bot sur ton serveur

✅ Tous les problèmes de permissions seront résolés !
