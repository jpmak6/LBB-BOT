# 🚀 Guide Ultra-Simple - Bot LBB pour PME

## ✨ DÉMARRAGE RAPIDE EN 3 ÉTAPES

### 1️⃣ Lance le Bot
Le bot est déjà en ligne ! Tu n'as rien à faire.

### 2️⃣ Crée le Panneau Principal  
Dans n'importe quel salon, tape :
```k!nlk 
!setup
```

### 3️⃣ C'EST FINI !
Tout le monde peut maintenant cliquer sur les boutons pour :
- 🎫 Ouvrir un ticket
- 📊 Créer un sondage  
- 📝 Faire une annonce

**Plus besoin de commandes compliquées !** 🎉

---

## 🎛️ LE PANNEAU PRINCIPAL

Quand tu tapes `!setup`, un panneau apparaît avec **3 boutons** :

### 🎫 Bouton "Ouvrir un Ticket"
**Qui peut l'utiliser ?** → **TOUT LE MONDE**

1. Clique sur le bouton bleu
2. Choisis le type :
   - 💬 Support Général
   - 🐛 Signaler un Bug
   - 💼 Partenariat
   - ❓ Autre Demande
3. Un salon privé se crée automatiquement
4. Le staff est notifié
5. Tu peux discuter en privé

**Pour fermer le ticket :** Clique sur le bouton rouge "🔒 Fermer"

---

### 📊 Bouton "Créer un Sondage"
**Qui peut l'utiliser ?** → **TOUT LE MONDE**

1. Clique sur le bouton vert
2. Un formulaire s'ouvre :
   - **Question** : Écris ta question
   - **Options** : Une par ligne (max 10)
   - **Durée** : En minutes (ou laisse vide)
3. Le sondage est publié
4. Les gens votent avec les réactions

**C'est automatique !** Pas besoin de savoir quoi que ce soit 😊

---

### 📝 Bouton "Créer une Annonce"
**Qui peut l'utiliser ?** → **TOUT LE MONDE**

1. Clique sur le bouton gris
2. Un formulaire s'ouvre :
   - **Titre** : Le titre de ton annonce
   - **Message** : Ton message
3. L'annonce est publiée avec un beau design

---

## 📱 COMMANDES RAPIDES (Si tu préfères taper)

### Pour Tout le Monde

#### Ouvrir un Ticket
```
!ticket
```
→ Menu avec les 4 types de tickets

#### Créer un Sondage
```
!poll 60 "Quelle pizza préférez-vous?" "Margherita" "Pepperoni" "4 Fromages"
```
- `60` = durée en minutes
- Entre guillemets pour la question et les options

**Sondage Oui/Non (encore plus simple) :**
```
!quickpoll Aimez-vous le nouveau logo?
```

#### Faire une Annonce
```
!announcement Réunion demain à 14h dans le salon vocal!
```

---

### Pour les Admins/Mods

#### Modération
```
!clear 50                    → Supprimer 50 messages
!kick @user spam             → Expulser
!ban @user insultes          → Bannir
!timeout @user 10 m spam     → Timeout 10 minutes
!untimeout @user             → Retirer le timeout
```

**Unités de temps pour timeout :**
- `s` = secondes
- `m` = minutes  
- `h` = heures
- `d` = jours

#### Gérer les Tickets
```
!closeticket                 → Fermer le ticket actuel
!addticket @user             → Ajouter quelqu'un au ticket
!removeticket @user          → Retirer quelqu'un
```

---

## 💡 ASTUCES POUR BIEN DÉMARRER

### Configuration Initiale

1. **Crée ces rôles** (optionnel mais recommandé) :
   - `Admin` → Accès complet
   - `Modérateur` → Modération + tickets
   - `Staff` → Voir les tickets
   - `Gérant` → Direction

2. **Crée ces salons** :
   - `#panneau-principal` → Pour mettre le `!setup`
   - `#annonces` → Pour les annonces importantes
   - `#sondages` → Pour les sondages

