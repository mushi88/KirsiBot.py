from __future__ import unicode_literals
from theBot import Settings
import discord
import asyncio
import urllib
import urllib.request
import urllib.parse
import re
import threading
import types
import os
import time
import sys
import random
import subprocess

sys.setrecursionlimit(sys.maxsize) # TODO: Fix crashing. [Cause may be thread]

prefix=Settings.Prefix
client = discord.Client()
musico=False

loop=1

valid_prefixx = ["`", ", ", "~", ", ", "!", ", ", "#", ", ", "$", ", ", "%", ", ", "^", ", ", "&", ", ", "*", ", ", "(", ", ", ")", ", ", "-", ", ", "_", ", ", "+", ", ", "="]
valid_prefix = ''.join(valid_prefixx)
valid_prefixx = ["`", "~", "!", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "="]

MusicCmds=[prefix+"Search - Search for a song ["+prefix+"search <SongName>]", prefix+"Volume - Set volume ["+prefix+"volume <#>]", prefix+"Pause - Pause song ["+prefix+"pause]", prefix+"Resume - Resumes song after pauseing ["+prefix+"resume]", prefix+"Skip - Skips song if there is another song in queue ["+prefix+"skip]", prefix+"Clear - Clears queue ["+prefix+"clear]", prefix+"Playlist - Changes queue to playist ["+prefix+"playlist <PlaylistName>]", prefix+"Stop - Stops current song, no resuming ["+prefix+"stop]", prefix+"Shutdown - Shuts down the bot ["+prefix+"shutdown]", prefix+"Repeat - toggles repeat on,  only works for one song ["+prefix+"repeat]", prefix+"Url - Shows URL of song playing ["+prefix+"url]", prefix+"Playlists - Shows available playlists ["+prefix+"playlists]"]
Cmds=[prefix+"Test - Tests to see how many messages you have sent ["+prefix+"test]", prefix+"Sleep - Makes the bot sleep ["+prefix+"sleep <#>]", prefix+"Purge - Mass deletes messages ["+prefix+"purge <#>]", prefix+"Shutdown - Shuts down the bot ["+prefix+"shutdown]", prefix+"Access - Changes peoples access rank ["+prefix+"access]", prefix+"Music - Launched music client ["+prefix+"music]", prefix+"Ping! - Pong! ["+prefix+"ping]", prefix+"Cmds - Shows available commands ["+prefix+"cmds]"]
MusicLevels=["Banned", "Extended", "Extended", "Extended", "Extended", "Extended", "Extended", "Extended", "Owner", "Extended", "Banned", "Banned"]
CmdLevels=["Banned", "Extended", "Extended", "Owner", "Owner", "Full", "Banned", "Banned"]

cooldown=False

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def acctest(p, i):
    if p=="Banned":
        try:
            file=open(".\\theBot\\Access\\Banned\\"+i+".txt")
            file.close()
            return True
        except:
            return False
    try:
        file=open(".\\theBot\\Access\\Banned\\"+i+".txt")
        file.close()
        return False
    except:
        pass
    if p=="Extended":
        try:
            file=open(".\\theBot\\Access\\Extended\\"+i+".txt")
            file.close()
            return True
        except:
            pass
    if p=="Full" or p=="Extended":
        try:
            file=open(".\\theBot\\Access\\Full\\"+i+".txt")
            file.close()
            return True
        except:
            pass
    if p=="Owner" or p=="Full" or p=="Extended":
        try:
            file=open(".\\theBot\\Access\\Owner\\"+i+".txt")
            file.close()
            return True
        except:
            return False

def check():
    ##global loop
    global cooldown
    while True:
        if cooldown:
            time.sleep(1)
            cooldown=False
        time.sleep(1)
    #if loop==sys.maxsize - 1:
    #    sys.exit()
    #else:
    #    loop += 1
    #check()

def Execute(f):
    if sys.platform=="win32":
        f=f.replace(' ', '" "')
        os.system("start "+f)
    elif sys.platform=="linux":
        os.system("xdg-open "+f)
    else:
        os.system("open "+f)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    if Settings.Autorun_Music==True:
        Execute("theBot\\Kirsi Music.py")
        musico=True
    if not acctest("Owner", Settings.User_ID):
        file=open(".\\theBot\\Access\\Owner\\"+Settings.User_ID+".txt", "w")
        file.write(Settings.User_ID)
        file.close()
    thread=threading.Thread(target=check)
    thread.start()

