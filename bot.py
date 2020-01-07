import json, discord
from datetime import datetime

TOKEN = 'NjM3MzM1MTQyNTgyNzE0Mzc4.XhIzUw.ya-R_UIdjnBVMzpB_qxu-6c4EXQ'
client = discord.Client()
global lastReaction
lastReaction = None

@client.event
async def on_ready():
    activity = discord.Activity(name='niet-pesten-januari', type=discord.ActivityType.playing)
    await client.change_presence(activity=activity)
    print("The bot is ready!")

@client.event
async def on_message(message):
    # makes sure bot doesnt react on own messages
    if message.author == client.user:
        return

    #users that can call a vote
    valid_users = ["Plumboi#6362", "Bengelboef#6632", "Je boy uit de inbraakhoofdstad#8452", "Sietse#8543",
                   "Maarten_C#4774", "DaanLettah#1610", "Robvanmourik#0331"]
    admins = ["Plumboi#6362", "Je boy uit de inbraakhoofdstad#8452"]

    #tests if message is command
    if message.content[0] == '!':
        global commandList
        commandList = message.content.split(' ', 2 )
        print(commandList)
        server = discord.Guild.id

        #executes vote command on '!jankerd'
        if commandList[0].lower() == '!jankerd' and str(message.author) in valid_users:

            #gets members in voice channel
            voice_channel = client.get_channel(527919083618828288)
            members = voice_channel.members
            #makes sure bots arent counted
            """for member in members:
                if member.bot == True:
                    members.remove(member)"""
            #counts number of people in voice channel
            numberOfMembers = len(members)

            if numberOfMembers < 2:
                await message.channel.send('er zijn niet genoeg mensen in de voice chat om een vote te beginnen.')
                return
            else:
                global votesRequired
                votesRequired = round(numberOfMembers/2)+1
                vote = await message.channel.send('{} noemt {} een jankerd om de rede \'{}\', vind je dit terecht, stem dan hieronder.\n'
                                                  'Er zijn {} stemmen nodig.'.format(message.author.display_name, commandList[1], commandList[2], votesRequired))
                await vote.add_reaction('⬆')
                await vote.add_reaction('⬇')
                global lastVote
                lastVote = vote.content
                await message.delete()

        #executes reasons command on !redenen
        if commandList[0].lower() == '!redenen':
            with open('strikes.json', 'r') as file:
                data = json.load(file)
                for item in data:
                    if commandList[1] == item["DiscordID"] or commandList[1].lower() == item["Name"]:
                        redenen_message = str()
                        redenen_message += '{} heeft {} keer zitten janken. \n'.format(item["Name"].capitalize(), len(item["Strikes"]))
                        for strike in item["Strikes"]:
                            redenen_message += '{}. \'{}\' op {} om {} \n'.format(strike["StrikeID"], strike["Reason"], strike["Date"], strike["Time"])
                        await message.channel.send(str(redenen_message))

        #executes remove command on !remove WIP
        """if commandList[0].lower() == '!remove' and str(message.author) in admins:
            with open('strikes.json', 'r') as file:
                data = json.load(file)
                for item in data:
                    if item["DiscordID"] == commandList[1]:
                        for i in range(len(item["Strikes"])):
                            if str(item["Strikes"][i]['StrikeID']) == commandList[2]:
                                del item["Strikes"][i]
                                await message.channel.send('yeetus deletus {}'.format(i))
        """
        #execute rank command on !rank
        if commandList[0].lower() == '!rank':
            rank_message = 'De score op het moment:\n'
            with open('strikes.json', 'r') as file:
                data = json.load(file)
                sortedData = sorted(data, key=lambda item: len(item["Strikes"]), reverse=True)
                number = 1
                for item in sortedData:
                    rank_message += '{}. {} met {} jankmomenten.\n'.format(number, item["Name"].capitalize(), len(item["Strikes"]))
                    number += 1
                await message.channel.send(rank_message)

        #execute help command on !help
        if commandList[0].lower() == '!help':
            await message.channel.send('1. !jankerd <persoon> <reden> (start een vote) \n'
                                       '2. !redenen <persoon> (zie alle jankmomenten voor deze persoon)\n'
                                       '3. !rank (zie wie de meeste jankmomenten heeft gehad tot nu toe)')

@client.event
async def on_reaction_add(reaction, user):
    channel = reaction.message.channel
    votes = 1
    tegenVotes = 1
    if user != client.user:
        #await channel.send('{} added {}'.format(user.display_name, reaction.emoji))
        if reaction.message.content == lastVote and reaction.emoji == '⬆':
            votes += 1
            if votes == votesRequired:
                await reaction.message.delete()

                #add strike to json file
                with open('strikes.json', 'r') as file:
                    data = json.load(file)
                    print(commandList[1])
                    for item in data:
                        if commandList[1] == item["DiscordID"]:
                            strike = {"StrikeID": (len(item["Strikes"])+1),
                                      "Reason": commandList[2],
                                      "Date": str(datetime.now().strftime("%d/%m/%Y")),
                                      "Time": str(datetime.now().strftime("%H:%M:%S"))
                                     }
                            item["Strikes"].append(strike)
                            await channel.send('vote passed: \'{}\', {} heeft nu {} keer zitten janken.'.format(commandList[2], commandList[1], len(item["Strikes"])))
                with open('strikes.json', 'w') as file:
                    json.dump(data, file, indent=4)

        elif reaction.emoji == '⬇':
            tegenVotes +=1
            if tegenVotes == votesRequired:
                await channel.send('vote not passed: {} om de reden \'{}\'.'.format(commandList[1], commandList[2]))
                await reaction.message.delete()


client.run(TOKEN)