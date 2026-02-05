import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput
from datetime import datetime
import os

# ============================================
# PANNEAU 1 : UNE DEMANDE / UN PROBLÈME
# ============================================

class PanelDemande(View):
    """Panneau pour les demandes générales - Persistant"""
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(
        label="🔦 Une demande ? un problème ?",
        style=discord.ButtonStyle.primary,
        custom_id="demande_button_persistent"
    )
    async def demande_button(self, interaction: discord.Interaction, button: Button):
        """Créer un ticket pour demande/problème"""
        await self.create_ticket(interaction, "🔦 Demande/Problème", "🎫 DEMANDES")
    
    async def create_ticket(self, interaction: discord.Interaction, ticket_type: str, category_name: str):
        # Vérifier si l'utilisateur a déjà un ticket
        existing_ticket = discord.utils.get(
            interaction.guild.text_channels,
            topic=f"Ticket de {interaction.user.id}"
        )
        
        if existing_ticket:
            await interaction.response.send_message(
                f"❌ **Tu as déjà un ticket ouvert !**\n\n"
                f"👉 Va ici : {existing_ticket.mention}\n"
                f"💡 Ferme-le d'abord avant d'en créer un nouveau.",
                ephemeral=True
            )
            return
        
        await interaction.response.defer(ephemeral=True)
        
        # Créer/trouver la catégorie
        category = discord.utils.get(interaction.guild.categories, name=category_name)
        if not category:
            category = await interaction.guild.create_category(name=category_name)
        
        # Permissions
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(
                read_messages=True, send_messages=True, attach_files=True, embed_links=True
            ),
            interaction.guild.me: discord.PermissionOverwrite(
                read_messages=True, send_messages=True, manage_channels=True
            )
        }
        
        # Ajouter staff
        for role_name in ["Admin", "Modérateur", "Staff", "Gérant"]:
            role = discord.utils.get(interaction.guild.roles, name=role_name)
            if role:
                overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        
        # Créer le salon
        ticket_num = len([c for c in category.channels if c.name.startswith("ticket-")]) + 1
        channel = await interaction.guild.create_text_channel(
            name=f"ticket-{ticket_num:04d}",
            category=category,
            topic=f"Ticket de {interaction.user.id}",
            overwrites=overwrites
        )
        
        # Message de bienvenue
        embed = discord.Embed(
            title=f"✅ Ticket #{ticket_num:04d} - {ticket_type}",
            description=(
                f"👋 Bonjour {interaction.user.mention} !\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"📝 **Explique ta demande ici :**\n"
                f"👉 Écris ton message ci-dessous\n"
                f"👉 Le staff te répond rapidement\n"
                f"👉 Seuls toi et le staff voient ce salon\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"🔒 **Pour fermer :**\n"
                f"👉 Clique sur le bouton rouge **\"🔒 Fermer\"** ci-dessous"
            ),
            color=discord.Color.green(),
            timestamp=datetime.now()
        )
        embed.set_footer(text=f"✅ Ticket créé automatiquement", icon_url=interaction.user.display_avatar.url)
        
        view = TicketControlView()
        await channel.send(content=f"{interaction.user.mention}", embed=embed, view=view)
        
        await interaction.followup.send(
            f"✅ **Parfait ! Ton ticket est créé !**\n\n"
            f"👉 **Clique ici pour y accéder :** {channel.mention}\n"
            f"💬 Écris ta demande dans ce salon\n"
            f"⏰ L'équipe te répond rapidement !",
            ephemeral=True
        )

# ============================================
# PANNEAU 2 : MAINTENANCES ET RÉPARATIONS
# ============================================

