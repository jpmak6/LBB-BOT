import discord
from discord.ext import commands
import os
import logging
from dotenv import load_dotenv
from datetime import datetime
import asyncio

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('discord')

# Chargement des variables d'environnement
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

if not TOKEN:
    logger.error("❌ Token Discord introuvable! Vérifiez votre fichier .env")
    exit(1)

# Configuration des intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.guilds = True
intents.presences = True

# Initialisation du bot
bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

@bot.event
async def on_ready():
    """Événement déclenché quand le bot est prêt"""
    logger.info(f"✅ Connecté en tant que {bot.user} (ID: {bot.user.id})")
    logger.info(f"🌐 Connecté à {len(bot.guilds)} serveur(s)")
    
    # Charger les cogs
    await load_extensions()
    
    # Définir l'activité du bot
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.watching,
            name="!aide pour les commandes"
        )
    )
    
    logger.info("🎉 Bot prêt et opérationnel!")

async def load_extensions():
    """Charger tous les modules (cogs)"""
    cogs = ['simple', 'tickets', 'embeds', 'polls']
    
    for cog in cogs:
        try:
            await bot.load_extension(f'cogs.{cog}')
            logger.info(f"✅ Module chargé: {cog}")
        except Exception as e:
            logger.error(f"❌ Erreur lors du chargement de {cog}: {e}")

@bot.event
async def on_member_join(member):
    """Message de bienvenue pour les nouveaux membres"""
    try:
        channel = discord.utils.get(member.guild.text_channels, name="general") or \
                  discord.utils.get(member.guild.text_channels, name="bienvenue")
        
        if channel:
            embed = discord.Embed(
                title="🎉 Nouveau membre !",
                description=f"Bienvenue {member.mention} sur **{member.guild.name}** !",
                color=discord.Color.green(),
                timestamp=datetime.now()
            )
            embed.set_thumbnail(url=member.display_avatar.url)
            embed.add_field(
                name="👥 Membres",
                value=f"Nous sommes maintenant **{member.guild.member_count}** membres !",
                inline=False
            )
            embed.set_footer(text=f"ID: {member.id}")
            
            await channel.send(embed=embed)
            logger.info(f"✅ Message de bienvenue envoyé pour {member.name}")
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'envoi du message de bienvenue: {e}")

@bot.event
async def on_member_remove(member):
    """Message quand un membre quitte"""
    try:
        channel = discord.utils.get(member.guild.text_channels, name="general")
        if channel:
            await channel.send(f"👋 {member.name} a quitté le serveur...")
            logger.info(f"📤 {member.name} a quitté le serveur")
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'envoi du message de départ: {e}")

@bot.event
async def on_command_error(ctx, error):
    """Gestion globale des erreurs"""
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Commande inconnue. Tape `!aide` pour voir les commandes disponibles.")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ Tu n'as pas la permission d'utiliser cette commande.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"❌ Argument manquant. Usage: `{ctx.prefix}{ctx.command.signature}`")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"⏱️ Cette commande est en cooldown. Réessaye dans {error.retry_after:.1f}s")
    else:
        logger.error(f"❌ Erreur non gérée: {error}", exc_info=error)
        await ctx.send("❌ Une erreur est survenue lors de l'exécution de la commande.")