3. **Lance !setup** dans `#panneau-principal`

4. **C'EST FINI !** Tout le monde peut utiliser

---

## 🎯 EXEMPLES D'UTILISATION EN PME

### Scénario 1 : Un Employé a Besoin d'Aide
1. Il clique sur 🎫 "Ouvrir un Ticket"
2. Choisit "💬 Support Général"  
3. Un salon privé se crée
4. Un manager le rejoint
5. Ils discutent en privé
6. Le manager ferme le ticket quand c'est résolu

### Scénario 2 : Décision d'Équipe
1. Le chef d'équipe clique sur 📊 "Créer un Sondage"
2. Question : "Quel jour pour la réunion?"
3. Options : Lundi / Mercredi / Vendredi
4. Durée : 60 minutes
5. L'équipe vote
6. Résultats automatiques à la fin

### Scénario 3 : Information Importante
1. Le gérant clique sur 📝 "Créer une Annonce"
2. Titre : "Nouveau Client"
3. Message : "Nous avons signé avec XYZ Corp!"
4. L'annonce est publiée avec un beau design

---

## ❓ QUESTIONS FRÉQUENTES

**Q : Est-ce que tout le monde peut créer des tickets/sondages/annonces ?**  
R : OUI ! C'est fait pour ça. Pas de restrictions.

**Q : Comment je sais si j'ai un ticket ouvert ?**  
R : Le bot te dira "Tu as déjà un ticket ouvert" si tu essaies d'en créer un deuxième.

**Q : Les sondages se ferment automatiquement ?**  
R : Oui, après la durée indiquée, les résultats s'affichent automatiquement.

**Q : Qui peut fermer un ticket ?**  
R : Le créateur du ticket OU n'importe quel staff (Admin, Mod, etc.)

**Q : Je ne veux plus taper de commandes, juste des boutons**  
R : Parfait ! Utilise uniquement `!setup` une fois, puis tout se fait par boutons.

---

## 🔧 COMMANDES D'INFO (Bonus)

Ces commandes donnent des infos mais ne modifient rien :

```
!ping                → Latence du bot
!info                → Infos du bot
!serveurinfo         → Stats du serveur
!userinfo @user      → Infos d'un membre
!aide                → Ce menu d'aide
```

---

## ✅ CHECKLIST DE DÉMARRAGE

- [ ] Le bot est en ligne (vérifie qu'il est connecté)
- [ ] Tu as créé les salons recommandés
- [ ] Tu as créé les rôles (Admin, Staff, etc.)
- [ ] Tu as tapé `!setup` dans le salon principal
- [ ] Le panneau s'affiche avec les 3 boutons
- [ ] Tu as testé en cliquant sur chaque bouton
- [ ] Tout le monde peut accéder aux boutons

**Si tout est ✅ → Ton bot est prêt ! 🎉**

---

## 🆘 EN CAS DE PROBLÈME

1. **Le panneau ne s'affiche pas**
   - Vérifie que le bot a la permission d'envoyer des messages
   - Retape `!setup`

2. **Les boutons ne fonctionnent pas**
   - Vérifie que le bot a la permission "Gérer les salons"
   - Redémarre le bot

3. **Un ticket ne se crée pas**
   - Vérifie que tu n'as pas déjà un ticket ouvert
   - Vérifie les permissions du bot

4. **Besoin d'aide ?**
   - Ouvre un ticket avec le bot lui-même ! 😄
   - Ou vérifie les logs dans `bot.log`

---

## 🎊 FÉLICITATIONS !

Ton bot est maintenant **ultra-simple** et **accessible à tous** !

**Avantages :**
- ✅ Interface intuitive avec boutons
- ✅ Pas besoin de formation
- ✅ Tout le monde peut créer tickets/sondages/annonces
- ✅ Parfait pour une PME de 80 personnes
- ✅ Modération complète pour les admins
- ✅ Design professionnel

**Profite bien de ton bot ! 🚀**