class PanelMaintenance(View):
    """Panneau pour les maintenances - Persistant"""
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(
        label="🛠️ Maintenances et Réparations",
        style=discord.ButtonStyle.danger,
        custom_id="maintenance_button_persistent"
    )
    async def maintenance_button(self, interaction: discord.Interaction, button: Button):
        """Créer un ticket pour maintenance"""
        await self.create_ticket(interaction, "🛠️ Maintenance", "🎫 MAINTENANCES")
    
    async def create_ticket(self, interaction: discord.Interaction, ticket_type: str, category_name: str):
        # Même logique que PanelDemande
        existing_ticket = discord.utils.get(
            interaction.guild.text_channels,
            topic=f"Ticket de {interaction.user.id}"
        )
        
        if existing_ticket:
            await interaction.response.send_message(
                f"❌ **Tu as déjà un ticket ouvert !**\n\n"
                f"👉 Va ici : {existing_ticket.mention}\n"
                f"💡 Ferme-le d'abord avant d'en créer un nouveau.",
                ephemeral=True
            )
            return
        
        await interaction.response.defer(ephemeral=True)
        
        category = discord.utils.get(interaction.guild.categories, name=category_name)
        if not category:
            category = await interaction.guild.create_category(name=category_name)
        
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            interaction.user: discord.PermissionOverwrite(
                read_messages=True, send_messages=True, attach_files=True, embed_links=True
            ),
            interaction.guild.me: discord.PermissionOverwrite(
                read_messages=True, send_messages=True, manage_channels=True
            )
        }
        
        for role_name in ["Admin", "Modérateur", "Staff", "Gérant"]:
            role = discord.utils.get(interaction.guild.roles, name=role_name)
            if role:
                overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        
        ticket_num = len([c for c in category.channels if c.name.startswith("ticket-")]) + 1
        channel = await interaction.guild.create_text_channel(
            name=f"ticket-{ticket_num:04d}",
            category=category,
            topic=f"Ticket de {interaction.user.id}",
            overwrites=overwrites
        )
        
        embed = discord.Embed(
            title=f"✅ Ticket #{ticket_num:04d} - {ticket_type}",
            description=(
                f"👋 Bonjour {interaction.user.mention} !\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"🛠️ **Explique ton problème technique :**\n"
                f"👉 Décris la panne ou réparation nécessaire\n"
                f"👉 L'équipe technique intervient rapidement\n"
                f"👉 Seuls toi et l'équipe voyez ce salon\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"🔒 **Pour fermer :**\n"
                f"👉 Clique sur le bouton rouge **\"🔒 Fermer\"** ci-dessous"
            ),
            color=discord.Color.orange(),
            timestamp=datetime.now()
        )
        embed.set_footer(text=f"✅ Ticket créé automatiquement", icon_url=interaction.user.display_avatar.url)
        
        view = TicketControlView()
        await channel.send(content=f"{interaction.user.mention}", embed=embed, view=view)
        
        await interaction.followup.send(
            f"✅ **Parfait ! Ton ticket maintenance est créé !**\n\n"
            f"👉 **Clique ici pour y accéder :** {channel.mention}\n"
            f"🛠️ Décris le problème dans ce salon\n"
            f"⏰ L'équipe technique te répond rapidement !",
            ephemeral=True
        )

# ============================================
# SYSTÈME DE FERMETURE AVANCÉ
# ============================================

class TicketControlView(View):
    """Bouton initial de fermeture - Persistant"""
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(
        label="🔒 Fermer",
        style=discord.ButtonStyle.danger,
        custom_id="close_ticket_initial_persistent"
    )
    async def close_ticket(self, interaction: discord.Interaction, button: Button):
        if not (interaction.user.guild_permissions.manage_channels or 
                interaction.channel.topic == f"Ticket de {interaction.user.id}"):
            await interaction.response.send_message(
                "❌ **Tu ne peux pas fermer ce ticket.**\n"
                "💡 Seul le créateur ou un administrateur peut le fermer.",
                ephemeral=True
            )
            return
        
        # Afficher la confirmation
        embed = discord.Embed(
            title="⚠️ Confirmation de fermeture",
            description="**Êtes-vous sûr de vouloir fermer ce ticket ?**",
            color=discord.Color.orange()
        )
        
        view = TicketConfirmView()
        await interaction.response.send_message(embed=embed, view=view)

