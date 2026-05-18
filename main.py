import os

import discord
from discord.ext import commands

# Récupération des variables d'environnement injectées par Docker
TOKEN = os.getenv("DISCORD_TOKEN")
TARGET_USER_ENV = os.getenv("TARGET_USER_ID")

if not TOKEN or not TARGET_USER_ENV:
    print(
        "Erreur critique : Les variables DISCORD_TOKEN ou TARGET_USER_ID ne sont pas configurées."
    )
    exit(1)

TARGET_USER_ID = int(TARGET_USER_ENV)


class BatonBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.voice_states = True
        intents.members = True

        super().__init__(command_prefix="!", intents=intents)
        self.has_baton = False

    async def setup_hook(self):
        await self.tree.sync()


bot = BatonBot()


@bot.event
async def on_ready():
    print(f"Bot connecté avec succès en tant que {bot.user}")


@bot.tree.command(
    name="baton", description="Alterne le bâton de la parole pour l'utilisateur cible."
)
async def baton(interaction: discord.Interaction):
    if interaction.user.id == TARGET_USER_ID:
        await interaction.response.send_message(
            "Vous n'avez pas le droit de vous donner le bâton vous-même !",
            ephemeral=True,
        )
        return

    bot.has_baton = not bot.has_baton
    member = interaction.guild.get_member(TARGET_USER_ID)

    if not member:
        await interaction.response.send_message(
            "L'utilisateur cible est introuvable sur ce serveur.", ephemeral=True
        )
        return

    etat = "donné" if bot.has_baton else "repris"
    action = (
        "Il peut maintenant parler."
        if bot.has_baton
        else "Il est de nouveau rendu muet."
    )

    await interaction.response.send_message(
        f"Le bâton de la parole a été {etat}. {action}"
    )

    if member.voice and member.voice.channel:
        try:
            await member.edit(mute=not bot.has_baton)
        except discord.HTTPException:
            pass


@bot.event
async def on_voice_state_update(member, before, after):
    if member.id == TARGET_USER_ID:
        if after.channel is not None:
            if not bot.has_baton and not after.mute:
                try:
                    await member.edit(mute=True)
                except discord.HTTPException:
                    pass
            elif bot.has_baton and after.mute:
                try:
                    await member.edit(mute=False)
                except discord.HTTPException:
                    pass


bot.run(TOKEN)
