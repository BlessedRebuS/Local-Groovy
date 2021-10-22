import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import os
import asyncio
from youtubesearchpython import VideosSearch

# bot params to be changed
BOT_ID = 0000
TOKEN = "YOUR_TOKEN"

# set bot intents
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="", description="Description", intents=intents)

# bot.OBJ to define global bot variables
bot.set = False
bot.list = list()


@bot.command()
async def music(ctx):
    if (
        "music help" not in ctx.message.content.lower()
        and "help music" not in ctx.message.content.lower()
    ):
        bot.list.clear()
        if not os.path.exists("audio.mp3"):
            os.remove("audio.mp3")
        x = ctx.message.content.split(" ")
        url = x[1]
        if "http" not in url:
            url_updated = ""
            await asyncio.sleep(1)
            for strings in x:
                url_updated += strings + " "
            print("URL: " + url_updated)
            bot.set = True
            videosSearch = VideosSearch(url_updated, limit=5)  # JSON
            #  print(videosSearch.result())
            i = 0
            for key in videosSearch.result()["result"]:
                i = i + 1
                title = key["title"]
                url_updated = key["link"]
                duration = key["duration"]
                result = (
                    "**"
                    + str(i)
                    + "** : "
                    + str(title)
                    + " **("
                    + str(duration)
                    + ")**"
                )
                await ctx.message.channel.send(result)
                bot.list.append(url_updated)
            print(bot.list)
        else:
            msg = ctx.message
            await player(msg, url)


async def player(msg, url):
    await msg.channel.send("Downloading... " + url)
    cmd = "youtube-dl --extract-audio --audio-format mp3 -o 'audio.%(ext)s' "
    song = cmd + " " + url
    os.system(song)
    while not os.path.exists("audio.mp3"):
        await asyncio.sleep(1)
    vc = await msg.author.voice.channel.connect()
    vc.play(discord.FFmpegPCMAudio("audio.mp3"))
    print("URL : " + url)
    while vc.is_playing():
        await asyncio.sleep(1)
    await vc.disconnect()


@bot.listen()
async def on_message(message):
    # bot.set changes dinamically because on_message(message) and music(ctx) are different functions
    if bot.set is True and message.author.id != BOT_ID:
        choice = message.content
        try:
            value = int(choice)
            if value in range(1, 6):
                bot.set = False
                await player(message, bot.list[value - 1])
            else:
                await message.channel.send("Pick a number between 1 and 5")
        except ValueError:
            # checking no string as value
            await message.channel.send("Pick a number between 1 and 5")


@bot.command()
async def stop(ctx):
    try:
        server = ctx.message.guild.voice_client
        bot.list.clear()
        bot.set = False
        await server.disconnect()
    except:
        print("Already disconnected")


@bot.event
async def on_ready():
    print("Ready")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error


bot.run(TOKEN)
