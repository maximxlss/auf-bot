from discord import *
import os

client = Client()

# get enviroment variables and check if they are present
CHANNEL_ID = os.environ.get("TEXT_CHANNEL_ID")
TOKEN = os.environ.get("DISCORD_TOKEN")

if not CHANNEL_ID:
    raise Exception("can't get text channel id from enviroment")
if not TOKEN:
    raise Exception("can't get token from enviroment")

# make CHANNEL_ID an integer
CHANNEL_ID = int(CHANNEL_ID)

# global TextChannel of configured text channel
# gets set up in on_ready
textch = None

# sets up everything that needs auntefication
@client.event
async def on_ready():
    global textch
    textch = client.get_channel(CHANNEL_ID)
    print("redy")

# VOICE NOTIFY FUNCTIONALITY ------------------------------
# sends a notify into configured text channel when user leaves, reconnects or joins voice channel
async def voice_notify_callback(member, before, after):
    if before.channel != None and before.channel.guild != textch.guild:
        return
    if after.channel != None and after.channel.guild != textch.guild:
        return
    if before.channel != None and after.channel == None:
        await textch.send(f"**{member.display_name}** вышел из чата **{before.channel.name}**")
    elif before.channel == None and after.channel != None:
        await textch.send(f"**{member.display_name}** присоединился к чату **{after.channel.name}**")
    elif before.channel != after.channel:
        await textch.send(f"**{member.display_name}** переместился из чата **{before.channel.name}** в чат **{after.channel.name}**")
# VOICE NOTIFY FUNCTIONALITY END --------------------------

# TEXT CHANNEL FOR VOICE FUNCTIONALITY --------------------
# makes configured text channel visible only for people in voice
async def text_for_voice_callback(member, before, after):
    if before.channel != None and before.channel.guild != textch.guild:
        return
    if after.channel != None and after.channel.guild != textch.guild:
        return
    overwrites = textch.overwrites
    if before.channel != None and after.channel == None:
        try:
            overwrites[member].view_channel = False
        except KeyError:
            overwrites = {**overwrites, member: PermissionOverwrite(view_channel=False)}
    elif before.channel == None and after.channel != None:
        try:
            overwrites[member].view_channel = True
        except KeyError:
            overwrites = {**overwrites, member: PermissionOverwrite(view_channel=True)}
    await textch.edit(overwrites=overwrites)
# TEXT CHANNEL FOR VOICE FUNCTIONALITY END ----------------

# set up callbacks
@client.event
async def on_voice_state_update(member, before, after):
    await voice_notify_callback(member, before, after)
    await text_for_voice_callback(member, before, after)

client.run(TOKEN)
