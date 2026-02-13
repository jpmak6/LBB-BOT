import discord
from discord.ext import commands, tasks
from discord.ui import Button, View, Modal, TextInput
from datetime import datetime, time
import asyncio
import logging

logger = logging.getLogger('discord')

# ============================================
# WHITELIST ULTRA-STRICTE - V3.1
# ============================================
ADMINS_AUTORISES = [
    1184303630250164239,  # Admin principal
    1391756912823107716   # Créateur du serveur
]

def est_admin(user_id: int) -> bool:
    """Vérifier si l'utilisateur est dans la whitelist"""
    return user_id in ADMINS_AUTORISES

# ============================================
# SONDAGE V3.1 - SIMPLE ET FONCTIONNEL
# ============================================

class SondageModal(Modal):
    """Modal pour créer un sondage (MAX 5 champs Discord)"""
    def __init__(self):
        super().__init__(title="📊 Créer un Sondage")
        
        self.question = TextInput(
            label="❓ Question du sondage",
            placeholder="Exemple : Préférez-vous le café ou le thé ?",
            style=discord.TextStyle.short,
            required=True,
            max_length=200
        )
        self.add_item(self.question)
        
        self.option1 = TextInput(
            label="🅰️ Option 1",
            placeholder="Exemple : Café",
            style=discord.TextStyle.short,
            required=True,
            max_length=80
        )
        self.add_item(self.option1)
        
        self.option2 = TextInput(
            label="🅱️ Option 2",
            placeholder="Exemple : Thé",
            style=discord.TextStyle.short,
            required=True,
            max_length=80
        )
        self.add_item(self.option2)
        
        self.option3 = TextInput(
            label="🅲 Option 3 (Optionnel)",
            placeholder="Laisser vide si pas besoin",
            style=discord.TextStyle.short,
            required=False,
            max_length=80
        )
        self.add_item(self.option3)
        
        self.duree = TextInput(
            label="⏱️ Durée en minutes (vide = illimité)",
            placeholder="Ex: 60 pour 1h",
            style=discord.TextStyle.short,
            required=False,
            max_length=5
        )
        self.add_item(self.duree)
        
    
    async def on_submit(self, interaction: discord.Interaction):
        # Créer les options (max 3 pour respecter limite Discord)
        options = [self.option1.value, self.option2.value]
        if self.option3.value:
            options.append(self.option3.value)
        
        # Gérer la durée
        duree_minutes = None
        if self.duree.value:
            try:
                duree_minutes = int(self.duree.value)
                if duree_minutes <= 0:
                    await interaction.response.send_message(
                        "❌ La durée doit être supérieure à 0 minutes.",
                        ephemeral=True
                    )
                    return
            except ValueError:
                await interaction.response.send_message(
                    "❌ Durée invalide. Entre un nombre entier.",
                    ephemeral=True
                )
                return
        
        # Emojis pour les votes
        emojis = ["🅰️", "🅱️", "🅲"]
        
        # Footer avec durée
        footer_text = "👆 Votez en cliquant sur les réactions"
        if duree_minutes:
            footer_text += f" • ⏱️ Expire dans {duree_minutes} min"
        
        # Créer l'embed du sondage
        embed = discord.Embed(
            title="📊 SONDAGE",
            description=f"**{self.question.value}**\n\n" + "\n".join([
                f"{emojis[i]} **{opt}**" for i, opt in enumerate(options)
            ]),
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        embed.set_author(
            name=f"Sondage par {interaction.user.display_name}",
            icon_url=interaction.user.display_avatar.url
        )
        embed.set_footer(text=footer_text)
        
        # Confirmer
        await interaction.response.send_message(
            f"✅ Sondage créé !{f' ⏱️ Suppression auto dans {duree_minutes} min' if duree_minutes else ''}",
            ephemeral=True
        )
        
        # Créer vue avec bouton admin
        view = SondageView()
        
        # Envoyer le sondage
        message = await interaction.channel.send(embed=embed, view=view)
        
        # Ajouter les réactions
        for i in range(len(options)):
            await message.add_reaction(emojis[i])
        
        # Auto-suppression si durée définie
        if duree_minutes:
            await asyncio.sleep(duree_minutes * 60)
            try:
                await message.delete()
                logger.info(f"🗑️ Sondage auto-supprimé après {duree_minutes} min")
            except:
                pass
            options.append(self.option4.value)
        
        # Emojis pour les votes
        emojis = ["🅰️", "🅱️", "🅲", "🅳"]
        
        # Créer l'embed du sondage
        embed = discord.Embed(
            title="📊 SONDAGE",
            description=f"**{self.question.value}**\n\n" + "\n".join([
                f"{emojis[i]} **{opt}**" for i, opt in enumerate(options)
            ]),
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        embed.set_author(
            name=f"Sondage créé par {interaction.user.display_name}",
            icon_url=interaction.user.display_avatar.url
        )
        embed.set_footer(text="👆 Votez en cliquant sur les réactions • Résultats en temps réel")
        
        # Confirmer la création
        await interaction.response.send_message(
            "✅ Sondage créé avec succès !",
            ephemeral=True
        )
        
        # Créer la vue avec bouton admin
        view = SondageView()
        
        # Envoyer le sondage dans le canal
        message = await interaction.channel.send(embed=embed, view=view)
        
        # Ajouter les réactions pour voter
        for i in range(len(options)):
            await message.add_reaction(emojis[i])

class SondageView(View):
    """Vue avec bouton pour voir les votants (admin only)"""
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(
        label="👥 Voir qui a voté",
        style=discord.ButtonStyle.secondary,
        custom_id="voir_votants_v3"
    )
    async def voir_votants(self, interaction: discord.Interaction, button: Button):
        # VÉRIFICATION : Seuls les admins peuvent voir
        if not est_admin(interaction.user.id):
            await interaction.response.send_message(
                "❌ **Accès refusé**\n\n"
                "🔐 Seuls les administrateurs SIMON&CO peuvent voir qui a voté.",
                ephemeral=True
            )
            return
        
        # Récupérer le message du sondage
        try:
            message = await interaction.channel.fetch_message(interaction.message.id)
        except:
            await interaction.response.send_message(
                "❌ Impossible de récupérer les votes. Le message est peut-être trop ancien.",
                ephemeral=True
            )
            return
        
        # Analyser les réactions
        votants_text = "**👥 LISTE DES VOTANTS**\n\n"
        total_votes = 0
        
        for reaction in message.reactions:
            if str(reaction.emoji) in ["🅰️", "🅱️", "🅲"]:
                users = [user async for user in reaction.users() if not user.bot]
                if users:
                    total_votes += len(users)
                    votants_text += f"{reaction.emoji} **({len(users)} votes)**\n"
                    votants_text += "\n".join([f"  • {user.mention}" for user in users])
                    votants_text += "\n\n"
        
        if total_votes == 0:
            votants_text += "_Aucun vote pour le moment._"
        
        # Créer l'embed des résultats détaillés
        embed = discord.Embed(
            title="🔐 Résultats détaillés du sondage",
            description=votants_text,
            color=discord.Color.gold(),
            timestamp=datetime.now()
        )
        embed.set_footer(text=f"🔒 Admin uniquement • Total: {total_votes} votes")
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

# ============================================
# PANEL ADMIN EMBED - PROFESSIONNEL & COMPLET
# ============================================

class EmbedPanelView(View):
    """Panel de contrôle professionnel pour créer des embeds"""
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(
        label="✨ Créer un Embed",
        style=discord.ButtonStyle.primary,
        custom_id="embed_create_v3",
        emoji="✨",
        row=0
    )
    async def creer_embed(self, interaction: discord.Interaction, button: Button):
        if not est_admin(interaction.user.id):
            await interaction.response.send_message("❌ Accès refusé", ephemeral=True)
            return
        await interaction.response.send_modal(EmbedModal())
    
    @discord.ui.button(
        label="Annonce Simple",
        style=discord.ButtonStyle.success,
        custom_id="embed_annonce_v3",
        emoji="📢",
        row=0
    )
    async def annonce_simple(self, interaction: discord.Interaction, button: Button):
        if not est_admin(interaction.user.id):
            await interaction.response.send_message("❌ Accès refusé", ephemeral=True)
            return
        await interaction.response.send_modal(AnnonceModal())
    
    @discord.ui.button(
        label="Info / Rappel",
        style=discord.ButtonStyle.secondary,
        custom_id="embed_info_v3",
        emoji="ℹ️",
        row=1
    )
    async def info_rappel(self, interaction: discord.Interaction, button: Button):
        if not est_admin(interaction.user.id):
            await interaction.response.send_message("❌ Accès refusé", ephemeral=True)
            return
        await interaction.response.send_modal(InfoModal())
    
    @discord.ui.button(
        label="Alerte / Urgent",
        style=discord.ButtonStyle.danger,
        custom_id="embed_alerte_v3",
        emoji="⚠️",
        row=1
    )
    async def alerte_urgent(self, interaction: discord.Interaction, button: Button):
        if not est_admin(interaction.user.id):
            await interaction.response.send_message("❌ Accès refusé", ephemeral=True)
            return
        await interaction.response.send_modal(AlerteModal())

class EmbedModal(Modal):
    """Modal complet pour créer un embed personnalisé"""
    def __init__(self):
        super().__init__(title="✨ Créer un Embed Personnalisé")
        
        self.titre = TextInput(
            label="📌 Titre",
            placeholder="Exemple : Annonce Importante",
            style=discord.TextStyle.short,
            required=True,
            max_length=256
        )
        self.add_item(self.titre)
        
        self.description = TextInput(
            label="📝 Message",
            placeholder="Ton message ici...",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=2000
        )
        self.add_item(self.description)
        
        self.couleur = TextInput(
            label="🎨 Couleur (bleu/rouge/vert/jaune/violet)",
            placeholder="bleu",
            style=discord.TextStyle.short,
            required=False,
            max_length=20
        )
        self.add_item(self.couleur)
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            # Couleurs disponibles
            couleurs = {
                "bleu": discord.Color.blue(),
                "rouge": discord.Color.red(),
                "vert": discord.Color.green(),
                "jaune": discord.Color.gold(),
                "violet": discord.Color.purple(),
                "orange": discord.Color.orange(),
            }
            
            couleur = couleurs.get(
                self.couleur.value.lower().strip() if self.couleur.value else "bleu", 
                discord.Color.blue()
            )
            
            # Créer l'embed
            embed = discord.Embed(
                title=self.titre.value,
                description=self.description.value,
                color=couleur,
                timestamp=datetime.now()
            )
            
            embed.set_footer(text=f"Par {interaction.user.display_name} • SIMON&CO")
            
            # Confirmer
            await interaction.response.send_message("✅ Embed créé !", ephemeral=True)
            
            # Envoyer l'embed
            await interaction.channel.send(embed=embed)
            logger.info(f"✅ Embed créé par {interaction.user.name}")
            
        except Exception as e:
            logger.error(f"❌ Erreur embed: {e}")
            await interaction.response.send_message(f"❌ Erreur: {e}", ephemeral=True)

class AnnonceModal(Modal):
    """Modal pour annonce rapide"""
    def __init__(self):
        super().__init__(title="📢 Annonce Simple")
        
        self.message = TextInput(
            label="📢 Ton annonce",
            placeholder="Exemple : Réunion demain à 14h...",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=2000
        )
        self.add_item(self.message)
        
        self.mention = TextInput(
            label="🔔 Mentionner @everyone ? (oui/non)",
            placeholder="non",
            style=discord.TextStyle.short,
            required=False,
            max_length=3
        )
        self.add_item(self.mention)
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            embed = discord.Embed(
                title="📢 ANNONCE",
                description=self.message.value,
                color=discord.Color.blue(),
                timestamp=datetime.now()
            )
            embed.set_footer(text=f"Par {interaction.user.display_name}")
            
            mention = self.mention.value and self.mention.value.lower() in ["oui", "yes", "o", "y"]
            
            await interaction.response.send_message("✅ Annonce publiée !", ephemeral=True)
            await interaction.channel.send(
                content="@everyone" if mention else None,
                embed=embed
            )
            logger.info(f"✅ Annonce créée par {interaction.user.name}")
        except Exception as e:
            logger.error(f"❌ Erreur annonce: {e}")
            await interaction.response.send_message(f"❌ Erreur: {e}", ephemeral=True)

class InfoModal(Modal):
    """Modal pour info/rappel"""
    def __init__(self):
        super().__init__(title="ℹ️ Information / Rappel")
        
        self.titre = TextInput(
            label="ℹ️ Titre",
            placeholder="Exemple : Rappel Important",
            style=discord.TextStyle.short,
            required=True,
            max_length=200
        )
        self.add_item(self.titre)
        
        self.message = TextInput(
            label="📝 Message",
            placeholder="Ton information...",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=2000
        )
        self.add_item(self.message)
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            embed = discord.Embed(
                title=f"ℹ️ {self.titre.value}",
                description=self.message.value,
                color=discord.Color.blue(),
                timestamp=datetime.now()
            )
            embed.set_footer(text="SIMON&CO")
            
            await interaction.response.send_message("✅ Info publiée !", ephemeral=True)
            await interaction.channel.send(embed=embed)
            logger.info(f"✅ Info créée par {interaction.user.name}")
        except Exception as e:
            logger.error(f"❌ Erreur info: {e}")
            await interaction.response.send_message(f"❌ Erreur: {e}", ephemeral=True)
            await interaction.channel.send(embed=embed)
            logger.info(f"✅ Info créée par {interaction.user.name}")
        except Exception as e:
            logger.error(f"❌ Erreur info: {e}")
            await interaction.response.send_message(f"❌ Erreur: {e}", ephemeral=True)

class AlerteModal(Modal):
    """Modal pour alerte urgente"""
    def __init__(self):
        super().__init__(title="⚠️ Alerte Urgente")
        
        self.titre = TextInput(
            label="⚠️ Titre de l'alerte",
            placeholder="Exemple : URGENT",
            style=discord.TextStyle.short,
            required=True,
            max_length=200
        )
        self.add_item(self.titre)
        
        self.message = TextInput(
            label="🚨 Message urgent",
            placeholder="Décris l'urgence...",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=2000
        )
        self.add_item(self.message)
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            embed = discord.Embed(
                title=f"🚨 {self.titre.value}",
                description=self.message.value,
                color=discord.Color.red(),
                timestamp=datetime.now()
            )
            embed.set_footer(text="⚠️ Alerte SIMON&CO")
            
            await interaction.response.send_message("✅ Alerte envoyée !", ephemeral=True)
            await interaction.channel.send(content="@everyone", embed=embed)
            logger.info(f"✅ Alerte créée par {interaction.user.name}")
        except Exception as e:
            logger.error(f"❌ Erreur alerte: {e}")
            await interaction.response.send_message(f"❌ Erreur: {e}", ephemeral=True
        )
        embed.set_footer(text="⚠️ Alerte SIMON&CO")
        
        await interaction.response.send_message("✅ Alerte envoyée !", ephemeral=True)
        await interaction.channel.send(content="@everyone", embed=embed)

# ============================================
# COG PRINCIPAL V3.1
# ============================================

class AdminV3(commands.Cog):
    """Commandes exclusives V3.1 pour admins SIMON&CO"""
    
    def __init__(self, bot):
        self.bot = bot
        self.rappel_salades.start()  # Démarrer la tâche automatique
    
    def cog_unload(self):
        """Arrêter la tâche quand le cog est déchargé"""
        self.rappel_salades.cancel()
    
    @tasks.loop(time=time(hour=8, minute=0))  # Tous les jours à 8h00
    async def rappel_salades(self):
        """Envoyer un rappel pour les salades tous les lundis à 8h"""
        # Vérifier si c'est lundi (0 = lundi)
        if datetime.now().weekday() != 0:
            return
        
        # Trouver le salon #🎭︱・responsables
        for guild in self.bot.guilds:
            channel = discord.utils.get(guild.text_channels, name="🎭︱・responsables")
            if channel:
                # Chercher le rôle @responsable
                role = discord.utils.get(guild.roles, name="responsable")
                mention = f"<@&{role.id}>" if role else "@responsable"
                
                embed = discord.Embed(
                    title="🥗 RAPPEL – COMMANDES SALADES",
                    description=(
                        f"{mention}\n\n"
                        "Bonjour à tous,\n"
                        "Petit rappel pour penser à commander les salades pour la semaine.\n\n"
                        "Merci 🙏\n"
                        "— Matteo"
                    ),
                    color=discord.Color.green(),
                    timestamp=datetime.now()
                )
                await channel.send(embed=embed)
                logger.info(f"✅ Rappel salades envoyé dans #{channel.name} avec mention {mention}")
                break
    
    @rappel_salades.before_loop
    async def before_rappel_salades(self):
        """Attendre que le bot soit prêt avant de démarrer la tâche"""
        await self.bot.wait_until_ready()
    
    @commands.command(name="sondage")
    async def sondage(self, ctx):
        """Créer un sondage professionnel (Admin SIMON&CO uniquement)"""
        
        # VÉRIFICATION WHITELIST
        if not est_admin(ctx.author.id):
            try:
                await ctx.message.delete()
            except:
                pass
            return
        
        # Supprimer la commande pour discrétion
        try:
            await ctx.message.delete()
        except:
            pass
        
        # Ouvrir le modal
        modal = SondageModal()
        await ctx.send("📊 Création du sondage...", delete_after=1)
        
        # Envoyer un message temporaire pour attacher le modal
        temp_msg = await ctx.send("_Chargement..._")
        
        # Simuler une interaction pour ouvrir le modal
        # Note: Discord.py ne permet pas d'ouvrir un modal depuis une commande texte
        # Solution: Créer un bouton temporaire
        view = View(timeout=60)
        button = Button(label="📊 Créer le sondage", style=discord.ButtonStyle.primary)
        
        async def button_callback(interaction: discord.Interaction):
            if not est_admin(interaction.user.id):
                await interaction.response.send_message("❌ Accès refusé", ephemeral=True)
                return
            await interaction.response.send_modal(SondageModal())
        
        button.callback = button_callback
        view.add_item(button)
        
        await temp_msg.edit(
            content=f"✅ {ctx.author.mention} Clique sur le bouton ci-dessous pour créer ton sondage :",
            view=view
        )
        
        # Supprimer le message après 60 secondes
        await asyncio.sleep(60)
        try:
            await temp_msg.delete()
        except:
            pass
    
    @commands.command(name="embed")
    async def embed_panel(self, ctx):
        """Ouvrir le panel de création d'embeds professionnel (Admin uniquement)"""
        
        # VÉRIFICATION WHITELIST
        if not est_admin(ctx.author.id):
            try:
                await ctx.message.delete()
            except:
                pass
            return
        
        # Supprimer la commande
        try:
            await ctx.message.delete()
        except:
            pass
        
        # Créer l'embed du panel
        embed = discord.Embed(
            title="✨ PANEL DE CRÉATION EMBED",
            description=(
                "**Bienvenue dans le panel professionnel de création d'embeds !**\n\n"
                "🎨 Choisis le type de message que tu veux créer :\n\n"
                "**✨ Créer un Embed** - Embed personnalisé complet\n"
                "**📢 Annonce Simple** - Message d'annonce rapide\n"
                "**ℹ️ Info / Rappel** - Information ou rappel standard\n"
                "**⚠️ Alerte / Urgent** - Message urgent avec @everyone\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            ),
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        embed.set_author(
            name=f"Panel Admin • {ctx.author.display_name}",
            icon_url=ctx.author.display_avatar.url
        )
        embed.set_footer(text="🔒 Réservé aux administrateurs SIMON&CO")
        
        # Créer la vue persistante
        view = EmbedPanelView()
        
        # Envoyer le panel
        await ctx.send(embed=embed, view=view)
    
    @commands.command(name="test_rappel")
    async def test_rappel(self, ctx):
        """Tester le rappel des salades immédiatement (Admin uniquement)"""
        
        # VÉRIFICATION WHITELIST
        if not est_admin(ctx.author.id):
            try:
                await ctx.message.delete()
            except:
                pass
            return
        
        # Supprimer la commande
        try:
            await ctx.message.delete()
        except:
            pass
        
        # Trouver le salon #🎭︱・responsables
        channel = discord.utils.get(ctx.guild.text_channels, name="🎭︱・responsables")
        
        if not channel:
            await ctx.send("❌ Salon `#🎭︱・responsables` introuvable.", delete_after=5)
            return
        
        # Envoyer le rappel
        embed = discord.Embed(
            title="🥗 RAPPEL – COMMANDES SALADES",
            description=(
                "Bonjour à tous,\n"
                "Petit rappel pour penser à commander les salades pour la semaine.\n\n"
                "Merci 🙏\n"
                "— Matteo"
            ),
            color=discord.Color.green(),
            timestamp=datetime.now()
        )
        embed.set_footer(text="🧪 Test du rappel automatique")
        
        await channel.send(embed=embed)
        
        # Confirmer à l'admin
        await ctx.send(f"✅ Rappel de test envoyé dans {channel.mention}", delete_after=5)
        logger.info(f"🧪 Test rappel salades envoyé par {ctx.author.name}")

async def setup(bot):
    await bot.add_cog(AdminV3(bot))
    # Enregistrer les vues persistantes
    bot.add_view(SondageView())
    bot.add_view(EmbedPanelView())