@bot.command(name="aide", aliases=["help", "h"])
async def aide(ctx):
    """Affiche toutes les commandes disponibles"""
    embed = discord.Embed(
        title="📚 Guide du Bot - Version PME Simplifiée",
        description=(
            "**🎛️ PANNEAU PRINCIPAL (Le plus simple !)**\n"
            "`!setup` - Créer le panneau interactif avec tous les boutons\n"
            "→ *1 clic = 1 action, plus besoin de commandes !*\n\n"
            "---\n\n"
            "**🚀 ACCÈS RAPIDE (Pour Tous)**"
        ),
        color=discord.Color.blue(),
        timestamp=datetime.now()
    )
    
    embed.add_field(
        name="🎫 Tickets (Tout le monde)",
        value=(
            "**Via le panneau** : Clique sur 🎫\n"
            "**Via commande** : `!ticket`\n"
            "→ Ouvre un ticket privé instantanément"
        ),
        inline=False
    )
    
    embed.add_field(
        name="📊 Sondages (Tout le monde)",
        value=(
            "**Via le panneau** : Clique sur 📊\n"
            "**Via commandes** :\n"
            "• `!poll 60 \"Question?\" \"Option1\" \"Option2\"`\n"
            "• `!quickpoll Question simple?` (Oui/Non)\n"
            "→ Crée un sondage en 2 secondes"
        ),
        inline=False
    )
    
    embed.add_field(
        name="📝 Annonces (Tout le monde)",
        value=(
            "**Via le panneau** : Clique sur 📝\n"
            "**Via commande** : `!announcement Message`\n"
            "→ Annonce stylisée automatique"
        ),
        inline=False
    )
    
    embed.add_field(
        name="📌 Informations",
        value=(
            "`!ping` - Latence du bot\n"
            "`!info` - Infos du bot\n"
            "`!serveurinfo` - Stats du serveur\n"
            "`!userinfo [@user]` - Infos d'un membre"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🛡️ Modération (Staff uniquement)",
        value=(
            "`!clear <nombre>` - Supprimer messages\n"
            "`!kick @user raison` - Expulser\n"
            "`!ban @user raison` - Bannir\n"
            "`!timeout @user <durée> <unité>` - Timeout\n"
            "→ *Unités: s, m, h, d*"
        ),
        inline=False
    )
    
    embed.add_field(
        name="💡 CONSEIL POUR DÉMARRER",
        value=(
            "**1.** Tape `!setup` dans un salon\n"
            "**2.** Le panneau apparaît avec des boutons\n"
            "**3.** Tout le monde peut cliquer et utiliser !\n\n"
            "✨ *C'est aussi simple que ça !*"
        ),
        inline=False
    )
    
    embed.set_footer(text=f"Bot simplifié pour PME • Demandé par {ctx.author.name}", 
                    icon_url=ctx.author.display_avatar.url)
    await ctx.send(embed=embed)

@bot.command(name="regles", aliases=["règles", "rules"])
async def regles(ctx):
    """Affiche les règles du serveur"""
    embed = discord.Embed(
        title="📜 Règles du serveur",
        description="Merci de respecter ces règles pour une bonne ambiance !",
        color=discord.Color.gold(),
        timestamp=datetime.now()
    )
    
    embed.add_field(name="1️⃣ Respect", value="Respectez tous les membres du serveur", inline=False)
    embed.add_field(name="2️⃣ Pas de spam", value="Ne spammez pas les salons", inline=False)
    embed.add_field(name="3️⃣ Contenu approprié", value="Pas de contenu NSFW, illégal ou offensant", inline=False)
    embed.add_field(name="4️⃣ Pas de pub", value="Pas de publicité sans permission", inline=False)
    embed.set_footer(text="En cas de non-respect, des sanctions seront appliquées")
    
    await ctx.send(embed=embed)

@bot.command(name="ping")
async def ping(ctx):
    """Affiche la latence du bot"""
    latency = round(bot.latency * 1000)
    emoji = "🟢" if latency < 100 else "🟡" if latency < 200 else "🔴"
    status = "Excellent" if latency < 100 else "Bon" if latency < 200 else "Lent"
    
    embed = discord.Embed(
        title="🏓 Pong!",
        description=f"{emoji} Latence: **{latency}ms** ({status})",
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)

@bot.command(name="info", aliases=["botinfo"])
async def info(ctx):
    """Informations sur le bot"""
    embed = discord.Embed(title="🤖 Informations sur le bot", color=discord.Color.purple(), timestamp=datetime.now())
    embed.set_thumbnail(url=bot.user.display_avatar.url)
    embed.add_field(name="👤 Nom", value=bot.user.name, inline=True)
    embed.add_field(name="🆔 ID", value=bot.user.id, inline=True)
    embed.add_field(name="🌐 Serveurs", value=len(bot.guilds), inline=True)
    embed.add_field(name="👥 Membres", value=sum(g.member_count for g in bot.guilds), inline=True)
    embed.add_field(name="🏓 Ping", value=f"{round(bot.latency * 1000)}ms", inline=True)
    embed.add_field(name="🐍 Discord.py", value=discord.__version__, inline=True)
    embed.set_footer(text=f"Demandé par {ctx.author.name}", icon_url=ctx.author.display_avatar.url)
    
    await ctx.send(embed=embed)

@bot.command(name="serveurinfo", aliases=["serverinfo", "si"])
async def serveurinfo(ctx):
    """Affiche les informations du serveur"""
    guild = ctx.guild
    embed = discord.Embed(title=f"📊 Informations sur {guild.name}", color=discord.Color.blue(), timestamp=datetime.now())
    
    if guild.icon:
        embed.set_thumbnail(url=guild.icon.url)
    
    embed.add_field(name="🆔 ID", value=guild.id, inline=True)
    embed.add_field(name="👑 Propriétaire", value=guild.owner.mention, inline=True)
    embed.add_field(name="📅 Créé le", value=guild.created_at.strftime("%d/%m/%Y"), inline=True)
    embed.add_field(name="👥 Membres", value=guild.member_count, inline=True)
    embed.add_field(name="💬 Salons", value=len(guild.text_channels), inline=True)
    embed.add_field(name="🔊 Vocaux", value=len(guild.voice_channels), inline=True)
    embed.add_field(name="🎭 Rôles", value=len(guild.roles), inline=True)
    embed.add_field(name="😊 Emojis", value=len(guild.emojis), inline=True)
    embed.add_field(name="🚀 Boost", value=f"Niveau {guild.premium_tier} ({guild.premium_subscription_count} boosts)", inline=True)
    
    await ctx.send(embed=embed)

@bot.command(name="userinfo", aliases=["ui", "user"])
async def userinfo(ctx, member: discord.Member = None):
    """Affiche les informations d'un membre"""
    member = member or ctx.author
    embed = discord.Embed(title=f"👤 Informations sur {member.name}", color=member.color, timestamp=datetime.now())
    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="🆔 ID", value=member.id, inline=True)
    embed.add_field(name="📛 Pseudo", value=member.display_name, inline=True)
    embed.add_field(name="🤖 Bot", value="Oui" if member.bot else "Non", inline=True)
    embed.add_field(name="📅 Compte créé", value=member.created_at.strftime("%d/%m/%Y"), inline=True)
    embed.add_field(name="📥 A rejoint", value=member.joined_at.strftime("%d/%m/%Y"), inline=True)
    embed.add_field(name="🎭 Rôles", value=f"{len(member.roles)-1} rôles", inline=True)
    
    if member.premium_since:
        embed.add_field(name="💎 Boost depuis", value=member.premium_since.strftime("%d/%m/%Y"), inline=True)
    
    await ctx.send(embed=embed)

