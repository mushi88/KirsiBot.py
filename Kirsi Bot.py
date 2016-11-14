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
    msg=message.content[len(prefix+'sleep')-1:]
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


async def cmd_prefix(message):
    global prefix
    if len(message.content)==9:
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
        await client.send_message(message.channel, message.author.mention+", invalid syntax.")


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


async def cmd_music(message):
    global musico
    if not musico:
        exec(open(".\\Bot\\Kirsi Music.py").read())
        musico=True
    else:
        await client.send_message(message.channel, "Music already started.")
            
## Func Exec

@client.event
async def on_message(message):
    if 1 == 1:

        
        if message.content.lower().startswith(prefix+'test'):
            if not acctest("Banned", message.author.id):
                await cmd_test(message)
            else:
                await client.send_message(message.channel, message.author.mention+", insufficient permissions.")
                
                
        elif message.content.lower().startswith(prefix+'sleep'):
            if acctest("Extended", message.author.id):
                await cmd_sleep(message)
            else:
                await client.send_message(message.channel, message.author.mention+", insufficient permissions.")

                
        elif message.content.lower().startswith(prefix+'purge'):
            if acctest("Extended", message.author.id):
                await cmd_purge(message)
            else:
                await client.send_message(message.channel, message.author.mention+", insufficient permissions.")

                
        elif message.content.lower().startswith(prefix+"prefix"):
            if acctest("Full", message.author.id):
                await cmd_prefix(message)
            else:
                await client.send_message(message.channel, message.author.mention+", insufficient permissions.")

                
        elif message.content.lower().startswith(prefix+"shutdown"):
            if acctest("Full", message.author.id):
                await cmd_shutdown(message)
            else:
                await client.send_message(message.channel, message.author.mention+", insufficient permissions.")
                
            
        elif message.content.lower().startswith(prefix+"access "):
            if acctest("Full", message.author.id):
                await cmd_access(message)
            else:
                await client.send_message(message.channel, message.author.mention+", insufficient permissions.")
                
            
        elif message.content.lower().startswith(prefix+"music"):
            if acctest("Full", message.author.id):
                await cmd_prefix(message)
            else:
                await client.send_message(message.channel, message.author.mention+", insufficient permissions.")

client.run(Settings.Token)