def is_int_try(str):
    try:
        int(str)
        return True
    except ValueError:
        return False

def logger(message, command):
    print(message.author.name+" used command: "+command)

## Cmd Funcs

async def cmd_test(message):
    counter = 0
    tmp = await client.send_message(message.channel, 'Calculating messages...')
    client.send_typing(message.channel)
    logger(message, "Test")
    async for log in client.logs_from(message.channel, limit=100):
        client.send_typing(message.channel)
        if log.author == message.author:
            counter += 1
    await client.edit_message(tmp, 'You have {} messages.'.format(counter))


async def cmd_sleep(message):
    msg=message.content[len(prefix+'sleep'):]
    if msg.startswith(" "):
        msg=msg.strip(" ")
        isint = is_int_try(msg)
        if isint:
            msg=int(msg)
            await client.send_message(message.channel, "Good night!")
            if msg>280:
                msg=280
            print("Sleeping for "+str(msg)+" seconds.")
            logger(message, "Sleep")
            await asyncio.sleep(msg)
            await client.send_message(message.channel, 'Morning~')
            print("Sleep finished.")
        else:
            await client.send_message(message.channel, "Usage: "+prefix+"sleep # -- max 280.")
    else:
        await client.send_message(message.channel, "Usage: "+prefix+ "sleep # -- max 280.")


async def cmd_purge(message):
    count = message.content.strip(prefix+'purge')
    if count.startswith(' '):
        count = count.strip(" ")
        isint = is_int_try(count)
        if isint:
            count = int(count)+1
            if count > 101:
                count = 101
            await client.purge_from(message.channel, limit=count)
            logger(message, "Purge")
        else:
            await client.send_message(message.channel, "```'" +prefix+ "purge #' -- Max 100```")
    else:
        await client.send_message(message.channel, "```'"+prefix+"purge #' -- Max 100```")


async def cmd_shutdown(message):
    await client.send_message(message.channel, "Bot is shutting down...")
    client.close()
    exit()


async def cmd_access(message):
    user=message.content[len(prefix+"access "):]
    To=None
    if user.lower().startswith("full "):
        To="Full"
        user=user[len("full "):]
    elif user.lower().startswith("extended "):
        To="Extended"
        user=user[len("extended "):]
    elif user.lower().startswith("banned "):
        To="Banned"
        user=user[len("banned "):]
    elif user.lower().startswith("owner "):
        To="Owner"
        user=user[len("owner "):]
    else:
        await client.send_message(message.channel, "Usage: \n ```"+prefix+"Access Owner/Full/Extended/Banned Grant/Remove Name```")
    if user.lower().startswith("grant "):
        user=user[len("grant "):]
        user=discord.utils.get(client.get_all_members(), server__id=message.server.id, name=user)
        name=user
        if not user==None:
            user=user.id
            if not acctest(To, user):
                file=open(".\\theBot\\Access\\"+To+"\\"+user+".txt", "w")
                file.write(user)
                file.close()
                await client.send_message(message.channel, message.author.mention+", Added "+str(name)+" to "+To+" list.")
            else:
                await client.send_message(message.channel, message.author.mention+", User already in list.")
        else:
            await client.send_message(message.channel, "Could not find user specified.")
    elif user.lower().startswith("remove "):
        user=user[len("remove "):]
        user=discord.utils.get(client.get_all_members(), server__id=message.server.id, name=user)
        name=user
        if not user==None:
            user=user.id
            if acctest(To, user):
                try:
                    os.remove(".\\theBot\\Access\\"+To+"\\"+user+".txt")
                    await client.send_message(message.channel, message.author.mention+", Removed "+str(name)+" from "+To+" list.")
                except:
                    await client.send_message(message.channel, "Failed to remove..")
            else:
                await client.send_message(message.channel, "Failed, user not in list.")
        else:
            await client.send_message(message.channel, message.author.mention+", User not found.")


async def cmd_music(message):
    global musico
    if not musico:
        Execute("theBot\\Kirsi Music.py")
        musico=True
        await client.send_message(message.channel, "Music client started.")
    else:
        await client.send_message(message.channel, "Music client already started.")