@bot.command(name="clear", aliases=["purge", "clean"])
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 10):
    """Supprime un nombre de messages (admin seulement)"""
    if amount < 1 or amount > 100:
        await ctx.send("❌ Le nombre doit être entre 1 et 100")
        return
    
    deleted = await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"✅ {len(deleted)-1} message(s) supprimé(s)")
    await msg.delete(delay=3)

@bot.command(name="kick")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="Aucune raison fournie"):
    """Expulser un membre du serveur"""
    if member.top_role >= ctx.author.top_role:
        await ctx.send("❌ Tu ne peux pas expulser ce membre (rôle supérieur ou égal).")
        return
    
    try:
        await member.kick(reason=f"{reason} | Par {ctx.author}")
        embed = discord.Embed(title="👢 Membre Expulsé", description=f"{member.mention} a été expulsé du serveur", color=discord.Color.orange(), timestamp=datetime.now())
        embed.add_field(name="👤 Membre", value=f"{member} ({member.id})", inline=True)
        embed.add_field(name="🛡️ Modérateur", value=ctx.author.mention, inline=True)
        embed.add_field(name="📝 Raison", value=reason, inline=False)
        await ctx.send(embed=embed)
        logger.info(f"{member} expulsé par {ctx.author} - Raison: {reason}")
    except Exception as e:
        await ctx.send(f"❌ Erreur lors de l'expulsion: {e}")

