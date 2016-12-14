import discord

import asyncio

import urllib

import urllib.request

import urllib.parse

import re

import time

import simplejson

import random

import os

import sys



import Settings

from Settings import Prefix as prefix



client = discord.Client()



resutls = None

voice = None

player = None

lastVideo = None

repeat = False



cooldown=0



playlistqueue=[]



ytsnip="http://www.youtube.com/watch?v="

vol=.15

queue = []



ungo = None

ch = None

vchannel = None

user=None

req=None

last=None


serverid = Settings.Server


# -------------------- Permissions

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

# -------------------- Funcs (Messy)

@client.event

async def on_ready():

    global user

    global voice

    global player

    global vchannel

    global permlist

    print("Logged in as:")

    print(client.user.name)

    print("-------")

    await client.change_presence(game=discord.Game(name="{}cmds for commands".format(prefix)))

    user=discord.utils.get(client.get_all_members(), id=client.user.id)

    voice = await client.join_voice_channel(discord.utils.get(client.get_all_channels(), id=Settings.Voice_Channel))

    sys.stdout = open(os.devnull, "w")

    player = await voice.create_ytdl_player("https://www.youtube.com/watch?v=Vbks4abvLEw")

    sys.stdout = sys.__stdout__

    vchannel = discord.utils.get(client.get_all_channels(), server__id=serverid, id=Settings.Chat_Channel)

    player.start()

    checkerrun = schedule_coroutine(check())

    checkerrun



def inChannel(message):
    if message.channel.id==Settings.Chat_Channel:
        return True
    else:
        return False



def list_files(path):

    files = []

    for name in os.listdir(path):

        if os.path.isfile(os.path.join(path, name)):

            if ".txt" in name:

                name=name.split(".", 1)

            files.append(name[0].capitalize())

    return files



@client.event

async def download(video):

    global player

    global repeat

    global vol

    global last

    if repeat:

        try:

            sys.stdout = open(os.devnull, "w")

            player = await voice.create_ytdl_player("http://www.youtube.com/watch?v="+lastVideo)

            sys.stdout = sys.__stdout__

            player.volume = vol

            await client.change_presence(game=discord.Game(name=player.title))

            player.start()

            dur=str(time.strftime("%H:%M:%S", time.gmtime(player.duration)))

            if last=="NowPlaying":

                print("\nNow playing: "+player.title+" (%s)" % dur)

            else:

                last=="NowPlaying"

                print("\n\nNow playing: "+player.title+" (%s)" % dur)

            await client.send_message(vchannel, "Now playing: "+player.title+" (%s)" % dur)

        except:

            await client.send_message(vchannel, "Error playing: %s. Repeat is now off." % player.title)

            repeat=False

    else:

        try:

            sys.stdout = open(os.devnull, "w")

            player = await voice.create_ytdl_player("http://www.youtube.com/watch?v="+video)

            sys.stdout = sys.__stdout__

            player.volume = vol

            await client.change_presence(game=discord.Game(name=player.title))

            player.start()

            dur=str(time.strftime("%H:%M:%S", time.gmtime(player.duration)))

            if last=="NowPlaying":

                print("\nNow playing: "+player.title+" (%s)" % dur)

            else:

                last=="NowPlaying"

                print("\n\nNow playing: "+player.title+" (%s)" % dur)

            await client.send_message(vchannel, "Now playing: "+player.title+" (%s)" % dur)

        except:

            print("Now playing: "+player.title+" (%s)" % dur)

            await client.send_message(vchannel, "Error playing: %s. Skipping..." % player.title)



def search(search):

    global results

    global lastVideo

    parse = urllib.parse.urlencode({"search_query": search})

    request = urllib.request.urlopen("http://www.youtube.com/results?"+parse)

    results = re.findall(r'href=\"\/watch\?v=(.{11})', request.read().decode())



def get_playlist(path):

    global playlistqueue

    global queue

    playlistqueue.clear()

    file=open(path)

    num_lines = sum(1 for line in open(path))

    for x in range(0, num_lines*50):

        temp=random.choice(open(path).readlines())

        if not temp in playlistqueue:

            playlistqueue.append(temp)

        queue=playlistqueue

        file.close()