async def cmd_cmds(message):
    AvaiCmds=[]
    AvaiMusic=[]
    if acctest("Banned", message.author.id):
        AvaiCmds.append("You have no available commands.")
        AvaiMusic.append("You have no available commands.")
    elif acctest("Owner", message.author.id):
        for x in range(0, len(Cmds)):
            if CmdLevels[x]=="Banned" or CmdLevels[x]=="Extended" or CmdLevels[x]=="Full" or CmdLevels[x]=="Owner":
                AvaiCmds.append(Cmds[x])
        for x in range(0, len(MusicCmds)):
            if MusicLevels[x]=="Banned" or MusicLevels[x]=="Extended" or MusicLevels[x]=="Full" or MusicLevels[x]=="Owner":
                AvaiMusic.append(MusicCmds[x])
    elif acctest("Full", message.author.id):
        for x in range(0, len(Cmds)):
            if CmdLevels[x]=="Banned" or CmdsLevel[x]=="Extended" or CmdsLevel[x]=="Full":
                AvaiCmds.append(Cmds[x])
        for x in range(0, len(MusicCmds)):
            if MusicLevels[x]=="Banned" or MusicLevels[x]=="Extended" or MusicLevels[x]=="Full":
                AvaiMusic.append(MusicCmds[x])
    elif acctest("Extended", message.author.id):
        for x in range(0, len(Cmds)):
            if CmdLevels[x]=="Banned" or CmdLevels[x]=="Extended":
                AvaiCmds.append(Cmds[x])
        for x in range(0, len(MusicCmds)):
            if MusicLevels[x]=="Banned" or MusicLevels[x]=="Extended":
                AvaiMusic.append(MusicCmds[x])
    elif not acctest("Banned", message.author.id):
        for x in range(0, len(Cmds)):
            if CmdLevels[x]=="Banned":
                AvaiCmds.append(Cmds[x])
        for x in range(0, len(MusicCmds)):
            if MusicLevels[x]=="Banned":
                AvaiMusic.append(MusicCmds[x])

    await client.send_message(message.channel, "Commands:\n```"+'\n\n'.join(AvaiCmds)+"```")
    await client.send_message(message.channel, "Music:\n```"+'\n\n'.join(AvaiMusic)+"```")

async def cmd_pingpong(message):
    await client.send_message(message.channel, "Pong!")



## Func Exec

@client.event
async def on_message(message):
    global cooldown

    if message.content.lower().startswith(prefix+'test'):
        if not cooldown:
            cooldown=True
            if not acctest("Banned", message.author.id):
                await cmd_test(message)
            else:
                await client.send_message(message.channel, message.author.mention+", insufficient permissions.")
            cooldown=False


    elif message.content.lower().startswith(prefix+'sleep'):
        if not cooldown:
            cooldown=True
            if acctest("Extended", message.author.id):
                await cmd_sleep(message)
            else:
                await client.send_message(message.channel, message.author.mention+", insufficient permissions.")


    elif message.content.lower().startswith(prefix+'purge'):
        if not cooldown:
            cooldown=True
            if acctest("Extended", message.author.id):
                await cmd_purge(message)
            else:
                await client.send_message(message.channel, message.author.mention+", insufficient permissions.")


    elif message.content.lower().startswith(prefix+"shutdown"):
        if not cooldown:
            cooldown=True
            if acctest("Owner", message.author.id):
                await cmd_shutdown(message)
            else:
                await client.send_message(message.channel, message.author.mention+", insufficient permissions.")


    elif message.content.lower().startswith(prefix+"access "):
        if not cooldown:
            cooldown=True
            if acctest("Owner", message.author.id):
                await cmd_access(message)
            else:
                await client.send_message(message.channel, message.author.mention+", insufficient permissions.")


    elif message.content.lower().startswith(prefix+"music"):
        if not cooldown:
            cooldown=True
            if acctest("Full", message.author.id):
                await cmd_music(message)
            else:
                await client.send_message(message.channel, message.author.mention+", insufficient permissions.")


    elif message.content.lower().startswith(prefix+"cmds"):
        if not cooldown:
            cooldown=True
            if not acctest("Banned", message.author.id):
                await cmd_cmds(message)
            else:
                await client.send_message(message.channel, message.author.mention+", insufficient permissions.")


    elif message.content.lower().startswith(prefix+"ping"):
        if not cooldown:
            cooldown=True
            if not acctest("Banned", message.author.id):
                await cmd_pingpong(message)
            else:
                await client.send_message(message.channel, message.author.mention+", insufficient permissions.")

client.run(Settings.Token)
