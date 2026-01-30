import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput
from datetime import datetime
import json
import os

class TicketButton(Button):
    def __init__(self, label, emoji, custom_id, category_name):
        super().__init__(
            label=label,
            emoji=emoji,
            style=discord.ButtonStyle.primary,
            custom_id=custom_id
        )
        self.category_name = category_name
    
    async def callback(self, interaction: discord.Interaction):
        # Vérifier si l'utilisateur a déjà un ticket ouvert
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
        
        # Créer le ticket
        await interaction.response.defer(ephemeral=True)
        
        # Trouver ou créer la catégorie
        category = discord.utils.get(
            interaction.guild.categories,
            name=self.category_name
        )
        
        if not category:
            category = await interaction.guild.create_category(
                name=self.category_name,
                reason="Catégorie pour les tickets"
            )
        
        # Permissions du ticket
        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(
                read_messages=False
            ),
            interaction.user: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True,
                attach_files=True,
                embed_links=True
            ),
            interaction.guild.me: discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True,
                manage_channels=True,
                manage_messages=True
            )
        }
        
        # Ajouter les admins/mods
        admin_role = discord.utils.get(interaction.guild.roles, name="Admin")
        mod_role = discord.utils.get(interaction.guild.roles, name="Modérateur")
        
        if admin_role:
            overwrites[admin_role] = discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True
            )
        if mod_role:
            overwrites[mod_role] = discord.PermissionOverwrite(
                read_messages=True,
                send_messages=True
            )
        
        # Créer le salon
        ticket_number = len([c for c in category.channels if c.name.startswith("ticket-")]) + 1
        channel = await interaction.guild.create_text_channel(
            name=f"ticket-{ticket_number:04d}",
            category=category,
            topic=f"Ticket de {interaction.user.id}",
            overwrites=overwrites,
            reason=f"Ticket créé par {interaction.user}"
        )
        
        # Embed de bienvenue
        embed = discord.Embed(
            title="🎫 Nouveau Ticket",
            description=f"Bienvenue {interaction.user.mention} !\n\n"
                       f"L'équipe va te répondre dès que possible.\n"
                       f"En attendant, explique-nous ta demande en détail.",
            color=discord.Color.green(),
            timestamp=datetime.now()
        )
        embed.add_field(
            name="📋 Catégorie",
            value=self.category_name,
            inline=True
        )
        embed.add_field(
            name="👤 Créé par",
            value=interaction.user.mention,
            inline=True
        )
        embed.set_footer(
            text="Pour fermer ce ticket, clique sur le bouton 🔒"
        )
        
        # Boutons de contrôle
        view = TicketControlView()
        await channel.send(
            content=f"{interaction.user.mention}",
            embed=embed,
            view=view
        )
        
        await interaction.followup.send(
            f"✅ Ton ticket a été créé : {channel.mention}",
            ephemeral=True
        )

