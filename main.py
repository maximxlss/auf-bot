from discord import *
import os

client = Client()

CHANNEL_ID = 853587303100448778
TOKEN = os.environ.get("DISCORD-TOKEN")

textch = None

if not TOKEN:
    raise Exception("can't get token from enviroment")

@client.event
async def on_ready():
    global textch
    textch = client.get_channel(CHANNEL_ID)


@client.event
async def on_voice_state_update(member, before, after):
    global textch
    overwrites = textch.overwrites
    if before.channel != None and after.channel == None:
        try:
            overwrites[member].view_channel = False
        except KeyError:
            overwrites = {**overwrites, member: PermissionOverwrite(view_channel=False)}
        await textch.send(f"**{member.display_name}** вышел из чата **{before.channel.name}**")
    elif before.channel == None and after.channel != None:
        try:
            overwrites[member].view_channel = True
        except KeyError:
            overwrites = {**overwrites, member: PermissionOverwrite(view_channel=True)}
        await textch.send(f"**{member.display_name}** присоединился к чату **{after.channel.name}**")
    elif before.channel != None and after.channel != None:
        await textch.send(f"**{member.display_name}** переместился из чата **{before.channel.name}** в чат **{after.channel.name}**")
    await textch.edit(overwrites=overwrites)

client.run(TOKEN)
