from email import message
from re import T
import discord as dc
import random
import json

double=0

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

def save_kick_count(count, user):
    jsonFile = open("config.json", "r") # Open the JSON file for reading
    data = json.load(jsonFile) # Read the JSON into the buffer
    jsonFile.close() # Close the JSON file
    
    users=data["kick_user"]
    users[user]=count
    data["kick_user"]=users
    
    jsonFile = open("config.json", "w+")
    jsonFile.write(json.dumps(data))
    jsonFile.close()

class MyClient(dc.Client):
    async def on_ready(self):
        print("Eingeloggt")
    async def on_message(self, message):
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
        if message.channel.id==801346971678801930 and not message.content==".":
            await message.delete()
            try:
                count=get_config("kick_user")[str(message.author)]
            except:
                save_kick_count(0,str(message.author))
                count=0
            count=count+1
            if count==5 and not str(message.author)=="calle20#3187":
                count=0
                await message.author.send("Du wurdest vom Langeweile-Server gekickt, weil du zu oft keinen Punkt in den punkte-kanal geschickt hast.")
                await message.author.kick()
                
            else:
                await message.author.send("Verwarnung! In den Punkte-Kanal auf dem Langeweile-Server solltest du doch nur einfache Punkte schreiben! Noch "+str(5-count)+" Verwarnungen und du wirst gekickt!")
            save_kick_count(count,str(message.author))
    async def on_typing(self, channel, user, when):
        global double
        if not double==4:
            double=double+1
        else:
            double=0
            await channel.send("Jetzt sende doch endlich mal deine Nachricht <@"+str(user.id)+">. Was dauert da so lange? Romane lese ich nicht gerne!")
    async def on_message_delete(self, message):
        pass
    async def on_message_edit(self, before, after):
        pass
    ##Aufgabe: Mod tool um user zu beobachten, die mist bauen 
    async def on_reaction_add(self, reaction, user):
        await reaction.message.channel.send("Reagiert ")

client=MyClient()
client.run("OTg5OTMxMDgxOTc5NTMxMzE1.GF7Q5V.fQ0YOKiFI63X9Z3E67c3JbiqJ4UfYsO7fpdtVo")