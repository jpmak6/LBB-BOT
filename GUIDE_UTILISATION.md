# 🎯 Guide Complet du Bot Discord LBB

## 🚀 Nouvelles Fonctionnalités Ajoutées

Votre bot est maintenant équipé de systèmes professionnels pour gérer un serveur de 80+ membres !

---

## 🎫 Système de Tickets

### Configuration Initiale
```
!ticketpanel
```
Cette commande créera un panel avec 4 boutons de tickets :
- 💬 **Support** - Questions générales
- 🐛 **Bug Report** - Signaler un bug  
- 💼 **Partenariat** - Demandes de partenariat
- ❓ **Autre** - Autres demandes

### Fonctionnalités
- ✅ Création automatique de salons privés
- ✅ Permissions automatiques (utilisateur + staff)
- ✅ Boutons de contrôle (Fermer, Claim)
- ✅ Sauvegarde des transcripts
- ✅ Organisation par catégories

### Commandes Tickets
- `!ticketpanel` - Créer le panel (Admin)
- `!closeticket` - Fermer un ticket
- `!addticket @user` - Ajouter quelqu'un au ticket
- `!removeticket @user` - Retirer quelqu'un du ticket

### Boutons dans les Tickets
- 🔒 **Fermer** - Ferme et supprime le ticket
- ✋ **Claim** - Prendre en charge le ticket (Staff)

---

## 📝 Système d'Embeds Personnalisés

### Méthode Interactive
```
!embed
```
Ouvre une interface interactive pour créer un embed facilement !

### Méthode Rapide
```
!embedsimple titre="Mon Titre" description="Ma description" couleur=#FF0000
```

**Options disponibles :**
- `titre` ou `title` - Titre de l'embed
- `description` ou `desc` - Description
- `couleur` ou `color` - Couleur en hexadécimal (#FF0000)
- `footer` - Texte en bas
- `image` - URL de l'image principale
- `thumbnail` - URL de la miniature
- `author` - Nom de l'auteur

### Méthode Avancée (JSON)
```
!sendembed {
  "title": "Mon Super Titre",
  "description": "Description complète",
  "color": 3447003,
  "fields": [
    {"name": "Champ 1", "value": "Valeur 1", "inline": true}
  ]
}
```

### Éditer un Embed
```
!editembed <message_id> <json>
```

### Faire une Annonce
```
!announcement Votre message d'annonce ici
```
Crée une belle annonce avec mention @everyone

---

## 📊 Système de Sondages

### Sondage Personnalisé
```
!poll 60 "Quelle est votre couleur préférée?" "Rouge" "Bleu" "Vert" "Jaune"
```
- **Durée** : en minutes (60 = 1 heure)
- **Question** : entre guillemets
- **Options** : 2 à 10 options entre guillemets

### Sondage Rapide Oui/Non
```
!quickpoll Aimez-vous les pizzas?
```
Crée un sondage avec ✅ et ❌

### Voir les Résultats
```
!pollresults <message_id>
```
Affiche les résultats en temps réel avec :
- Barres de progression
- Pourcentages
- Nombre de votes

### Arrêter un Sondage
```
!pollstop <message_id>
```
Termine le sondage immédiatement et affiche les résultats

### Aide Sondages
```
!pollhelp
```

---

## 🛡️ Commandes de Modération

### Clear/Purge
```
!clear 50
```
Supprime les X derniers messages (max 100)

### Kick (Expulsion)
```
!kick @user Raison de l'expulsion
```
Expulse un membre du serveur

### Ban (Bannissement)
```
!ban @user Raison du ban
```
Bannit définitivement un membre

### Unban (Débannissement)
```
!unban 123456789
```
Débannit un utilisateur (utilise son ID)

### Timeout (Mute Temporaire)
```
!timeout @user 10 m Spam dans le chat
```
Met un membre en timeout

**Unités de temps :**
- `s` - secondes
- `m` - minutes
- `h` - heures
- `d` - jours (max 28)

**Exemples :**
- `!timeout @user 30 s` - 30 secondes
- `!timeout @user 10 m` - 10 minutes
- `!timeout @user 2 h` - 2 heures
- `!timeout @user 1 d` - 1 jour

### Retirer un Timeout
```
!untimeout @user
```

---

## 👥 Commandes d'Information

### Info Serveur
```
!serveurinfo
```
Affiche toutes les stats du serveur

### Info Membre
```
!userinfo @user
```
Affiche les infos d'un membre

### Info Bot
```
!info
```
Stats et informations du bot

### Ping
```
!ping
```
Vérifie la latence du bot

---

## 📋 Menu d'Aide
```
!aide
```
Affiche toutes les commandes disponibles

---

## 🎯 Configuration Recommandée pour 80+ Membres

### 1. Créer les Rôles Nécessaires
- **Admin** - Accès complet
- **Modérateur** - Gestion des membres et tickets

### 2. Créer les Salons
- **#tickets** - Pour le panel de tickets
- **#annonces** - Pour les annonces officielles  
- **#sondages** - Pour les sondages
- **#règles** - Pour les règles du serveur

### 3. Configurer les Catégories
Le bot créera automatiquement :
- 🎫 TICKETS SUPPORT
- 🎫 TICKETS BUGS
- 🎫 TICKETS PARTENARIATS
- 🎫 TICKETS DIVERS

### 4. Lancer le Panel de Tickets
```
!ticketpanel
```
Dans le salon #tickets

### 5. Publier les Règles
```
!regles
```
Dans le salon #règles

---

## 💡 Astuces pour Gros Serveurs

### Organisation des Tickets
- Créez des rôles **Support Team** pour gérer les tickets
- Utilisez le bouton **Claim** pour assigner les tickets
- Les transcripts sont sauvegardés automatiquement

### Sondages Efficaces
- Utilisez des durées raisonnables (30-60 min pour décisions rapides)
- `!pollresults` permet de voir l'évolution en temps réel
- Épinglez les sondages importants

### Modération
- Utilisez `!timeout` pour les infractions mineures
- `!kick` pour les récidivistes
- `!ban` pour les cas graves
- Les logs sont enregistrés automatiquement

### Embeds
- Utilisez `!announcement` pour les annonces importantes
- Créez des embeds pour les événements
- `!embedsimple` est parfait pour des messages rapides

---

## 🔧 Permissions Nécessaires

Le bot a besoin de ces permissions :
- ✅ Gérer les salons
- ✅ Gérer les messages
- ✅ Gérer les rôles
- ✅ Expulser des membres
- ✅ Bannir des membres
- ✅ Mettre en timeout
- ✅ Envoyer des messages
- ✅ Ajouter des réactions
- ✅ Voir l'historique des messages
- ✅ Embed Links

---

## 🆘 Support

En cas de problème :
1. Vérifie que les intents sont activés sur Discord Developer Portal
2. Vérifie les permissions du bot
3. Regarde les logs dans `bot.log`
4. Les transcripts des tickets sont dans le dossier `/transcripts`

---

## 🎉 Prochaines Étapes

Le bot est prêt pour :
- Gérer 80+ membres efficacement
- Système de tickets professionnel
- Sondages communautaires
- Annonces stylisées
- Modération complète

**Le bot est maintenant opérationnel ! Teste les commandes sur ton serveur !** 🚀
