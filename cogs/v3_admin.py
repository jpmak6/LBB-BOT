import discord
from discord.ext import commands
from discord.ui import Button, View, Modal, TextInput
from datetime import datetime
import asyncio

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
# SONDAGE V3.1 - ULTRA SIMPLE
# ============================================

class SondageModal(Modal):
    """Modal pour créer un sondage professionnel"""
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
            label="🅲 Option 3 (Optionnelle)",
            placeholder="Exemple : Chocolat chaud",
            style=discord.TextStyle.short,
            required=False,
            max_length=80
        )
        self.add_item(self.option3)
        
        self.option4 = TextInput(
            label="🅳 Option 4 (Optionnelle)",
            placeholder="Exemple : Aucun",
            style=discord.TextStyle.short,
            required=False,
            max_length=80
        )
        self.add_item(self.option4)
    
    async def on_submit(self, interaction: discord.Interaction):
        # Créer les options
        options = [self.option1.value, self.option2.value]
        if self.option3.value:
            options.append(self.option3.value)
        if self.option4.value:
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
            if str(reaction.emoji) in ["🅰️", "🅱️", "🅲", "🅳"]:
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
# EMBED V3.1 - ULTRA SIMPLE
# ============================================

class EmbedModal(Modal):
    """Modal pour créer un embed professionnel sans coder"""
    def __init__(self):
        super().__init__(title="✨ Créer un Message Embed")
        
        self.titre = TextInput(
            label="📌 Titre de l'embed",
            placeholder="Exemple : Annonce Importante",
            style=discord.TextStyle.short,
            required=True,
            max_length=256
        )
        self.add_item(self.titre)
        
        self.description = TextInput(
            label="📝 Description / Message",
            placeholder="Exemple : Réunion mercredi à 14h dans la salle 2...",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=4000
        )
        self.add_item(self.description)
        
        self.couleur = TextInput(
            label="🎨 Couleur (bleu/rouge/vert/jaune/violet/orange)",
            placeholder="Exemple : bleu",
            style=discord.TextStyle.short,
            required=False,
            max_length=20
        )
        self.add_item(self.couleur)
        
        self.footer = TextInput(
            label="📄 Texte en bas (optionnel)",
            placeholder="Exemple : Direction SIMON&CO",
            style=discord.TextStyle.short,
            required=False,
            max_length=100
        )
        self.add_item(self.footer)
        
        self.mention = TextInput(
            label="📢 Mentionner @everyone ? (oui/non)",
            placeholder="non",
            style=discord.TextStyle.short,
            required=False,
            max_length=3
        )
        self.add_item(self.mention)
    
    async def on_submit(self, interaction: discord.Interaction):
        # Définir la couleur
        couleurs = {
            "bleu": discord.Color.blue(),
            "rouge": discord.Color.red(),
            "vert": discord.Color.green(),
            "jaune": discord.Color.gold(),
            "violet": discord.Color.purple(),
            "orange": discord.Color.orange(),
        }
        
        couleur_choisie = couleurs.get(
            self.couleur.value.lower().strip() if self.couleur.value else "",
            discord.Color.blue()
        )
        
        # Créer l'embed
        embed = discord.Embed(
            title=self.titre.value,
            description=self.description.value,
            color=couleur_choisie,
            timestamp=datetime.now()
        )
        
        # Ajouter l'auteur
        embed.set_author(
            name=interaction.user.display_name,
            icon_url=interaction.user.display_avatar.url
        )
        
        # Ajouter le footer si spécifié
        if self.footer.value:
            embed.set_footer(text=self.footer.value)
        else:
            embed.set_footer(text="SIMON&CO")
        
        # Envoyer l'embed dans le canal
        mention_everyone = self.mention.value and self.mention.value.lower() in ["oui", "yes", "o", "y"]
        
        # Confirmer à l'utilisateur
        await interaction.response.send_message(
            "✅ Embed créé avec succès !",
            ephemeral=True
        )
        
        # Envoyer l'embed dans le canal
        await interaction.channel.send(
            content="@everyone" if mention_everyone else None,
            embed=embed
        )

# ============================================
# COG PRINCIPAL V3.1
# ============================================

class AdminV3(commands.Cog):
    """Commandes exclusives V3.1 pour admins SIMON&CO"""
    
    def __init__(self, bot):
        self.bot = bot
    
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
    async def embed(self, ctx):
        """Créer un message embed personnalisé (Admin SIMON&CO uniquement)"""
        
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
        
        # Créer un bouton pour ouvrir le modal
        view = View(timeout=60)
        button = Button(label="✨ Créer l'embed", style=discord.ButtonStyle.success)
        
        async def button_callback(interaction: discord.Interaction):
            if not est_admin(interaction.user.id):
                await interaction.response.send_message("❌ Accès refusé", ephemeral=True)
                return
            await interaction.response.send_modal(EmbedModal())
        
        button.callback = button_callback
        view.add_item(button)
        
        msg = await ctx.send(
            f"✅ {ctx.author.mention} Clique sur le bouton ci-dessous pour créer ton embed :",
            view=view
        )
        
        # Supprimer le message après 60 secondes
        await asyncio.sleep(60)
        try:
            await msg.delete()
        except:
            pass

async def setup(bot):
    await bot.add_cog(AdminV3(bot))
    # Enregistrer la vue persistante pour les sondages
    bot.add_view(SondageView(None))
