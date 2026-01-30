import discord
from discord.ext import commands
from datetime import datetime, timedelta
import asyncio

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.active_polls = {}
    
    @commands.command(name="poll")
    async def create_poll(self, ctx, durée: int, question, *options):
        """
        Créer un sondage
        Usage: !poll 60 "Quelle est votre couleur préférée?" "Rouge" "Bleu" "Vert"
        La durée est en minutes
        """
        if len(options) < 2:
            await ctx.send("❌ Il faut au moins 2 options!")
            return
        
        if len(options) > 10:
            await ctx.send("❌ Maximum 10 options!")
            return
        
        # Émojis de réaction
        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        
        # Créer l'embed
        embed = discord.Embed(
            title="📊 Sondage",
            description=f"**{question}**\n\n",
            color=discord.Color.blue(),
            timestamp=datetime.now()
        )
        
        # Ajouter les options
        for i, option in enumerate(options):
            embed.description += f"{emojis[i]} {option}\n"
        
        embed.set_footer(text=f"Sondage créé par {ctx.author.name} • Se termine dans {durée} min")
        embed.add_field(
            name="⏰ Durée",
            value=f"{durée} minute(s)",
            inline=True
        )
        embed.add_field(
            name="📈 Statut",
            value="En cours",
            inline=True
        )
        
        # Envoyer le sondage
        poll_message = await ctx.send(embed=embed)
        
        # Ajouter les réactions
        for i in range(len(options)):
            await poll_message.add_reaction(emojis[i])
        
        # Sauvegarder le sondage
        self.active_polls[poll_message.id] = {
            'question': question,
            'options': options,
            'author': ctx.author.id,
            'channel': ctx.channel.id,
            'end_time': datetime.now() + timedelta(minutes=durée)
        }
        
        # Supprimer le message de commande
        try:
            await ctx.message.delete()
        except:
            pass
        
        # Attendre la fin du sondage
        await asyncio.sleep(durée * 60)
        await self.end_poll(poll_message)
    
    @commands.command(name="quickpoll", aliases=["qp"])
    async def quick_poll(self, ctx, *, question):
        """
        Sondage rapide Oui/Non
        Usage: !quickpoll Est-ce que vous aimez les pizzas?
        """
        embed = discord.Embed(
            title="📊 Sondage Rapide",
            description=f"**{question}**",
            color=discord.Color.green(),
            timestamp=datetime.now()
        )
        embed.set_footer(text=f"Sondage par {ctx.author.name}")
        
        message = await ctx.send(embed=embed)
        await message.add_reaction("✅")
        await message.add_reaction("❌")
        
        try:
            await ctx.message.delete()
        except:
            pass
    
    @commands.command(name="pollresults", aliases=["resultats"])
    async def poll_results(self, ctx, message_id: int):
        """Afficher les résultats d'un sondage"""
        try:
            message = await ctx.channel.fetch_message(message_id)
            
            if not message.embeds:
                await ctx.send("❌ Ce message n'est pas un sondage!")
                return
            
            embed = message.embeds[0]
            
            # Compter les réactions
            results = []
            for reaction in message.reactions:
                if str(reaction.emoji) in ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]:
                    # -1 pour ne pas compter la réaction du bot
                    count = reaction.count - 1
                    results.append((str(reaction.emoji), count))
            
            # Créer l'embed des résultats
            total_votes = sum(r[1] for r in results)
            
            result_embed = discord.Embed(
                title="📊 Résultats du Sondage",
                description=embed.description.split('\n\n')[0],
                color=discord.Color.gold(),
                timestamp=datetime.now()
            )
            
            # Afficher les résultats
            result_text = ""
            for emoji, count in results:
                percentage = (count / total_votes * 100) if total_votes > 0 else 0
                bar_length = int(percentage / 10)
                bar = "█" * bar_length + "░" * (10 - bar_length)
                result_text += f"{emoji} {bar} {count} votes ({percentage:.1f}%)\n"
            
            result_embed.add_field(
                name=f"📈 Résultats ({total_votes} votes au total)",
                value=result_text or "Aucun vote",
                inline=False
            )
            
            result_embed.set_footer(text=f"Demandé par {ctx.author.name}")
            
            await ctx.send(embed=result_embed)
            
        except discord.NotFound:
            await ctx.send("❌ Message introuvable!")
        except Exception as e:
            await ctx.send(f"❌ Erreur: {e}")
    
    async def end_poll(self, message):
        """Terminer un sondage automatiquement"""
        try:
            # Rafraîchir le message
            message = await message.channel.fetch_message(message.id)
            
            if message.id not in self.active_polls:
                return
            
            poll_data = self.active_polls[message.id]
            
            # Compter les votes
            emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
            results = []
            total_votes = 0
            
            for i, reaction in enumerate(message.reactions):
                if str(reaction.emoji) in emojis:
                    count = reaction.count - 1  # -1 pour le bot
                    results.append((poll_data['options'][i], count))
                    total_votes += count
            
            # Trouver le gagnant
            winner = max(results, key=lambda x: x[1]) if results else ("Aucun", 0)
            
            # Créer l'embed des résultats
            result_embed = discord.Embed(
                title="📊 Sondage Terminé!",
                description=f"**{poll_data['question']}**\n\n",
                color=discord.Color.gold(),
                timestamp=datetime.now()
            )
            
            # Afficher les résultats
            for i, (option, count) in enumerate(results):
                percentage = (count / total_votes * 100) if total_votes > 0 else 0
                bar_length = int(percentage / 10)
                bar = "█" * bar_length + "░" * (10 - bar_length)
                
                is_winner = option == winner[0] and count > 0
                trophy = "🏆 " if is_winner else ""
                
                result_embed.description += f"{emojis[i]} {trophy}**{option}**\n"
                result_embed.description += f"{bar} {count} votes ({percentage:.1f}%)\n\n"
            
            result_embed.add_field(
                name="📈 Total",
                value=f"{total_votes} vote(s)",
                inline=True
            )
            
            if winner[1] > 0:
                result_embed.add_field(
                    name="🏆 Gagnant",
                    value=winner[0],
                    inline=True
                )
            
            result_embed.set_footer(text=f"Sondage créé par {self.bot.get_user(poll_data['author']).name}")
            
            # Éditer le message
            await message.edit(embed=result_embed)
            await message.clear_reactions()
            
            # Retirer de la liste des sondages actifs
            del self.active_polls[message.id]
            
        except Exception as e:
            print(f"Erreur lors de la fin du sondage: {e}")
    
    @commands.command(name="pollstop", aliases=["stoppoll"])
    @commands.has_permissions(manage_messages=True)
    async def stop_poll(self, ctx, message_id: int):
        """Arrêter un sondage manuellement"""
        try:
            message = await ctx.channel.fetch_message(message_id)
            
            if message.id in self.active_polls:
                await self.end_poll(message)
                await ctx.send("✅ Sondage terminé!")
            else:
                await ctx.send("❌ Ce sondage n'est pas actif ou n'existe pas.")
                
        except discord.NotFound:
            await ctx.send("❌ Message introuvable!")
        except Exception as e:
            await ctx.send(f"❌ Erreur: {e}")
    
    @commands.command(name="pollhelp")
    async def poll_help(self, ctx):
        """Aide pour les sondages"""
        embed = discord.Embed(
            title="📊 Système de Sondages",
            description="Voici comment utiliser les sondages:",
            color=discord.Color.blue()
        )
        
        embed.add_field(
            name="!poll <durée> \"question\" \"option1\" \"option2\" ...",
            value="Créer un sondage personnalisé (max 10 options)\nDurée en minutes",
            inline=False
        )
        
        embed.add_field(
            name="!quickpoll <question>",
            value="Sondage rapide Oui/Non (✅/❌)",
            inline=False
        )
        
        embed.add_field(
            name="!pollresults <message_id>",
            value="Afficher les résultats en temps réel",
            inline=False
        )
        
        embed.add_field(
            name="!pollstop <message_id>",
            value="Arrêter un sondage (admin uniquement)",
            inline=False
        )
        
        embed.add_field(
            name="📝 Exemples",
            value=(
                '`!poll 60 "Couleur préférée?" "Rouge" "Bleu" "Vert"`\n'
                '`!quickpoll Aimez-vous les pizzas?`\n'
                '`!pollresults 123456789`'
            ),
            inline=False
        )
        
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Poll(bot))
