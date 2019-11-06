import discord, json

TOKEN = 'YEET'
client = discord.Client()

@client.event
async def on_ready():
    print("The bot is ready!")
    activity = discord.Activity(name='no-gijs-pest-november', type=discord.ActivityType.playing)
    await client.change_presence(activity=activity)

@client.event
async def on_message(message):
    valid_users = ["Bengelboef#6632"]

    if message.author == client.user:
        return
    commandList = message.content.split(' ')
    if commandList[0] == '!add' and str(message.author) in valid_users:
        with open('strikes.json', 'r') as file:
            data = json.load(file)
            for item in data:
                if item["Name"] == commandList[1].lower():
                    item["Strikes"] += int(commandList[2])
                    await message.channel.send('{} krijgt er {} strike(s) bij, en heeft er nu {}'.format(item["Name"].capitalize(), commandList[2], item["Strikes"]))
        with open('strikes.json', 'w') as file:
            json.dump(data, file, indent=4)
    elif commandList[0] == '!remove' and str(message.author) in valid_users:
        with open('strikes.json', 'r') as file:
            data = json.load(file)
            for item in data:
                if item["Name"] == commandList[1].lower():
                    item["Strikes"] -= int(commandList[2])
                    await message.channel.send('{} krijgt {} strike(s) minder, en heeft er nu {}'.format(item["Name"].capitalize(), commandList[2], item["Strikes"]))
        with open('strikes.json', 'w') as file:
            json.dump(data, file, indent=4)
    elif commandList[0] == '!rank':
        with open('strikes.json', 'r') as file:
            data = json.load(file)
            sortedData = sorted(data, key=lambda item: item["Strikes"], reverse=True)
            for item in sortedData:
                await message.channel.send('{}: {}'.format(item["Name"].capitalize(), item["Strikes"]))
    elif commandList[0] == '!add' or '!remove' and str(message.author) not in valid_users:
        await message.channel.send('Volgens mij heet jij geen Gijs...')

client.run(TOKEN)