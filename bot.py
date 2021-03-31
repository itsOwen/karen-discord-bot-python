import discord
import random
import asyncio
import os
from discord.ext import tasks
from discord.utils import get
from discord.ext import commands
from discord.ext.commands import Bot

client = discord.Client()

# random messages list
r = open('random.txt', 'r')
responses = r.readlines()

# Heykaren responses
p = open('hey.txt', 'r')
hikaren = p.readlines()

# jokes list
j = open('jokes.txt', 'r')
jokes = j.readlines()

# karen abuse reply list
a = open('karenabuse_resp.txt', 'r')
kabuse = a.readlines()

# karen love reply list
c = open('klover.txt', 'r')
klover = c.readlines()

# karen mention reply list
d = open('kmention.txt', 'r')
kmention = d.readlines()

# karen facts reply list
h = open('facts.txt', 'r')
facts = h.readlines()


#CHANNEL_ID = 762686015881084978
def file_load(filename):
    new_str = []
    with open(f"{filename}.txt", "r", encoding="utf8") as file:
        for line in file:
            new_str.append(line.strip())
    return new_str


karen = file_load("kabuse_list")

helps = ["need", "help me", "pls", "please", "someone", "admin"]

karenhi = file_load("heyinput")

jlist = ["joke"]

flist = ["fact"]

klove = ["love"]

whomade = ["develop", "created", "made", "creator"]

banwords = file_load("badwords")

# File related functions


def file_word_add(filename, word):
    f = open(f"{filename}.txt", "a", encoding='utf-8')
    f.write("\n"+word)
    f.close()


def file_word_remove(filename, word):
    file_str = ''
    f = open(f"{filename}.txt", "r", encoding='utf-8')

    for line in f:
        file_str = file_str + line
    removed_str = file_str.replace(f"\n{word}", '')
    with open(f'{filename}.txt', 'w', encoding='utf8') as file:
        file.write(removed_str)

    if(len(file_str) == len(removed_str)):
        print("Word not found/removed")
    else:
        print("sucessfully removed")
    f.close()
# ends

# karen word trigger function


def karen_word_trigger(bot_msg_arr, usr_message):
    for word in bot_msg_arr:
        if(word in usr_message and "karen" in usr_message):
            return True


@tasks.loop(minutes=20)
async def rm():
    #channel = client.get_channel(CHANNEL_ID)
    guild = client.guilds[0]
    channel = discord.utils.get(guild.text_channels, name="『💬』general-chat")
    resp = random.choice(responses)
    async for message in channel.history(limit=1):
        if message.author.id == "author id here remove quotes":
            return
        else:
            await channel.send(resp)


@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="Talking with the Manager!"))
    rm.start()


@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.author.bot == True:
        return

    if message.content.startswith(">"):
        return

# commands to add and remove banwords
    if message.content.startswith("!badd"):
        if message.author.guild_permissions.administrator == False:
            await message.channel.send("Only Head admins and Server owner can use this command")
        else:
            ban_write = message.content[slice(6, len(message.content))]
            file_word_add("badwords", ban_write)
            await message.channel.send("Ban Word Added")
        return

    if message.content.startswith("!bremove"):
        if message.author.guild_permissions.administrator == False:
            await message.channel.send("Only Head admins and Server owner can use this command")
        else:
            ban_rem = message.content[slice(9, len(message.content))]
            print(ban_rem)
            file_word_remove("badwords", ban_rem)
            await message.channel.send("Ban Word removed")
        return
# end

    def bad_word_trigger(bot_msg_arr, usr_message):
        for word in bot_msg_arr:
            if(word in usr_message):
                return True

    if(bad_word_trigger(banwords, message.content.lower())) and (message.author.guild_permissions.administrator == False):
        await message.delete()
        await message.channel.send(str(message.author.mention) + " You are using a forbidden word in the chat, read <#channel id here bruh> before proceeding or I have to talk to your mum!")
        imgList = os.listdir("./images")
        imgString = random.choice(imgList)
        path = "./images/" + imgString
        await message.channel.send(file=discord.File(path))
# end

# karen trigger messages start\
    if(karen_word_trigger(karenhi, message.content.lower())):
        randkaren = random.choice(hikaren)
        await message.channel.send((message.author.mention) + (randkaren))

    if message.content.startswith("!hiadd"):
        if message.author.guild_permissions.administrator == False:
            await message.channel.send("Only Head admins and Server owner can use this command")
        else:
            hi_add = message.content[slice(7, len(message.content))]
            karenhi.append(hi_add)
            file_word_add("heyinput", hi_add)
            await message.channel.send("Word added to Garettings library :)")

    if message.content.startswith("!hiremove"):
        if message.author.guild_permissions.administrator == False:
            await message.channel.send("Only Head admins and Server owner can use this command")
        else:
            hi_rem = message.content[slice(10, len(message.content))]
            file_word_remove("heyinput", hi_rem)
            await message.channel.send("Greetings Word removed")
        return

    if(karen_word_trigger(jlist, message.content.lower())):
        jo = random.choice(jokes)
        await message.channel.send(jo)

    if(karen_word_trigger(flist, message.content.lower())):
        fl = random.choice(facts)
        await message.channel.send(fl)

    if(karen_word_trigger(karen, message.content.lower())):
        kab = random.choice(kabuse)
        await message.channel.send(str(message.author.mention) + (kab))

    if message.content.startswith("!abuseadd"):
        if message.author.guild_permissions.administrator == False:
            await message.channel.send("Only Head admins and Server owner can use this command")
        else:
            abuse_add = message.content[slice(10, len(message.content))]
            karen.append(abuse_add)
            file_word_add("kabuse_list", abuse_add)
            await message.channel.send("Word added to abusive library :)")

    if message.content.startswith("!abuseremove"):
        if message.author.guild_permissions.administrator == False:
            await message.channel.send("Only Head admins and Server owner can use this command")
        else:
            ab_rem = message.content[slice(13, len(message.content))]
            file_word_remove("kabuse_list", ab_rem)
            await message.channel.send("Abusive Word removed")
        return

    for word in helps:
        if(word in message.content and "help" in message.content.lower()):
            await message.channel.send("Please don't just type *help* in chat, elaborate your problem here and then wait for help :)")

    if(karen_word_trigger(klove, message.content.lower())):
        loveresp = random.choice(klover)
        await message.channel.send(str(message.author.mention) + (loveresp))

    if client.user.mentioned_in(message):
        kmen = random.choice(kmention)
        await message.channel.send(str(message.author.mention) + (kmen))

    if(karen_word_trigger(whomade, message.content.lower())):
        await message.channel.send(str(message.author.mention) + " I was created by Owen Singh to help people, Now I am clearingg his mess!")
# karen trigger messages end

    # Make ur commands
    if message.content.startswith("++injectbll"):
        await message.channel.send("Here this is similar process with all games, but you may use different injektors for different games: https://youtu.be/7eFkToypW6c")

    if message.content.startswith("++extract"):
        await message.channel.send("Here you go user: https://youtu.be/dr0g_Ux7_8M")

    if message.content.startswith("++defender"):
        await message.channel.send("Same process for your other antivirus as well (if you have any): https://youtu.be/apuccBWaNkQ")
    # mods info end

# @client.event
# async def on_guild_join(guild):
    # await guild.create_text_channel("『💬』general-chat")

print("Bot is has started running")
client.run('Your Token Here')
