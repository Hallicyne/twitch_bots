import discord

def main():
    discordConnect()

def discordConnect():
    @bot.command(pass_context=True)
    @commands.has_role("Streamers")
    async def addtwitch(ctx, user: discord.Member):
        if role in user.roles:
            await bot.says(f"!twitch {user}")