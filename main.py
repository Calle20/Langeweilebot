from re import T
import discord as dc
import random

trys=0
trys2=0
resultnum=0
left_trys=0
started=False



class MyClient(dc.Client):
    async def on_ready(self):
        print("Eingeloggt")
    async def on_message(self, message):
        if message.author==client.user:
            return
        if message.content.startswith("Hallo bot"):
            await message.channel.send("Hallo wie geht es dir?")
        if message.content.startswith("Tschüss bot"):
            await message.channel.send("Auf Wiedersehen. Hoffentlich hast du deine Langeweile überwunden. Komm bald wieder!")
        if message.content=="lb!help":
            embed=dc.Embed(title="Hilfe", color=0xFF5733)
            embed.add_field(name="lb!helpRoulette", value="Roulette spielen", inline=False)
            embed.add_field(name="lb!helpZahlenraten", value="Zahlenraten spielen", inline=False)
            await message.channel.send(embed=embed)    
        if message.content=="lb!helpRoulette":
            embed=dc.Embed(title="Hilfe Roulette spielen", color=0xFF5733)
            embed.add_field(name="lb!roulette {bid}", value="Roulette spielen, {bid} ist der Wert, auf den geboten wird: red, black oder 0-36", inline=False)
            await message.channel.send(embed=embed) 
        if message.content=="lb!helpZahlenraten":
            embed=dc.Embed(title="Zahlenraten spielen", color=0xFF5733)
            embed.add_field(name="lb!startZahlenraten {range} {trys}", value="Zahlenraten starten: {range}=höchste Zahl des Zahlenbereichs, in dem die Zahl liegt; {trys} maximale Anzahl an Versuchen zum erraten der Zahl", inline=False)
            embed.add_field(name="lb!zahlenraten {guess}", value="Zahlenraten spielen: {guess}=die geratene Zahl", inline=False)
            await message.channel.send(embed=embed)    
        if message.content.startswith("lb!roulette"):
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
        if message.content.startswith("lb!startZahlenraten "):
           global trys, trys2, resultnum, left_trys
           range=message.content.split(" ")[1]
           trys=message.content.split(" ")[2]
           try:
               trys=int(trys)
               range=int(range)
           except:
               await message.channel.send("Fehler! Bitte nur ganze Zahlen eingeben!")
               return
           resultnum=random.randint(0,range)
           await message.channel.send("Errate eine Zahl zwischen 0 und "+str(range)+" mit weniger als "+str(trys)+" Versuche.")
           global started
           started=True
        if message.content.startswith("lb!zahlenraten "):
            if started==False:
                await message.channel.send("Zahlenraten bitte erst starten!")
            else:
                guess_param=0
                guess=message.content.split(" ")[1]
                try:
                    guess_param=int(guess)
                except:
                    await message.channel.send("Fehler! Bitte nur ganze Zahlen eingeben!")
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
                elif guess_param>resultnum:
                    await message.channel.send("Die gesuchte Zahl ist kleiner. Du hast noch "+left_trys_str)
                elif guess_param<resultnum:
                    await message.channel.send("Die gesuchte Zahl ist größer. Du hast noch "+left_trys_str)
                elif guess_param==resultnum:
                    await message.channel.send("Du hast gewonnen!!! Du hattest noch "+left_trys_str)
                    trys=0
                    trys2=0
                    resultnum=0
                    left_trys=0
                    started=False
client=MyClient()
client.run("OTg5OTMxMDgxOTc5NTMxMzE1.GF7Q5V.fQ0YOKiFI63X9Z3E67c3JbiqJ4UfYsO7fpdtVo")