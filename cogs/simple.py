import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput, Select
from datetime import datetime

class MainMenuView(View):
    """Menu principal avec tous les boutons d'accès"""
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="🎫 Ouvrir un Ticket", style=discord.ButtonStyle.primary, custom_id="open_ticket_menu")
    async def open_ticket_menu(self, interaction: discord.Interaction, button: Button):
        """Ouvrir le menu des tickets"""
        view = TicketTypeSelectView()
        embed = discord.Embed(
            title="🎫 Créer un Ticket",
            description="Sélectionne le type de ticket que tu veux ouvrir :",
            color=discord.Color.blue()
        )
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    @discord.ui.button(label="📊 Créer un Sondage", style=discord.ButtonStyle.success, custom_id="create_poll")
    async def create_poll(self, interaction: discord.Interaction, button: Button):
        """Créer un sondage"""
        modal = PollCreatorModal()
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label="📝 Créer une Annonce", style=discord.ButtonStyle.secondary, custom_id="create_announcement")
    async def create_announcement(self, interaction: discord.Interaction, button: Button):
        """Créer une annonce"""
        modal = AnnouncementModal()
        await interaction.response.send_modal(modal)

class TicketTypeSelectView(View):
    """Menu de sélection du type de ticket"""
    def __init__(self):
        super().__init__(timeout=60)
    
    @discord.ui.button(label="💬 Support Général", style=discord.ButtonStyle.primary, emoji="💬")
    async def support_ticket(self, interaction: discord.Interaction, button: Button):
        await self.create_ticket(interaction, "💬 Support", "🎫 SUPPORT")
    
    @discord.ui.button(label="🐛 Signaler un Bug", style=discord.ButtonStyle.danger, emoji="🐛")
    async def bug_ticket(self, interaction: discord.Interaction, button: Button):
        await self.create_ticket(interaction, "🐛 Bug", "🎫 BUGS")
    
    @discord.ui.button(label="💼 Partenariat", style=discord.ButtonStyle.success, emoji="💼")
    async def partnership_ticket(self, interaction: discord.Interaction, button: Button):
        await self.create_ticket(interaction, "💼 Partenariat", "🎫 PARTENARIATS")
    
    @discord.ui.button(label="❓ Autre Demande", style=discord.ButtonStyle.secondary, emoji="❓")
    async def other_ticket(self, interaction: discord.Interaction, button: Button):
        await self.create_ticket(interaction, "❓ Autre", "🎫 DIVERS")
    
    async def create_ticket(self, interaction: discord.Interaction, ticket_type: str, category_name: str):
        """Créer un ticket"""
        # Vérifier si l'utilisateur a déjà un ticket
        existing_ticket = discord.utils.get(
            interaction.guild.text_channels,
            topic=f"Ticket de {interaction.user.id}"
        )
        
        if existing_ticket:
            await interaction.response.send_message(
                f"❌ Tu as déjà un ticket ouvert : {existing_ticket.mention}",
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
            title=f"{ticket_type} - Ticket #{ticket_num:04d}",
            description=f"Bienvenue {interaction.user.mention} !\n\n"
                       f"📌 Un membre du staff va te répondre rapidement.\n"
                       f"💡 Explique ta demande en détail.\n"
                       f"🔒 Pour fermer ce ticket, clique sur le bouton rouge ci-dessous.",
            color=discord.Color.green(),
            timestamp=datetime.now()
        )
        embed.set_footer(text=f"Créé par {interaction.user.name}", icon_url=interaction.user.display_avatar.url)
        
        view = TicketControlView()
        await channel.send(content=f"{interaction.user.mention}", embed=embed, view=view)
        
        await interaction.followup.send(f"✅ Ton ticket a été créé : {channel.mention}", ephemeral=True)

class TicketControlView(View):
    """Boutons de contrôle dans un ticket"""
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Fermer le Ticket", emoji="🔒", style=discord.ButtonStyle.danger, custom_id="close_ticket_btn")
    async def close_ticket(self, interaction: discord.Interaction, button: Button):
        if not (interaction.user.guild_permissions.manage_channels or 
                interaction.channel.topic == f"Ticket de {interaction.user.id}"):
            await interaction.response.send_message("❌ Tu ne peux pas fermer ce ticket.", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="🔒 Ticket Fermé",
            description=f"Fermé par {interaction.user.mention}\nSuppression dans 5 secondes...",
            color=discord.Color.red()
        )
        await interaction.response.send_message(embed=embed)
        await interaction.channel.delete(delay=5, reason=f"Ticket fermé par {interaction.user}")