@bot.command(name="ban")
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="Aucune raison fournie"):
    """Bannir un membre du serveur"""
    if member.top_role >= ctx.author.top_role:
        await ctx.send("❌ Tu ne peux pas bannir ce membre (rôle supérieur ou égal).")
        return
    
    try:
        await member.ban(reason=f"{reason} | Par {ctx.author}", delete_message_days=1)
        embed = discord.Embed(title="🔨 Membre Banni", description=f"{member.mention} a été banni du serveur", color=discord.Color.red(), timestamp=datetime.now())
        embed.add_field(name="👤 Membre", value=f"{member} ({member.id})", inline=True)
        embed.add_field(name="🛡️ Modérateur", value=ctx.author.mention, inline=True)
        embed.add_field(name="📝 Raison", value=reason, inline=False)
        await ctx.send(embed=embed)
        logger.info(f"{member} banni par {ctx.author} - Raison: {reason}")
    except Exception as e:
        await ctx.send(f"❌ Erreur lors du bannissement: {e}")

@bot.command(name="unban")
@commands.has_permissions(ban_members=True)
async def unban(ctx, user_id: int):
    """Débannir un utilisateur"""
    try:
        user = await bot.fetch_user(user_id)
        await ctx.guild.unban(user, reason=f"Débanni par {ctx.author}")
        embed = discord.Embed(title="✅ Membre Débanni", description=f"{user} a été débanni", color=discord.Color.green(), timestamp=datetime.now())
        embed.add_field(name="👤 Utilisateur", value=f"{user} ({user.id})", inline=True)
        embed.add_field(name="🛡️ Modérateur", value=ctx.author.mention, inline=True)
        await ctx.send(embed=embed)
        logger.info(f"{user} débanni par {ctx.author}")
    except discord.NotFound:
        await ctx.send("❌ Utilisateur introuvable ou non banni.")
    except Exception as e:
        await ctx.send(f"❌ Erreur: {e}")

@bot.command(name="timeout", aliases=["mute"])
@commands.has_permissions(moderate_members=True)
async def timeout(ctx, member: discord.Member, duration: int, unit: str = "m", *, reason="Aucune raison"):
    """Mettre un membre en timeout"""
    multipliers = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}
    if unit.lower() not in multipliers:
        await ctx.send("❌ Unité invalide! Utilise: s, m, h, ou d")
        return
    
    timeout_duration = duration * multipliers[unit.lower()]
    if timeout_duration > 2419200:
        await ctx.send("❌ La durée maximale est de 28 jours!")
        return
    
    try:
        from discord.utils import utcnow
        await member.timeout(utcnow() + discord.utils.timedelta(seconds=timeout_duration), reason=f"{reason} | Par {ctx.author}")
        
        time_display = f"{duration}{unit}"
        embed = discord.Embed(title="🔇 Membre en Timeout", description=f"{member.mention} a été mis en timeout", color=discord.Color.orange(), timestamp=datetime.now())
        embed.add_field(name="👤 Membre", value=member.mention, inline=True)
        embed.add_field(name="⏰ Durée", value=time_display, inline=True)
        embed.add_field(name="🛡️ Modérateur", value=ctx.author.mention, inline=True)
        embed.add_field(name="📝 Raison", value=reason, inline=False)
        await ctx.send(embed=embed)
        logger.info(f"{member} en timeout ({time_display}) par {ctx.author}")
    except Exception as e:
        await ctx.send(f"❌ Erreur: {e}")

@bot.command(name="untimeout", aliases=["unmute"])
@commands.has_permissions(moderate_members=True)
async def untimeout(ctx, member: discord.Member):
    """Retirer le timeout d'un membre"""
    try:
        await member.timeout(None, reason=f"Timeout retiré par {ctx.author}")
        await ctx.send(f"✅ {member.mention} n'est plus en timeout.")
        logger.info(f"Timeout retiré de {member} par {ctx.author}")
    except Exception as e:
        await ctx.send(f"❌ Erreur: {e}")

# Lancement du bot
if __name__ == "__main__":
    try:
        logger.info("🚀 Démarrage du bot...")
        bot.run(TOKEN)
    except discord.LoginFailure:
        logger.error("❌ Token invalide! Vérifiez votre fichier .env")
    except Exception as e:
        logger.error(f"❌ Erreur critique: {e}", exc_info=True)
