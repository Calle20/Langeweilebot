from re import T
import discord as dc
import random
import json
import os
from discord.ext import commands


def get_config(name):
    with open("config.json", "r") as f:
        json_file=json.load(f)
    return json_file[name]

def write_user_in_config(user,trys,resultnum, started):
    jsonFile = open("config.json", "r") # Open the JSON file for reading
    data = json.load(jsonFile) # Read the JSON into the buffer
    jsonFile.close() # Close the JSON file
    data[user]={
        "trys": trys,
        "trys2": "0",
        "resultnum": resultnum,
        "left_trys": "0",
        "started": started
    }
    
    with open("config.json", "w+") as f:
        json.dump(data,f)

def write_new_data_in_user(user, trys2, left_trys):
    jsonFile = open("config.json", "r") # Open the JSON file for reading
    data = json.load(jsonFile) # Read the JSON into the buffer
    jsonFile.close() # Close the JSON file
    
    for i in data:
        if i==user:
            workuser=data[user]
            workuser["trys2"]=trys2
            workuser["left_trys"]=left_trys
            data[user]=workuser
    
    jsonFile = open("config.json", "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()

def delte_json(user):
    jsonFile = open("config.json", "r") # Open the JSON file for reading
    data = json.load(jsonFile) # Read the JSON into the buffer
    jsonFile.close() # Close the JSON file

    data.pop(user)

    jsonFile = open("config.json", "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()

def save_count(count, user, name):
    jsonFile = open("config.json", "r") # Open the JSON file for reading
    data = json.load(jsonFile) # Read the JSON into the buffer
    jsonFile.close() # Close the JSON file
    
    users=data[name]
    users[user]=count
    data[name]=users
    
    jsonFile = open("config.json", "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()

class MyClient(dc.Client):
    async def on_ready(self):
        print("Eingeloggt")
    async def on_message(self, message):
        if (message.channel.id==801346971678801930 and not message.content==".") or (message.channel.id==996417869933973504 and not message.content.startswith("lb!") and not message.author.bot):
            await message.delete()
            if not message.author.bot:
                try:
                    count=get_config("kick_user")[str(message.author)]
                except:
                    save_count(0,str(message.author),"kick_user")
                    count=0
                count=count+1
                if count==5 and not str(message.author)=="calle20#3187":
                    count=0
                    await message.author.send("Du wurdest vom Langeweile-Server gekickt, weil du in einen Channel etwas verbotenes gesendet hast.")
                    await message.author.kick()
                else:
                    fail=""
                    if message.channel.id==801346971678801930:
                        fail="einfache Punkte"
                    else:
                        fail="Zahlenraten-Befehle schreiben"
                        await message.author.send("Verwarnung! In den "+str(message.channel)+" auf dem Langeweile-Server solltest du doch nur "+fail+" schreiben! Noch "+str(5-count)+" Verwarnungen und du wirst gekickt!")
                save_count(count,str(message.author), "kick_user")
        if message.author==client.user:
            return
        elif message.content.startswith("Hallo bot"):
            await message.channel.send("Hallo wie geht es dir?")
        elif message.content.startswith("Tschüss bot"):
            await message.channel.send("Auf Wiedersehen. Hoffentlich hast du deine Langeweile überwunden. Komm bald wieder!")
        elif message.content=="lb!help":
            embed=dc.Embed(title="Hilfe", color=0xFF5733)
            embed.add_field(name="lb!helpRoulette", value="Roulette spielen", inline=False)
            embed.add_field(name="lb!helpZahlenraten", value="Zahlenraten spielen", inline=False)
            await message.channel.send(embed=embed)    
        elif message.content=="lb!helpRoulette":
            embed=dc.Embed(title="Hilfe Roulette spielen", color=0xFF5733)
            embed.add_field(name="lb!roulette {bid}", value="Roulette spielen, {bid} ist der Wert, auf den geboten wird: red, black oder 0-36", inline=False)
            await message.channel.send(embed=embed) 
        elif message.content=="lb!helpZahlenraten":
            embed=dc.Embed(title="Zahlenraten spielen", color=0xFF5733)
            embed.add_field(name="lb!startZahlenraten {range} {trys}", value="Zahlenraten starten: {range}=höchste Zahl des Zahlenbereichs, in dem die Zahl liegt; {trys} maximale Anzahl an Versuchen zum erraten der Zahl", inline=False)
            embed.add_field(name="lb!zahlenraten {guess}", value="Zahlenraten spielen: {guess}=die geratene Zahl", inline=False)
            await message.channel.send(embed=embed)    
        elif message.content.startswith("lb!roulette"):
            bid=message.content.split(" ")[1]
            bid_param=-3
            if bid.lower()=="black":
                bid_param=-1
            elif bid.lower()=="red":
                bid_param=-2
            else:
                try:
                    bid_param=int(bid)
                except:
                    bid_param=-3
            if bid_param==-3:
                await message.channel.send("Ungültige Eingabe! 'lb!helpRoulette' für weitere Hilfe")
                return
            result=random.randint(0,36)
            if bid_param==-1:
                won = result%2 == 0 and not result==0
            elif bid_param==-2:
                won = result%2 == 1
            else:
                won = result == bid_param
            if won: 
                await message.channel.send("$$$$ Du hast Gewonnen $$$$ "+str(result))
            else: 
                await message.channel.send("Verloren. Mit der Zahl "+str(result)+" hättest du gewonnen.")
        elif message.content.startswith("lb!startZahlenraten "):
            range=message.content.split(" ")[1]
            trys=message.content.split(" ")[2]
            try:
               trys=int(trys)
               range=int(range)
            except:
               await message.channel.send("Fehler! Bitte nur ganze Zahlen eingeben!")
               return
            if trys==0:
                await message.channel.send("Dein Ernst? Wie willst du mit 0 Versuchen eine Zahl erraten?")
                return
            resultnum=random.randint(0,range)
            await message.channel.send("Errate eine Zahl zwischen 0 und "+str(range)+" mit weniger als "+str(trys)+" Versuche.")
            started=True
            write_user_in_config(str(message.author), trys, resultnum, started)
        elif message.content.startswith("lb!zahlenraten "):
            trys=int(get_config(str(message.author))["trys"])
            trys2=int(get_config(str(message.author))["trys2"])
            resultnum=int(get_config(str(message.author))["resultnum"])
            left_trys=int(get_config(str(message.author))["left_trys"])
            started=get_config(str(message.author))["started"]

            if started==False:
                await message.channel.send("Zahlenraten bitte erst starten!")
            else:
                guess_param=0
                guess=message.content.split(" ")[1]
                try:
                    guess_param=int(guess)
                except:
                    await message.channel.send("Fehler! Bitte nur ganze Zahlen eingeben!")
                    delte_json(str(message.author))
                    return
                trys2=trys2+1
                left_trys=int(trys)-int(trys2)
                left_trys_str=""
                if left_trys==1:
                    left_trys_str="1 Versuch!"
                else:
                    left_trys_str=str(left_trys)+" Versuche!"
                if left_trys==0 and not guess_param==resultnum:
                    await message.channel.send("Du hast verloren!!! Die gesuchte Zahl war "+str(resultnum)+"!")
                    started=False
                    trys=0
                    trys2=0
                    resultnum=0
                    left_trys=0
                    started=False
                    delte_json(str(message.author))
                elif guess_param>resultnum:
                    await message.channel.send("Die gesuchte Zahl ist kleiner. Du hast noch "+left_trys_str)
                    write_new_data_in_user(str(message.author),trys2, left_trys)
                elif guess_param<resultnum:
                    await message.channel.send("Die gesuchte Zahl ist größer. Du hast noch "+left_trys_str)
                    write_new_data_in_user(str(message.author),trys2, left_trys)
                elif guess_param==resultnum:
                    await message.channel.send("Du hast gewonnen!!! Du hattest noch "+left_trys_str)
                    trys=0
                    trys2=0
                    resultnum=0
                    left_trys=0
                    started=False
                    delte_json(str(message.author))
        elif message.content.startswith("lb!"):
            await message.channel.send("Das ist mein Prefix. Was gibts? lb!help für Hilfe.")
        c_channel = dc.utils.get(message.author.guild.text_channels, name='counter')
        messages = await c_channel.history(limit=2).flatten()
        if message.channel == c_channel and int(messages[1].content) + 1 != int(message.content):
            await message.delete()
            await message.channel.send("Hey <@"+str(message.author.id)+">! Lern mal zählen bevor du hier anfängst zu zählen!",delete_after=3)

        if isinstance(message.channel, dc.channel.DMChannel):
            print(str(message.author)+": "+message.content)
    async def on_typing(self, channel, user, when):
        try:
            double=get_config("double_counter")[str(user)]
        except:
            save_count("0 "+str(channel.id),str(user),"double_counter")
            double="0 "+str(channel.id)
        double_count=int(double.split(" ")[0])
        channel_id=int(double.split(" ")[1])
        if channel.id==channel_id:
            if not double_count==4:
                double_count=double_count+1
            else:
                double_count=0
                await channel.send("Jetzt sende doch endlich mal deine Nachricht <@"+str(user.id)+">. Was dauert da so lange? Romane lese ich nicht gerne!")
        else:
            double_count=0
            channel_id=channel.id
        double=str(double_count)+" "+str(channel_id)
        save_count(double,str(user), "double_counter")
    async def on_raw_reaction_add(self, payload):
        channel=client.get_channel(payload.channel_id)
        user = payload.member
        among_us=dc.utils.get(user.guild.roles,name="Among Us Player")
        programmer=dc.utils.get(user.guild.roles,name="Programmierer")
        minecraft=dc.utils.get(user.guild.roles,name="Minecraft Player")
        langeweile=dc.utils.get(user.guild.roles,name="Langeweile")
        members=dc.utils.get(user.guild.roles,name="members")
        selfroles=client.get_channel(810178026527653898)
        rules=client.get_channel(818767129050349578)

        if str(payload.emoji)=="✅"and channel==rules:
            await user.add_roles(members)
        if str(payload.emoji)=="🟨"and channel==selfroles:
            await user.add_roles(among_us)
        if str(payload.emoji)=="🟦"and channel==selfroles:
            await user.add_roles(programmer)
        if str(payload.emoji)=="🟥"and channel==selfroles:
            await user.add_roles(minecraft)
        if str(payload.emoji)=="<:Langeweile:997830237947703347>"and channel==selfroles:
            await user.add_roles(langeweile)
    async def on_raw_reaction_remove(self, payload):
        channel=client.get_channel(payload.channel_id)
        guild = client.get_guild(payload.guild_id)
        user = await(guild.fetch_member(payload.user_id))

        among_us=dc.utils.get(guild.roles,name="Among Us Player")
        programmer=dc.utils.get(guild.roles,name="Programmierer")
        minecraft=dc.utils.get(guild.roles,name="Minecraft Player")
        langeweile=dc.utils.get(guild.roles,name="Langeweile")
        members=dc.utils.get(guild.roles,name="members")
        selfroles=client.get_channel(810178026527653898)
        rules=client.get_channel(818767129050349578)

        if str(payload.emoji)=="✅"and channel==rules:
            await user.remove_roles(members)
        if str(payload.emoji)=="🟨"and channel==selfroles:
            await user.remove_roles(among_us)
        if str(payload.emoji)=="🟦"and channel==selfroles:
            await user.remove_roles(programmer)
        if str(payload.emoji)=="🟥"and channel==selfroles:
            await user.remove_roles(minecraft)
        if str(payload.emoji)=="<:Langeweile:997830237947703347>"and channel==selfroles:
            await user.remove_roles(langeweile)

client=MyClient()
##client.run(os.environ["BOT_TOKEN"])
client.run("OTg5OTMxMDgxOTc5NTMxMzE1.GF7Q5V.fQ0YOKiFI63X9Z3E67c3JbiqJ4UfYsO7fpdtVo")