class PollCreatorModal(Modal):
    """Modal pour créer un sondage simplement"""
    def __init__(self):
        super().__init__(title="📊 Créer un Sondage")
        
        self.question = TextInput(
            label="Question du sondage",
            placeholder="Ex: Quelle est votre couleur préférée?",
            style=discord.TextStyle.short,
            required=True,
            max_length=200
        )
        self.add_item(self.question)
        
        self.options = TextInput(
            label="Options (une par ligne, max 10)",
            placeholder="Rouge\nBleu\nVert\nJaune",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=500
        )
        self.add_item(self.options)
        
        self.duration = TextInput(
            label="Durée en minutes (laisse vide pour illimité)",
            placeholder="Ex: 60",
            style=discord.TextStyle.short,
            required=False,
            max_length=4
        )
        self.add_item(self.duration)
    
    async def on_submit(self, interaction: discord.Interaction):
        # Parser les options
        options = [opt.strip() for opt in self.options.value.split('\n') if opt.strip()]
        
        if len(options) < 2:
            await interaction.response.send_message("❌ Il faut au moins 2 options!", ephemeral=True)
            return
        
        if len(options) > 10:
            await interaction.response.send_message("❌ Maximum 10 options!", ephemeral=True)
            return
        
        # Emojis
        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        
        # Créer l'embed
        embed = discord.Embed(
            title="📊 Sondage",
            description=f"**{self.question.value}**\n\n",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        
        for i, option in enumerate(options):
            embed.description += f"{emojis[i]} {option}\n"
        
        duration_text = f"{self.duration.value} min" if self.duration.value else "Illimité"
        embed.set_footer(text=f"Par {interaction.user.name} • Durée: {duration_text}", 
                        icon_url=interaction.user.display_avatar.url)
        
        # Envoyer
        await interaction.response.send_message(embed=embed)
        message = await interaction.original_response()
        
        # Ajouter les réactions
        for i in range(len(options)):
            await message.add_reaction(emojis[i])

class AnnouncementModal(Modal):
    """Modal pour créer une annonce"""
    def __init__(self):
        super().__init__(title="📝 Créer une Annonce")
        
        self.title = TextInput(
            label="Titre de l'annonce",
            placeholder="Ex: Nouvelle Fonctionnalité!",
            style=discord.TextStyle.short,
            required=True,
            max_length=100
        )
        self.add_item(self.title)
        
        self.message = TextInput(
            label="Message",
            placeholder="Écris ton annonce ici...",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=2000
        )
        self.add_item(self.message)
    
    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title=f"📢 {self.title.value}",
            description=self.message.value,
            color=discord.Color.gold(),
            timestamp=datetime.now()
        )
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        embed.set_footer(text=f"Annonce par {interaction.user.name}")
        
        await interaction.response.send_message(embed=embed)

class SimpleBot(commands.Cog):
    """Interface simplifiée pour PME"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="setup")
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx):
        """Créer le panneau principal (Admin uniquement)"""
        embed = discord.Embed(
            title="🎛️ Panneau de Contrôle LBB",
            description=(
                "Bienvenue sur le panneau de contrôle du serveur !\n\n"
                "**🎫 Ouvrir un Ticket**\n"
                "Besoin d'aide ? Clique sur le bouton bleu pour ouvrir un ticket privé.\n\n"
                "**📊 Créer un Sondage**\n"
                "Pose une question à la communauté avec un sondage interactif.\n\n"
                "**📝 Créer une Annonce**\n"
                "Partage une information importante avec tout le monde.\n\n"
                "Tout est simple : **1 clic = 1 action** ! 🚀"
            ),
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else None)
        embed.set_footer(text="Système simplifié pour PME")
        
        view = MainMenuView()
        await ctx.send(embed=embed, view=view)
        
        try:
            await ctx.message.delete()
        except:
            pass
    
    @commands.command(name="ticket")
    async def quick_ticket(self, ctx):
        """Ouvrir un ticket rapidement"""
        view = TicketTypeSelectView()
        embed = discord.Embed(
            title="🎫 Créer un Ticket",
            description="Sélectionne le type de ticket :",
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed, view=view)
    
    @commands.command(name="sondage")
    async def quick_poll(self, ctx):
        """Créer un sondage rapidement"""
        modal = PollCreatorModal()
        await ctx.send("✅ Un formulaire va s'ouvrir pour créer ton sondage!", delete_after=3)
        # Note: Les modals ne peuvent pas être envoyés via commande, seulement via interaction
        await ctx.send("💡 **Astuce:** Utilise le panneau principal avec le bouton '📊 Créer un Sondage' pour une interface plus simple!")

async def setup(bot):
    await bot.add_cog(SimpleBot(bot))