class TicketConfirmView(View):
    """Confirmation : Fermer ou Annuler - Persistant"""
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(
        label="Fermer",
        style=discord.ButtonStyle.danger,
        custom_id="confirm_close_persistent"
    )
    async def confirm_close(self, interaction: discord.Interaction, button: Button):
        # Afficher les 3 options finales
        embed = discord.Embed(
            title="🔒 Ticket en cours de fermeture",
            description="**Choisissez une action :**",
            color=discord.Color.red()
        )
        
        view = TicketFinalActionsView()
        await interaction.response.edit_message(embed=embed, view=view)
    
    @discord.ui.button(
        label="Annuler",
        style=discord.ButtonStyle.secondary,
        custom_id="cancel_close_persistent"
    )
    async def cancel_close(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(
            title="✅ Fermeture annulée",
            description="Le ticket reste ouvert.",
            color=discord.Color.green()
        )
        await interaction.response.edit_message(embed=embed, view=None)
        await interaction.message.delete(delay=3)

class TicketFinalActionsView(View):
    """3 actions finales : Transcrire / Ouvrir / Supprimer - Persistant"""
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(
        label="📃 Transcrire",
        style=discord.ButtonStyle.primary,
        custom_id="transcript_ticket_persistent"
    )
    async def transcript_ticket(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer()
        
        # Créer le transcript
        transcript_channel = discord.utils.get(interaction.guild.text_channels, name="transcripts")
        if not transcript_channel:
            transcript_channel = await interaction.guild.create_text_channel(name="transcripts")
        
        # Sauvegarder l'historique COMPLET
        messages_text = []
        message_count = 0
        
        async for message in interaction.channel.history(limit=None, oldest_first=True):
            timestamp = message.created_at.strftime("%d/%m/%Y %H:%M:%S")
            author = f"{message.author.name} ({message.author.id})"
            content = message.content if message.content else "[Message vide ou embed]"
            
            # Ajouter les pièces jointes
            attachments = ""
            if message.attachments:
                attachments = " [Fichiers: " + ", ".join([att.filename for att in message.attachments]) + "]"
            
            messages_text.append(f"[{timestamp}] {author}: {content}{attachments}")
            message_count += 1
        
        # Créer fichier transcript
        if not os.path.exists("transcripts"):
            os.makedirs("transcripts")
        
        filename = f"transcripts/ticket-{interaction.channel.name}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"═══════════════════════════════════════════════════\n")
            f.write(f"       TRANSCRIPT DE TICKET - {interaction.channel.name.upper()}\n")
            f.write(f"═══════════════════════════════════════════════════\n\n")
            f.write(f"📅 Date de création : {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}\n")
            f.write(f"👤 Fermé par : {interaction.user.name} ({interaction.user.id})\n")
            f.write(f"💬 Nombre de messages : {message_count}\n")
            f.write(f"\n{'=' * 50}\n")
            f.write(f"HISTORIQUE COMPLET\n")
            f.write(f"{'=' * 50}\n\n")
            
            if messages_text:
                f.write("\n".join(messages_text))
            else:
                f.write("[Aucun message trouvé dans ce ticket]\n")
            
            f.write(f"\n\n{'=' * 50}\n")
            f.write(f"Fin du transcript - {message_count} message(s) archivé(s)\n")
            f.write(f"{'=' * 50}\n")
        
        # Envoyer dans #transcripts
        embed = discord.Embed(
            title=f"📃 Transcript - {interaction.channel.name}",
            description=(
                f"**Ticket fermé par :** {interaction.user.mention}\n"
                f"**Date :** {datetime.now().strftime('%d/%m/%Y à %H:%M')}\n"
                f"**Messages archivés :** {message_count}"
            ),
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        embed.set_footer(text=f"Ticket: {interaction.channel.name}")
        
        await transcript_channel.send(
            embed=embed,
            file=discord.File(filename)
        )
        
        await interaction.followup.send(
            f"✅ **Transcript sauvegardé avec succès !**\n\n"
            f"📁 **Fichier :** {filename}\n"
            f"💬 **Messages :** {message_count}\n"
            f"📍 **Salon :** {transcript_channel.mention}\n\n"
            f"⛔ Tu peux maintenant cliquer sur **⛔ Supprimer** pour fermer définitivement.",
            ephemeral=True
        )
    
    @discord.ui.button(
        label="🔓 Ouvrir",
        style=discord.ButtonStyle.success,
        custom_id="reopen_ticket_persistent"
    )
    async def reopen_ticket(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(
            title="🔓 Ticket réouvert",
            description=f"Le ticket a été réouvert par {interaction.user.mention}",
            color=discord.Color.green()
        )
        await interaction.response.edit_message(embed=embed, view=None)
        await interaction.message.delete(delay=3)
    
    @discord.ui.button(
        label="⛔ Supprimer",
        style=discord.ButtonStyle.danger,
        custom_id="delete_ticket_persistent"
    )
    async def delete_ticket(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(
            title="⛔ Suppression en cours",
            description=f"🗑️ Ce ticket sera supprimé dans **5 secondes**...\n\n⏰ Suppression par {interaction.user.mention}",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=False)
        
        # Supprimer le canal après 5 secondes
        import asyncio
        await asyncio.sleep(5)
        await interaction.channel.delete(reason=f"Ticket supprimé par {interaction.user}")

# ============================================
# SONDAGES ET ANNONCES (ADMINS UNIQUEMENT)
# ============================================

class PollCreatorModal(Modal):
    """Modal pour créer un sondage (Admins seulement)"""
    def __init__(self):
        super().__init__(title="📊 Créer un sondage (Admin)")
        
        self.question = TextInput(
            label="📝 Question du sondage",
            placeholder="Exemple : Quelle est votre pizza préférée ?",
            style=discord.TextStyle.short,
            required=True,
            max_length=200
        )
        self.add_item(self.question)
        
        self.options = TextInput(
            label="✅ Les choix (un par ligne, max 10)",
            placeholder="Margherita\n4 Fromages\nPepperoni\nVégétarienne",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=500
        )
        self.add_item(self.options)
        
        self.duration = TextInput(
            label="⏰ Durée en minutes (vide = illimité)",
            placeholder="60",
            style=discord.TextStyle.short,
            required=False,
            max_length=4
        )
        self.add_item(self.duration)
    
    async def on_submit(self, interaction: discord.Interaction):
        options = [opt.strip() for opt in self.options.value.split('\n') if opt.strip()]
        
        if len(options) < 2:
            await interaction.response.send_message("❌ Il faut au moins 2 choix !", ephemeral=True)
            return
        
        if len(options) > 10:
            await interaction.response.send_message("❌ Maximum 10 choix !", ephemeral=True)
            return
        
        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        
        embed = discord.Embed(
            title="📊 SONDAGE",
            description=f"**{self.question.value}**\n\n" + "\n".join([f"{emojis[i]} {opt}" for i, opt in enumerate(options)]),
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        
        duration_text = f"{self.duration.value} min" if self.duration.value else "Illimité"
        embed.set_footer(text=f"Par {interaction.user.name} • Durée: {duration_text}", 
                        icon_url=interaction.user.display_avatar.url)
        
        await interaction.response.send_message(embed=embed)
        message = await interaction.original_response()
        
        for i in range(len(options)):
            await message.add_reaction(emojis[i])

class AnnouncementModal(Modal):
    """Modal pour créer une annonce (Admins seulement)"""
    def __init__(self):
        super().__init__(title="📢 Créer une annonce")
        
        self.annonce_title = TextInput(
            label="📌 Titre de l'annonce",
            placeholder="Exemple : Réunion d'équipe mercredi",
            style=discord.TextStyle.short,
            required=True,
            max_length=100
        )
        self.add_item(self.annonce_title)
        
        self.annonce_message = TextInput(
            label="💬 Contenu de l'annonce",
            placeholder="Exemple : RDV mercredi à 14h en salle 2 pour discuter du projet",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=2000
        )
        self.add_item(self.annonce_message)
    
    async def on_submit(self, interaction: discord.Interaction):
        # Créer l'embed d'annonce
        embed = discord.Embed(
            title=f"📢 ANNONCE",
            description=(
                f"**{self.annonce_title.value}**\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n\n"
                f"{self.annonce_message.value}\n\n"
                f"━━━━━━━━━━━━━━━━━━━━━━"
            ),
            color=discord.Color.gold(),
            timestamp=datetime.now()
        )
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        embed.set_footer(text=f"📢 Annoncé par {interaction.user.name}")
        
        # Envoyer l'annonce
        await interaction.response.send_message(
            content="@everyone",
            embed=embed
        )

# ============================================
# COG PRINCIPAL AVEC COMMANDES
# ============================================

class SimpleBot(commands.Cog):
    """Interface V2 - Ultra simple et complète"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="setup_demande")
    @commands.has_permissions(administrator=True)
    async def setup_demande(self, ctx):
        """Créer le panneau DEMANDE/PROBLÈME (Admin uniquement)"""
        embed = discord.Embed(
            title="🔦 Une demande ? un problème ?",
            description=(
                "Pour créer un ticket réagissez avec : **🔦 Une demande ? un problème ?**\n\n"
                "Une fois que vous avez appuyé sur le bouton, veuillez cliquer sur le **#ticket-XXXX** (lien en bleu) "
                "Ce qui vous redirigera automatiquement dans le ticket créé."
            ),
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        embed.set_footer(text="✅ Système de tickets simplifié")
        
        view = PanelDemande()
        await ctx.send(embed=embed, view=view)
    
    @commands.command(name="setup_maintenance")
    @commands.has_permissions(administrator=True)
    async def setup_maintenance(self, ctx):
        """Créer le panneau MAINTENANCE (Admin uniquement)"""
        embed = discord.Embed(
            title="🛠️ Maintenances et Réparations",
            description=(
                "Pour créer un ticket réagissez avec : **🛠️ Maintenances et Réparations**\n\n"
                "Une fois que vous avez appuyé sur le bouton, veuillez cliquer sur le **#ticket-XXXX** (lien en bleu) "
                "Ce qui vous redirigera automatiquement dans le ticket créé."
            ),
            color=discord.Color.orange(),
            timestamp=datetime.now()
        )
        embed.set_footer(text="✅ Système de tickets maintenance")
        
        view = PanelMaintenance()
        await ctx.send(embed=embed, view=view)
    
    @commands.command(name="pollcreate")
    @commands.has_permissions(administrator=True)
    async def create_poll_admin(self, ctx):
        """Créer un sondage (Admin uniquement)"""
        modal = PollCreatorModal()
        await ctx.send("Ouvre le modal pour créer un sondage", ephemeral=True)
    
    @commands.command(name="announcement")
    @commands.has_permissions(administrator=True)
    async def create_announcement_admin(self, ctx, *, message: str):
        """Créer une annonce rapide (Admin uniquement)"""
        embed = discord.Embed(
            title="📢 ANNONCE",
            description=message,
            color=discord.Color.gold(),
            timestamp=datetime.now()
        )
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
        await ctx.send(embed=embed)
    
    @commands.command(name="panel_admin")
    async def panel_admin(self, ctx):
        """Créer le PANNEAU ADMIN COMPLET (Admin uniquement)"""
        
        # ========================================
        # WHITELIST ULTRA-STRICTE - SEULEMENT CES IDs
        # ========================================
        ADMINS_AUTORISES = [
            1184303630250164239,  # Ton ID
            1391756912823107716   # Créateur du serveur
        ]
        
        # VÉRIFICATION ABSOLUE : Si l'ID n'est pas dans la liste → BLOQUÉ
        if ctx.author.id not in ADMINS_AUTORISES:
            # Supprimer le message silencieusement
            try:
                await ctx.message.delete()
            except:
                pass
            # NE RIEN FAIRE - Ignorer totalement
            return
        
        # ========================================
        # SI ON ARRIVE ICI = ADMIN AUTORISÉ
        # ========================================
        
        # Supprimer la commande pour la discrétion
        try:
            await ctx.message.delete()
        except:
            pass
        
        embed = discord.Embed(
            title="🔧 PANNEAU ADMINISTRATION",
            description=(
                "**👑 Interface réservée aux Administrateurs**\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "**📊 COMMUNICATION**\n"
                "🔹 Créer un sondage\n\n"
                "**⚡ MODÉRATION**\n"
                "🔹 Kick un membre\n"
                "🔹 Ban un membre\n"
                "🔹 Timeout un membre\n"
                "🔹 Supprimer messages\n\n"
                "**🎫 TICKETS**\n"
                "🔹 Créer panneau Demandes\n"
                "🔹 Créer panneau Maintenance\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "✨ **Tout est accessible en un clic !**\n"
                "⚠️ **Seuls les admins peuvent utiliser ces boutons**\n\n"
                "💡 **CONSEIL** : Tape cette commande dans un salon privé admin-only"
            ),
            color=discord.Color.red(),
            timestamp=datetime.now()
        )
        embed.set_footer(text="🔐 Réservé aux Administrateurs")
        
        view = AdminPanelView()
        await ctx.send(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(SimpleBot(bot))

# ============================================
# PANNEAU ADMIN AVEC TOUS LES BOUTONS
# ============================================

class AdminPanelView(View):
    """Panneau admin complet - Persistant"""
    def __init__(self):
        super().__init__(timeout=None)
    
    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Vérifie que l'utilisateur est admin AVANT toute interaction"""
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message(
                "❌ **ACCÈS REFUSÉ**\n\n"
                "🔐 Ce panneau est **strictement réservé aux administrateurs**.\n"
                "Tu n'as pas les permissions nécessaires pour utiliser ces boutons.",
                ephemeral=True
            )
            return False
        return True
    
    @discord.ui.button(
        label="📊 Créer un Sondage",
        style=discord.ButtonStyle.primary,
        custom_id="admin_create_poll_persistent",
        row=0
    )
    async def admin_create_poll(self, interaction: discord.Interaction, button: Button):
        modal = PollCreatorModal()
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(
        label="👢 Kick un Membre",
        style=discord.ButtonStyle.danger,
        custom_id="admin_kick_persistent",
        row=1
    )
    async def admin_kick(self, interaction: discord.Interaction, button: Button):
        modal = KickModal()
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(
        label="🔨 Ban un Membre",
        style=discord.ButtonStyle.danger,
        custom_id="admin_ban_persistent",
        row=1
    )
    async def admin_ban(self, interaction: discord.Interaction, button: Button):
        modal = BanModal()
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(
        label="🔇 Timeout un Membre",
        style=discord.ButtonStyle.secondary,
        custom_id="admin_timeout_persistent",
        row=2
    )
    async def admin_timeout(self, interaction: discord.Interaction, button: Button):
        modal = TimeoutModal()
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(
        label="🗑️ Supprimer Messages",
        style=discord.ButtonStyle.secondary,
        custom_id="admin_clear_persistent",
        row=2
    )
    async def admin_clear(self, interaction: discord.Interaction, button: Button):
        modal = ClearModal()
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(
        label="🎫 Panneau Demandes",
        style=discord.ButtonStyle.success,
        custom_id="admin_setup_demande_persistent",
        row=3
    )
    async def admin_setup_demande(self, interaction: discord.Interaction, button: Button):
        
        embed = discord.Embed(
            title="🔦 Une demande ? un problème ?",
            description=(
                "Pour créer un ticket réagissez avec : **🔦 Une demande ? un problème ?**\n\n"
                "Une fois que vous avez appuyé sur le bouton, veuillez cliquer sur le **#ticket-XXXX** (lien en bleu) "
                "Ce qui vous redirigera automatiquement dans le ticket créé."
            ),
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        embed.set_footer(text="✅ Système de tickets simplifié")
        
        view = PanelDemande()
        await interaction.response.send_message(embed=embed, view=view)
    
    @discord.ui.button(
        label="🛠️ Panneau Maintenance",
        style=discord.ButtonStyle.success,
        custom_id="admin_setup_maintenance_persistent",
        row=3
    )
    async def admin_setup_maintenance(self, interaction: discord.Interaction, button: Button):
        
        embed = discord.Embed(
            title="🛠️ Maintenances et Réparations",
            description=(
                "Pour créer un ticket réagissez avec : **🛠️ Maintenances et Réparations**\n\n"
                "Une fois que vous avez appuyé sur le bouton, veuillez cliquer sur le **#ticket-XXXX** (lien en bleu) "
                "Ce qui vous redirigera automatiquement dans le ticket créé."
            ),
            color=discord.Color.orange(),
            timestamp=datetime.now()
        )
        embed.set_footer(text="✅ Système de tickets maintenance")
        
        view = PanelMaintenance()
        await interaction.response.send_message(embed=embed, view=view)

# ============================================
# MODALS POUR LE PANNEAU ADMIN
# ============================================

class KickModal(Modal):
    def __init__(self):
        super().__init__(title="👢 Kick un Membre")
        
        self.user_id = TextInput(
            label="ID du membre à kick",
            placeholder="Exemple : 123456789012345678",
            style=discord.TextStyle.short,
            required=True
        )
        self.add_item(self.user_id)
        
        self.reason = TextInput(
            label="Raison",
            placeholder="Exemple : Spam répété",
            style=discord.TextStyle.paragraph,
            required=False
        )
        self.add_item(self.reason)
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            member = await interaction.guild.fetch_member(int(self.user_id.value))
            reason = self.reason.value or "Aucune raison"
            
            if member.top_role >= interaction.user.top_role:
                await interaction.response.send_message("❌ Tu ne peux pas kick ce membre (rôle supérieur)", ephemeral=True)
                return
            
            await member.kick(reason=f"{reason} | Par {interaction.user}")
            
            embed = discord.Embed(
                title="👢 Membre Expulsé",
                description=f"✅ {member.mention} a été expulsé",
                color=discord.Color.orange()
            )
            embed.add_field(name="Raison", value=reason, inline=False)
            embed.add_field(name="Par", value=interaction.user.mention, inline=False)
            
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"❌ Erreur : {e}", ephemeral=True)

class BanModal(Modal):
    def __init__(self):
        super().__init__(title="🔨 Ban un Membre")
        
        self.user_id = TextInput(
            label="ID du membre à ban",
            placeholder="Exemple : 123456789012345678",
            style=discord.TextStyle.short,
            required=True
        )
        self.add_item(self.user_id)
        
        self.reason = TextInput(
            label="Raison",
            placeholder="Exemple : Insultes graves",
            style=discord.TextStyle.paragraph,
            required=False
        )
        self.add_item(self.reason)
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            member = await interaction.guild.fetch_member(int(self.user_id.value))
            reason = self.reason.value or "Aucune raison"
            
            if member.top_role >= interaction.user.top_role:
                await interaction.response.send_message("❌ Tu ne peux pas ban ce membre (rôle supérieur)", ephemeral=True)
                return
            
            await member.ban(reason=f"{reason} | Par {interaction.user}", delete_message_days=1)
            
            embed = discord.Embed(
                title="🔨 Membre Banni",
                description=f"✅ {member.mention} a été banni",
                color=discord.Color.red()
            )
            embed.add_field(name="Raison", value=reason, inline=False)
            embed.add_field(name="Par", value=interaction.user.mention, inline=False)
            
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"❌ Erreur : {e}", ephemeral=True)

class TimeoutModal(Modal):
    def __init__(self):
        super().__init__(title="🔇 Timeout un Membre")
        
        self.user_id = TextInput(
            label="ID du membre",
            placeholder="Exemple : 123456789012345678",
            style=discord.TextStyle.short,
            required=True
        )
        self.add_item(self.user_id)
        
        self.duration = TextInput(
            label="Durée (en minutes)",
            placeholder="Exemple : 60",
            style=discord.TextStyle.short,
            required=True
        )
        self.add_item(self.duration)
        
        self.reason = TextInput(
            label="Raison",
            placeholder="Exemple : Spam",
            style=discord.TextStyle.paragraph,
            required=False
        )
        self.add_item(self.reason)
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            member = await interaction.guild.fetch_member(int(self.user_id.value))
            duration = int(self.duration.value)
            reason = self.reason.value or "Aucune raison"
            
            from discord.utils import utcnow
            await member.timeout(utcnow() + discord.utils.timedelta(minutes=duration), reason=reason)
            
            embed = discord.Embed(
                title="🔇 Membre en Timeout",
                description=f"✅ {member.mention} est en timeout",
                color=discord.Color.orange()
            )
            embed.add_field(name="Durée", value=f"{duration} minutes", inline=False)
            embed.add_field(name="Raison", value=reason, inline=False)
            
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"❌ Erreur : {e}", ephemeral=True)

class ClearModal(Modal):
    def __init__(self):
        super().__init__(title="🗑️ Supprimer Messages")
        
        self.amount = TextInput(
            label="Nombre de messages à supprimer",
            placeholder="Exemple : 50 (max 100)",
            style=discord.TextStyle.short,
            required=True
        )
        self.add_item(self.amount)
    
    async def on_submit(self, interaction: discord.Interaction):
        try:
            amount = int(self.amount.value)
            
            if amount < 1 or amount > 100:
                await interaction.response.send_message("❌ Le nombre doit être entre 1 et 100", ephemeral=True)
                return
            
            await interaction.response.defer(ephemeral=True)
            deleted = await interaction.channel.purge(limit=amount)
            
            await interaction.followup.send(f"✅ {len(deleted)} message(s) supprimé(s)", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ Erreur : {e}", ephemeral=True)

async def setup(bot):
    await bot.add_cog(SimpleBot(bot))
