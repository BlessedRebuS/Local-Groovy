import discord
from discord.ext import commands
from discord.ext.commands import CommandNotFound
import asyncio
from youtubesearchpython import VideosSearch
import youtube_dl

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

# audio format use bestaudio for better quality (slower performances)
ydl_opts = {"format": "worstaudio"}

# set bot intents
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="", description="Description", intents=intents)

# bot.OBJ to define global bot variables
bot.set = False
bot.list = list()
bot.queue = list()
bot.playing = False


@bot.command()
async def music(ctx):
    if (
        "music help" not in ctx.message.content.lower()
        and "help music" not in ctx.message.content.lower()
    ):
        bot.list.clear()
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
            bot.queue.append(url)
            await player(msg)


async def player(msg):
    bot.playing = True
    vc = await msg.author.voice.channel.connect()
    for url in bot.queue:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            URL = info["formats"][0]["url"]
        vc.play(discord.FFmpegPCMAudio(URL))
        while vc.is_playing():
            await asyncio.sleep(1)
    bot.playing = False
    bot.queue.clear()
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
                bot.queue.append(bot.list[value - 1])
                if(bot.playing is False):
                 await player(message)
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
        bot.queue.clear()
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
