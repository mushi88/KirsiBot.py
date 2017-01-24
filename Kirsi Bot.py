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
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


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
            time.sleep(.2)
            cooldown=False
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

@client.event
async def on_member_join(member):
    if Settings.WelcomeMessage:
        welcomechat=discord.utils.get(client.get_all_channels(), server__id=Settings.Server, id=Settings.Welcome_Channel)
        await client.send_message(welcomechat, "Welcome to "+str(member.server.name)+" "+member.mention+"! Make sure to go to #terms_conditions-server-ranks to check out the terms and conditions!", tts=True)

def logger(message, command):
    print(message.author.name+" used command: "+command)

async def sm(channel, msg):
    return await client.send_message(channel, msg)

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
    while 1:
        tempmessage=await client.send_message(message.channel, "Access Options (Send **Cancel** at any time to cancel.):\n```What is the name of the user you would like to change the permissions of?```")
        Options=await client.wait_for_message(timeout=10, author=message.author, channel=message.channel)
        if not Options==None:
            if Options.content.lower()=="cancel":
                await client.delete_message(tempmessage)
                break
            else:
                user=discord.utils.get(client.get_all_members(), server__id=message.server.id, name=user)
                name=user
                if not user==None:
                    To=None
                    nTo=None
                    user=user.id
                    if acctest("Full", user):
                        To="Full"
                    elif acctest("Extended", user):
                        To="Extended"
                    elif acctest("Banned", user):
                        To="no"
                    elif acctest("Owner", user):
                        To="Owner"
                    else:
                        To="Normal"
                    await client.delete_message(tempmessage)
                    while 1:
                        tempmessage=await client.send_message(message.channel, Options.content+" currently has "+To+" permissions.\n**What permission level do you want to give them?\n```1) Owner\n2) Full\n3) Extended\n4) Normal\n5) None```")
                        Options=await client.wait_for_message(timeout=10, author=message.author, channel=message.channel)
                        if not Options==None:
                            if Options.content.lower()=="cancel":
                                await client.delete_message(tempmessage)
                                break
                            else:
                                if To=="no":
                                    To="Banned"
                                os.remove(".\\theBot\\Access\\"+To+"\\"+user+".txt")
                                Options=Options.content
                                if Options=="1":
                                    nTo="Owner"
                                elif Options=="2":
                                    nTo="Full"
                                elif Options=="3":
                                    nTo="Extended"
                                elif Options=="4":
                                    nTo=None
                                elif Options=="5":
                                    nTo="Banned"
                                else:
                                    await client.delete_message(tempmessage)
                                    continue
                                if not nTo==None:
                                    file=open(".\\theBot\\Access\\"+nTo+"\\"+user+".txt", "w")
                                    file.write(user)
                                    file.close()
                                else:
                                    nTo=="Normal"
                                await client.send_message(message.channel, message.author.mention+", Gave "+str(name)+" "+nTo+" permissions.")
                        else:
                            await client.delete_message(tempmessage)
                            tempmessage=await client.send_message(message.channel, "No reply recieved.")
                            time.sleep(2)
                            await client.delete_message(tempmessage)
                            break
                else:
                    await client.delete_message(tempmessage)
                    tempmessage=await client.send_message(message.channel, "Could not find user specified.")
                    time.sleep(2)
                    await client.delete_message(tempmessage)
                    continue
        else:
            await client.delete_message(tempmessage)
            tempmessage=await client.send_message(message.channel, "No reply recieved, Access Options closed.")
            time.sleep(2)
            await client.delete_message(tempmessage)
            break



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
            if CmdLevels[x]=="Banned" or CmdLevels[x]=="Extended" or CmdLevels[x]=="Full":
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
