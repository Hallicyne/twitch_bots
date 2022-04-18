import discord
import os

from dotenv import load_dotenv


def main():
    load_dotenv()
    discord_token = os.getenv('DISCORD_TOKEN')
    discord_guild = os.getenv('DISCORD_GUILD')

    intents = discord.Intents.default()
    intents.members = True

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():

        for guild in client.guilds:
            if guild.name == discord_guild:
                breakpoint

        print(f"{client.user} connected to discord!\n")

        sf = "streamers.txt"

        for each in guild.members:
            for role in each.roles:
                # check each user for the streamer role, if it exists, print it
                if "streamers" in role.name.lower():
                    print(f"Streamer: {each.name}")
                    # open the streamers file and check if the name exists
                    with open(sf, "r", encoding="utf-8") as f:
                        arr = f.readlines()
                        if each.name in arr:
                            # error user exists
                            print("User exists, skipping")
                        else:
                            # write name to file so we dont just keep wrting
                            # the same name repeatedly
                            with open(sf, "a", encoding="utf-8") as f:
                                f.write(f"{each.name}")
                                print(f"{each.name} written to file")
                                # write to discord channel #self-promotion
                                channel = discord.utils.get(
                                    # send the message to self promotion
                                    # channel.
                                    guild.channels, name='self-promotion')
                                chan = client.get_channel(channel.id)
                                await chan.send(f"!twitch {each.name}")
                else:
                    pass

    client.run(discord_token)


if __name__ == '__main__':
    main()
