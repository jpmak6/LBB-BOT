import discord
from discord.ext import commands
from discord.ui import Modal, TextInput
import json
from datetime import datetime

class EmbedCreator(Modal):
    def __init__(self):
        super().__init__(title="📝 Créer un Embed")
        
        self.title_input = TextInput(
            label="Titre",
            placeholder="Titre de l'embed",
            required=True,
            max_length=256
        )
        self.add_item(self.title_input)
        
        self.description_input = TextInput(
            label="Description",
            placeholder="Description de l'embed",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=4000
        )
        self.add_item(self.description_input)
        
        self.color_input = TextInput(
            label="Couleur (hex, ex: #FF0000)",
            placeholder="#3498db",
            required=False,
            max_length=7
        )
        self.add_item(self.color_input)
        
        self.footer_input = TextInput(
            label="Footer (optionnel)",
            placeholder="Texte en bas de l'embed",
            required=False,
            max_length=2048
        )
        self.add_item(self.footer_input)
        
        self.thumbnail_input = TextInput(
            label="URL Image (optionnel)",
            placeholder="https://exemple.com/image.png",
            required=False
        )
        self.add_item(self.thumbnail_input)
    
    async def on_submit(self, interaction: discord.Interaction):
        # Traiter la couleur
        try:
            color_hex = self.color_input.value or "#3498db"
            if not color_hex.startswith("#"):
                color_hex = "#" + color_hex
            color = discord.Color(int(color_hex[1:], 16))
        except:
            color = discord.Color.blue()
        
        # Créer l'embed
        embed = discord.Embed(
            title=self.title_input.value,
            description=self.description_input.value,
            color=color,
            timestamp=datetime.now()
        )
        
        if self.footer_input.value:
            embed.set_footer(text=self.footer_input.value)
        
        if self.thumbnail_input.value:
            try:
                embed.set_thumbnail(url=self.thumbnail_input.value)
            except:
                pass
        
        await interaction.response.send_message(embed=embed)