class TicketControlView(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Fermer", emoji="🔒", style=discord.ButtonStyle.danger, custom_id="close_ticket")
    async def close_ticket(self, interaction: discord.Interaction, button: Button):
        # Vérifier les permissions
        if not (interaction.user.guild_permissions.manage_channels or 
                interaction.channel.topic == f"Ticket de {interaction.user.id}"):
            await interaction.response.send_message(
                "❌ Tu n'as pas la permission de fermer ce ticket.",
                ephemeral=True
            )
            return
        
        embed = discord.Embed(
            title="🔒 Fermeture du ticket",
            description=f"Ticket fermé par {interaction.user.mention}\n"
                       f"Le salon sera supprimé dans 5 secondes...",
            color=discord.Color.red(),
            timestamp=datetime.now()
        )
        
        await interaction.response.send_message(embed=embed)
        
        # Sauvegarder le transcript (optionnel)
        await self.save_transcript(interaction.channel)
        
        # Supprimer le salon après 5 secondes
        await interaction.channel.delete(delay=5, reason=f"Ticket fermé par {interaction.user}")
    
    @discord.ui.button(label="Claim", emoji="✋", style=discord.ButtonStyle.success, custom_id="claim_ticket")
    async def claim_ticket(self, interaction: discord.Interaction, button: Button):
        # Seuls les mods/admins peuvent claim
        if not interaction.user.guild_permissions.manage_messages:
            await interaction.response.send_message(
                "❌ Seuls les modérateurs peuvent claim un ticket.",
                ephemeral=True
            )
            return
        
        embed = discord.Embed(
            title="✅ Ticket pris en charge",
            description=f"{interaction.user.mention} s'occupe de ce ticket.",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        
        await interaction.response.send_message(embed=embed)
        
        # Renommer le salon
        new_name = f"{interaction.channel.name}-{interaction.user.name}"[:100]
        await interaction.channel.edit(name=new_name)
    
    async def save_transcript(self, channel):
        """Sauvegarde l'historique du ticket"""
        try:
            messages = []
            async for message in channel.history(limit=None, oldest_first=True):
                messages.append(
                    f"[{message.created_at.strftime('%Y-%m-%d %H:%M:%S')}] "
                    f"{message.author}: {message.content}"
                )
            
            # Créer le dossier transcripts s'il n'existe pas
            os.makedirs("transcripts", exist_ok=True)
            
            # Sauvegarder
            filename = f"transcripts/ticket-{channel.name}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write("\n".join(messages))
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du transcript: {e}")

class TicketPanelView(View):
    def __init__(self):
        super().__init__(timeout=None)
        # Ajouter les boutons pour différents types de tickets
        self.add_item(TicketButton("💬 Support", "💬", "ticket_support", "🎫 TICKETS SUPPORT"))
        self.add_item(TicketButton("🐛 Bug Report", "🐛", "ticket_bug", "🎫 TICKETS BUGS"))
        self.add_item(TicketButton("💼 Partenariat", "💼", "ticket_partnership", "🎫 TICKETS PARTENARIATS"))
        self.add_item(TicketButton("❓ Autre", "❓", "ticket_other", "🎫 TICKETS DIVERS"))

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="ticketpanel", aliases=["createpanel"])
    async def ticket_panel(self, ctx):
        """Créer le panel de tickets (Accessible à tous)"""
        embed = discord.Embed(
            title="🎫 Système de Tickets",
            description=(
                "Besoin d'aide ? Ouvre un ticket !\n\n"
                "**Types de tickets disponibles :**\n"
                "💬 **Support** - Questions générales\n"
                "🐛 **Bug Report** - Signaler un bug\n"
                "💼 **Partenariat** - Demande de partenariat\n"
                "❓ **Autre** - Autres demandes\n\n"
                "Clique sur un bouton ci-dessous pour créer ton ticket."
            ),
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        embed.set_footer(text="Un seul ticket à la fois par personne")
        embed.set_thumbnail(url=ctx.guild.icon.url if ctx.guild.icon else None)
        
        view = TicketPanelView()
        await ctx.send(embed=embed, view=view)
        
        # Supprimer le message de commande
        try:
            await ctx.message.delete()
        except:
            pass
    
    @commands.command(name="closeticket", aliases=["close"])
    async def close_ticket(self, ctx):
        """Fermer un ticket manuellement"""
        if not ctx.channel.topic or not ctx.channel.topic.startswith("Ticket de"):
            await ctx.send("❌ Cette commande ne fonctionne que dans un ticket.")
            return
        
        embed = discord.Embed(
            title="🔒 Fermeture du ticket",
            description=f"Ticket fermé par {ctx.author.mention}\n"
                       f"Le salon sera supprimé dans 5 secondes...",
            color=discord.Color.red(),
            timestamp=datetime.now()
        )
        
        await ctx.send(embed=embed)
        await ctx.channel.delete(delay=5, reason=f"Ticket fermé par {ctx.author}")
    
    @commands.command(name="addticket", aliases=["add"])
    @commands.has_permissions(manage_channels=True)
    async def add_to_ticket(self, ctx, member: discord.Member):
        """Ajouter quelqu'un à un ticket"""
        if not ctx.channel.topic or not ctx.channel.topic.startswith("Ticket de"):
            await ctx.send("❌ Cette commande ne fonctionne que dans un ticket.")
            return
        
        await ctx.channel.set_permissions(
            member,
            read_messages=True,
            send_messages=True
        )
        
        await ctx.send(f"✅ {member.mention} a été ajouté au ticket.")
    
    @commands.command(name="removeticket", aliases=["remove"])
    @commands.has_permissions(manage_channels=True)
    async def remove_from_ticket(self, ctx, member: discord.Member):
        """Retirer quelqu'un d'un ticket"""
        if not ctx.channel.topic or not ctx.channel.topic.startswith("Ticket de"):
            await ctx.send("❌ Cette commande ne fonctionne que dans un ticket.")
            return
        
        await ctx.channel.set_permissions(member, overwrite=None)
        await ctx.send(f"✅ {member.mention} a été retiré du ticket.")

async def setup(bot):
    await bot.add_cog(Tickets(bot))
