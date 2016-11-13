from __future__ import unicode_literals
import discord
import asyncio
import urllib
import urllib.request
import urllib.parse
import re
import threading
import types
import os

from Bot import Settings

prefix = "~"
client = discord.Client()
txt=None
music=None
musico=False

valid_prefixx = ["`", ", ", "~", ", ", "!", ", ", "#", ", ", "$", ", ", "%", ", ", "^", ", ", "&", ", ", "*", ", ", "(", ", ", ")", ", ", "-", ", ", "_", ", ", "+", ", ", "="]
valid_prefix = ''.join(valid_prefixx)
valid_prefixx = ["`", "~", "!", "#", "$", "%", "^", "&", "*", "(", ")", "-", "_", "+", "="]

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def acctest(p, i):
    if p=="Banned":
        try:
            file=open(".\\Bot\\Access\\Banned\\"+i+".txt")
            file.close()
            return True
        except:
            return False
    try:
        file=open(".\\Bot\\Access\\Banned\\"+i+".txt")
        file.close()
        return False
    except:
        hi=None
    if p=="Extended":
        try:
            file=open(".\\Bot\\Access\\Extended\\"+i+".txt")
            file.close()
            return True
        except:
            hi=None
    if p=="Full" or p=="Extended":
        try:
            file=open(".\\Bot\\Access\\Full\\"+i+".txt")
            file.close()
            return True
        except:
            return False

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    if Settings.Autorun_Music==True:
        os.system("start Bot\\Kirsi\" \"Music.py")
        musico=True
    if not acctest("Full", Settings.User_ID):
        file=open(".\\Bot\\Access\\Full\\"+Settings.User_ID+".txt", "w")
        file.write(Settings.User_ID)
        file.close()

def is_int_try(str):
    try:
        int(str)
        return True
    except ValueError:
        return False

def logger(message, command):
    print(message.author.name+" used command: "+command)

@client.event
async def on_message(message):
    global prefix
    global txt
    global music
    global queue
    global musico
    if not message.channel.id == "232497426529910786" or not message.channel.id == "241717368160518144":
        #if message.content.startswith(prefix+'summon'):
            #if message.author == discord.utils.get(client.get_all_members(), id='193997394411520001'):
                #if not discord.utils.get(message.server.channels, name='music', type=discord.ChannelType.text)==None:
                    #txt=discord.utils.get(message.server.channels, name='music', type=discord.ChannelType.text)
                    #if not discord.utils.get(message.server.channels, name='kirsi', type=discord.ChannelType.voice)==None:
                        #music=discord.utils.get(message.server.channels, name='kirsi', type=discord.ChannelType.voice)
                        #await client.send_message(message.channel, "I summon thou great beast, Kirsi Music!")
                        #os.system("start Kirsi\" \"Music.py")
                    #elif discord.utils.get(message.server.channels, name='music', type=discord.ChannelType.voice)==None:
                        #music=discord.utils.get(message.server.channels, name='music', type=discord.ChannelType.voice)
                        #await client.send_message(message.channel, "I summon thou great beast, Kirsi Music!")
                        #os.system("start Kirsi\" \"Music.py")
                    #else:
                        #print("error")
                #else:
                    #print("error")
                    
        # --------------------------------------------------------------------------------------------------------- Test
        if message.content.startswith(prefix+'test') and acctest("Basic", message.author.id):
            counter = 0
            tmp = await client.send_message(message.channel, 'Calculating messages...')
            client.send_typing(message.channel)
            logger(message, "Test")
            async for log in client.logs_from(message.channel, limit=100):
                client.send_typing(message.channel)
                if log.author == message.author:
                    counter += 1
            await client.edit_message(tmp, 'You have {} messages.'.format(counter))
        # --------------------------------------------------------------------------------------------------------- Sleep
        elif message.content.startswith(prefix+'sleep') and acctest("Extended", message.author.id):
            if message.author.server_permissions.administrator:
                msg=message.content[len(prefix+'sleep')-1:]
                if msg.startswith(" "):
                    msg=msg.strip(" ")
                    isint = is_int_try(msg)
                    if isint:
                        msg=int(msg)
                        await client.send_message(message.channel, "Good night!")
                        if msg>280:
                            msg=280
                        print("Sleeping for "+str(280)+" seconds.")
                        logger(message, "Sleep")
                        await asyncio.sleep(msg)
                        await client.send_message(message.channel, 'Morning~')
                        print("Sleep finished.")
                    else:
                        await client.send_message(message.channel, "Usage: "+prefix+"sleep # -- max 280.")
                else:
                    await client.send_message(message.channel, "Usage: "+prefix+ "sleep # -- max 280.")
            else:
                await client.send_message(message.channel, message.author.mention+", insufficient permissions.")
        # --------------------------------------------------------------------------------------------------------- Purge
        elif message.content.startswith(prefix+'purge') and acctest("Extended", message.author.id):
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
        elif message.content.startswith(prefix+"prefix") and acctest("Full", message.author.id):
            if len(message.content)==9:
                if message.author == discord.utils.get(client.get_all_members(), server__name='Un-Go',name='Kirsi') or message.author == discord.utils.get(client.get_all_members(), server__name='Un-Go', name='Inga 因果'):
                    msg=message.content.strip(prefix+"prefix")
                    if msg.startswith(" "):
                        msg=msg.strip(" ")
                        if valid_prefixx.index(msg):
                            prefix=msg
                            await client.send_message(message.channel, message.author.mention+" changed prefix to '"+prefix+"'.")
                        else:
                            await client.send_message(message.channel, message.author.mention+", invalid prefix.")
                    else:
                        await client.send_message(message.channel, message.author.mention+", invalid syntax.")
                else:
                    await client.send_message(message.channel, message.author.mention+", insufficient permissions.")
            else:
                await client.send_message(message.channel, message.author.mention+", invalid syntax.")
        elif message.content.startswith(prefix+"restartkirsi") and acctest("Full", message.author.id):
            await client.send_message(message.channel, "Restarting bot.")
            sys.exit()
        elif message.content.lower().startswith(prefix+"access ") and acctest("Full", message.author.id):
            cooldown=1
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
            else:
                await client.send_message(message.channel, "Usage: \n ```"+prefix+"Access Full/Extended/Banned Grant/Remove Name```")
            if user.lower().startswith("grant "):
                user=user[len("grant "):]
                user=discord.utils.get(client.get_all_members(), server__id=message.server.id, name=user)
                name=user
                if not user==None:
                    user=user.id
                    if not acctest(To, user):
                        file=open(".\\Bot\\Access\\"+To+"\\"+user+".txt", "w")
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
                            os.remove(".\\Bot\\Access\\"+To+"\\"+user+".txt")
                            await client.send_message(message.channel, message.author.mention+", Removed "+str(name)+" from "+To+" list.")
                        except:
                            await client.send_message(message.channel, "Failed to remove..")
                    else:
                        await client.send_message(message.channel, "Failed, user not in list.")
                else:
                    await client.send_message(message.channel, message.author.mention+", User not found.")
        elif message.content.lower().startswith(prefix+"music") and acctest("Full", message.author.id) and not music:
            os.system("start Bot\\Kirsi\" \"Music.py")
            musico=True

client.run(Settings.Token)