class Embeds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="embed")
    async def create_embed(self, ctx):
        """Créer un embed personnalisé (Accessible à tous)"""
        modal = EmbedCreator()
        await ctx.send("✅ Clique sur le bouton pour ouvrir le créateur d'embed!", view=EmbedModalView(modal))
        try:
            await ctx.message.delete()
        except:
            pass
    
    @commands.command(name="embedsimple")
    async def embed_simple(self, ctx, *, args):
        """
        Créer un embed rapidement (Accessible à tous)
        Usage: !embedsimple titre="Mon Titre" description="Ma description" couleur=#FF0000
        """
        try:
            # Parser les arguments
            params = {}
            import re
            matches = re.findall(r'(\w+)="([^"]*)"', args)
            for key, value in matches:
                params[key.lower()] = value
            
            # Créer l'embed
            title = params.get('titre') or params.get('title', 'Embed')
            description = params.get('description') or params.get('desc', '')
            color_hex = params.get('couleur') or params.get('color', '#3498db')
            
            if not color_hex.startswith('#'):
                color_hex = '#' + color_hex
            
            color = discord.Color(int(color_hex[1:], 16))
            
            embed = discord.Embed(
                title=title,
                description=description,
                color=color,
                timestamp=datetime.now()
            )
            
            # Options supplémentaires
            if 'footer' in params:
                embed.set_footer(text=params['footer'])
            
            if 'image' in params:
                embed.set_image(url=params['image'])
            
            if 'thumbnail' in params:
                embed.set_thumbnail(url=params['thumbnail'])
            
            if 'author' in params:
                embed.set_author(name=params['author'])
            
            await ctx.send(embed=embed)
            
            try:
                await ctx.message.delete()
            except:
                pass
                
        except Exception as e:
            await ctx.send(
                f"❌ Erreur de syntaxe!\n\n"
                f"**Usage:**\n"
                f'`!embedsimple titre="Mon Titre" description="Ma description" couleur=#FF0000`\n\n'
                f"**Options disponibles:**\n"
                f"- `titre` ou `title`\n"
                f"- `description` ou `desc`\n"
                f"- `couleur` ou `color` (hex: #FF0000)\n"
                f"- `footer`\n"
                f"- `image` (URL)\n"
                f"- `thumbnail` (URL)\n"
                f"- `author`"
            )
    
    @commands.command(name="embedcomplet")
    @commands.has_permissions(manage_messages=True)
    async def embed_complet(self, ctx):
        """Créer un embed ultra-personnalisé avec toutes les options"""
        embed = discord.Embed(
            title="🎨 Créateur d'Embed Complet",
            description=(
                "Utilise cette commande pour créer des embeds détaillés:\n\n"
                "**Format JSON:**\n"
                "```json\n"
                "{\n"
                '  "title": "Mon Super Titre",\n'
                '  "description": "Ma description",\n'
                '  "color": 3447003,\n'
                '  "footer": {"text": "Footer text"},\n'
                '  "thumbnail": {"url": "URL"},\n'
                '  "image": {"url": "URL"},\n'
                '  "fields": [\n'
                '    {"name": "Champ 1", "value": "Valeur 1", "inline": true},\n'
                '    {"name": "Champ 2", "value": "Valeur 2", "inline": true}\n'
                "  ]\n"
                "}\n"
                "```\n\n"
                "**Envoie le JSON avec:**\n"
                "`!sendembed <json>`"
            ),
            color=discord.Color.blue()
        )
        
        await ctx.send(embed=embed)
    
    @commands.command(name="sendembed")
    @commands.has_permissions(manage_messages=True)
    async def send_embed(self, ctx, *, json_data):
        """Envoyer un embed depuis du JSON"""
        try:
            # Nettoyer le JSON
            json_data = json_data.strip()
            if json_data.startswith("```json"):
                json_data = json_data[7:]
            if json_data.startswith("```"):
                json_data = json_data[3:]
            if json_data.endswith("```"):
                json_data = json_data[:-3]
            
            data = json.loads(json_data)
            embed = discord.Embed.from_dict(data)
            
            await ctx.send(embed=embed)
            
            try:
                await ctx.message.delete()
            except:
                pass
                
        except json.JSONDecodeError:
            await ctx.send("❌ JSON invalide! Vérifie la syntaxe.")
        except Exception as e:
            await ctx.send(f"❌ Erreur: {e}")
    
    @commands.command(name="editembed")
    @commands.has_permissions(manage_messages=True)
    async def edit_embed(self, ctx, message_id: int, *, json_data):
        """Éditer un embed existant"""
        try:
            message = await ctx.channel.fetch_message(message_id)
            
            # Nettoyer le JSON
            json_data = json_data.strip()
            if json_data.startswith("```json"):
                json_data = json_data[7:]
            if json_data.startswith("```"):
                json_data = json_data[3:]
            if json_data.endswith("```"):
                json_data = json_data[:-3]
            
            data = json.loads(json_data)
            embed = discord.Embed.from_dict(data)
            
            await message.edit(embed=embed)
            await ctx.send("✅ Embed modifié!")
            
            try:
                await ctx.message.delete()
            except:
                pass
                
        except discord.NotFound:
            await ctx.send("❌ Message introuvable!")
        except json.JSONDecodeError:
            await ctx.send("❌ JSON invalide!")
        except Exception as e:
            await ctx.send(f"❌ Erreur: {e}")
    
    @commands.command(name="announcement", aliases=["annonce"])
    @commands.command(name="announcement", aliases=["annonce"])
    async def announcement(self, ctx, *, message):
        """Faire une annonce stylisée (Accessible à tous)"""
        embed = discord.Embed(
            title="📢 ANNONCE",
            description=message,
            color=discord.Color.gold(),
            timestamp=datetime.now()
        )
        embed.set_author(
            name=ctx.author.display_name,
            icon_url=ctx.author.display_avatar.url
        )
        embed.set_footer(text=f"Annonce par {ctx.author.name}")
        
        await ctx.send("@everyone", embed=embed)
        
        try:
            await ctx.message.delete()
        except:
            pass

class EmbedModalView(discord.ui.View):
    def __init__(self, modal):
        super().__init__(timeout=60)
        self.modal = modal
    
    @discord.ui.button(label="Créer l'Embed", style=discord.ButtonStyle.primary, emoji="📝")
    async def create_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(self.modal)

async def setup(bot):
    await bot.add_cog(Embeds(bot))