@client.event

async def check():

    global queue

    global cooldown

    if repeat:

        if not len(queue)==0:

            if not queue[0]==lastVideo:

                queue.clear()

                queue.append(lastVideo)

        else:

                queue.append(lastVideo)

    if len(queue)>0 and player.is_done():

        await download(queue[0])

        queue.remove(queue[0])

    elif player.is_done() and len(queue)==0 and not user.game==discord.Game(name="{}cmds for commands".format(prefix)):

        await client.change_presence(game=discord.Game(name="{}cmds for commands".format(prefix)))

    if cooldown==1:

        await asyncio.sleep(1)

        cooldown=0

    await asyncio.sleep(1)

    checkerrun = schedule_coroutine(check())

    checkerrun





def schedule_coroutine(target, loop=None):

    if asyncio.iscoroutine(target):

        return asyncio.ensure_future(target, loop=loop)

    raise TypeError("target must be a coroutine, "

                    "not {!r}".format(type(target)))



def is_int_try(trys):

    try:

        int(trys)

        return True

    except ValueError:

        return False



# -------------------- Commands



async def cmd_search(message):

    global player

    msg=message.content[len(prefix+"search ")-1:]

    search(msg)

    if player and player.is_playing():

        queue.append(results[0])

        await client.send_message(message.channel, "Added to queue. There are now %s thing(s) in queue." % str(len(queue)))

    else:

        await download(results[0])





async def cmd_skip(message):

    if len(queue)>0:

        await client.send_message(message.channel, "Skipped.")

        player.stop()

    else:

        await client.send_message(message.channel, "No songs queued.")





async def cmd_volume(message):

    global vol

    if len(message.content) > 8:

        msg = message.content.strip(prefix + "volume ")

        isint = is_int_try(msg)

        if isint:

            imsg = int(msg)

            if imsg / 200 <= .5 and imsg / 200 >= 0:

                if player:

                    player.volume = imsg / 100

                    vol = imsg / 100

                    await client.send_message(message.channel, message.author.mention + ", set volume to " + msg + "%.")

                else:

                    await client.send_message(message.channel, message.author.mention + ", music not playing.")

            else:

                await client.send_message(message.channel, message.author.mention + ", invalid volume. Valid volumes: 0 to 100")

        else:

            await client.send_message(message.channel, message.author.mention + ", variable error.")

    else:

        await client.send_message(message.channel, message.author.mention + ", invalid syntax.")





async def cmd_pause(message):

    player.pause()

    if not user.game==None:

        await client.change_status(game=discord.Game(name="[P] "+player.title))

        await client.send_message(message.channel, "Paused.")





async def cmd_resume(message):

    player.resume()

    if not user.game==None:

        await client.change_presence(game=discord.Game(name=player.title))

        await client.send_message(message.channel, "Resumed.")





async def cmd_repeat(message):

    global queue

    global repeat

    global lastvideo

    global last

    if repeat:

        repeat = False

        queue.clear()

        await client.send_message(message.channel, "Repeat toggled off, queue has been cleared.")

        if last=="Repeat":

            print("\nRepeat toggled off. [%s]" % message.author.name)

        else:

            last=="Repeat"

            print("\n\nRepeat toggled off. [%s]" % message.author.name)

    else:

        repeat = True

        await client.send_message(message.channel, "Repeat toggled on.")

        lastVideo = player.url[len(player.url)-11:]

        if last=="Repeat":

            print("\nRepeat toggled on. [%s]" % message.author.name)

        else:

            last=="Repeat"

            print("\n\nRepeat toggled on. [%s]" % message.author.name)





async def cmd_playlist(message):

    global queue

    msg = message.content[len(prefix+"playlist "):]

    try:

        file=".\\theBot\\Playlists\\"+msg.lower()+".txt"

        await client.send_message(message.channel, "Changing queue to playlist: "+msg.lower().capitalize())

        queue.clear()

        num_lines = sum(1 for line in open(file) if line.rstrip())

        get_playlist(file)

        await client.send_message(message.channel, "Done. Some songs *MAY* not play. Playlist will not repeat. New queue item amount: %s" % str(len(queue)))

    except:

        await client.send_message(message.channel, "Playlist not found.")





async def cmd_stop(message):

    player.stop()

    await client.send_message(message.channel, "Stopped.")





async def cmd_shutdown(message):

    await client.send_message(message.channel, "Shutting down music....")

    client.close()

    exit()





async def cmd_url(message):

    await client.send_message(message.channel, message.author.mention+player.url)





async def cmd_clear(message):

    global queue

    await client.send_message(message.channel, "Queue cleared.")

    queue.clear()





async def cmd_playlists(message):

    playlists=list_files("theBot\\Playlists")

    await client.send_message(message.channel, "Playlists:\n```-"+"\n\n-".join(playlists)+"```")



# -------------------- Command Exec



@client.event

async def on_message(message):

    global cooldown

    global user

    if cooldown==0:

        if message.channel == vchannel:

            user=message.author

            if message.content.lower().startswith(prefix+"search "):

                cooldown=1

                if not acctest("Banned", message.author.id) and inChannel(message):

                    await cmd_search(message)

                else:

                    await client.send_message(message.channel, "Who dafuq you think you are? Ordering me around like that?")





            elif message.content.startswith(prefix+"skip"):

                cooldown=1

                if acctest("Extended", message.author.id) and inChannel(message):

                    await cmd_skip(message)

                else:

                    await client.send_message(message.channel, "Who dafuq you think you are? Ordering me around like that?")





            elif message.content.lower().startswith(prefix+"volume"):

                cooldown=1

                if acctest("Extended", message.author.id) and inChannel(message):

                    await cmd_volume(message)

                else:

                    await client.send_message(message.channel, "Who dafuq you think you are? Ordering me around like that?")





            elif message.content.lower().startswith(prefix+"pause"):

                cooldown=1

                if acctest("Extended", message.author.id) and inChannel(message):

                    await cmd_pause(message)

                else:

                    await client.send_message(message.channel, "Who dafuq you think you are? Ordering me around like that?")





            elif message.content.lower().startswith(prefix+"resume"):

                cooldown=1

                if acctest("Extended", message.author.id) and inChannel(message):

                    await cmd_resume(message)

                else:

                    await client.send_message(message.channel, "Who dafuq you think you are? Ordering me around like that?")





            elif message.content.lower().startswith(prefix+"repeat"):

                cooldown=1

                if acctest("Extended", message.author.id) and inChannel(message):

                    await cmd_repeat(message)

                else:

                    await client.send_message(message.channel, "Who dafuq you think you are? Ordering me around like that?")





            elif message.content.lower().startswith(prefix + "playlist ") and len(message.content)>10:

                cooldown=1

                if acctest("Extended", message.author.id) and inChannel(message):

                    await cmd_playlist(message)

                else:

                    await client.send_message(message.channel, "Who dafuq you think you are? Ordering me around like that?")





            elif message.content.lower().startswith(prefix+"stop"):

                cooldown=1

                if acctest("Extended", message.author.id) and inChannel(message):

                    await cmd_stop(message)

                else:

                    await client.send_message(message.channel, "Who dafuq you think you are? Ordering me around like that?")





            elif message.content.lower().startswith(prefix+"shutdown"):

                cooldown=1

                if acctest("Owner", message.author.id) and inChannel(message):

                    await cmd_shutdown(message)

                else:

                    await client.send_message(message.channel, "Who dafuq you think you are? Ordering me around like that?")





            elif message.content.lower().startswith(prefix+"url"):

                cooldown=1

                if not acctest("Banned", message.author.id) and inChannel(message):

                    await cmd_url(message)

                else:

                    await client.send_message(message.channel, "Who dafuq you think you are? Ordering me around like that?")





            elif message.content.lower().startswith(prefix+"clear"):

                cooldown=1

                if acctest("Extended", message.author.id) and inChannel(message):

                    await cmd_clear(message)

                else:

                    await client.send_message(message.channel, "Who dafuq you think you are? Ordering me around like that?")





            elif message.content.lower().startswith(prefix+"playlists"):

                cooldown=1

                if not acctest("Banned", message.author.id) and inChannel(message):

                    await cmd_playlists(message)

client.run(Settings.Token)
