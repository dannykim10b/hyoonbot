# bot.py
import os
import random
import discord
import json

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!hyoon ')

@bot.event
async def on_ready():
   print("Ready")

@bot.command(name='roll', help='view the queen')
async def hyoon(ctx):

    hyoonList = os.listdir("./images/")
    # hyoonString = "forbiddenhyoon.jpg"
    hyoonString = random.choice(hyoonList)
    hyoonStringCleaned = hyoonString.split('.')[0]

    descriptionMessage = ''

    with open('hyoon.json', 'r+') as jsonFile:
        hyoonJson = json.load(jsonFile)

    user_id = str(ctx.author.id)
    username = await bot.fetch_user(user_id)
    userFound = False
    forbiddenHyoonFound = False

    for user in hyoonJson['hyoonLeaderboard']:
        if user['id'] == user_id:
            user['totalHyoons'] += 1
            userFound = True
            if hyoonStringCleaned == 'forbiddenhyoon':
                user['forbiddenHyoons'] += 1
                descriptionMessage = str(username) + ' has found the forbidden hyoon!'
            user['forbiddenHyoonPercentage'] = user['forbiddenHyoons']/user['totalHyoons']
            break

    if not userFound:
        if hyoonStringCleaned == 'forbiddenhyoon':       
            userData = {
                "id": user_id,
                "forbiddenHyoons": 1,
                "totalHyoons": 1,
                "forbiddenHyoonPercentage": 1,
            }
            descriptionMessage = str(username) + ' has found the forbidden hyoon!'
        else:
            userData = {
                "id": user_id,
                "forbiddenHyoons": 0,
                "totalHyoons": 1,
                "forbiddenHyoonPercentage": 0.00
            }
        with open('hyoon.json', 'w') as jsonFile:
            hyoonJson['hyoonLeaderboard'].append(userData)
            jsonFile.seek(0)
            json.dump(hyoonJson, jsonFile)

    # if hyoonStringCleaned == 'forbiddenhyoon':
    #     found = False
    #     for user in hyoonJson['hyoonLeaderboard']:
    #         if user['id'] == user_id:
    #             user['forbiddenHyoons'] += 1
    #             found = True
    #             break
    #     if not found:
    #         userData = {
    #             "id": user_id,
    #             "forbiddenHyoons": 1
    #         }      
    #         with open('hyoon.json', 'w') as jsonFile:
    #             hyoonJson['hyoonLeaderboard'].append(userData)
    #             jsonFile.seek(0)
                # json.dump(hyoonJson, jsonFile)

    if hyoonStringCleaned not in hyoonJson['hyoonStats']:
        hyoonJson['hyoonStats'][hyoonStringCleaned] = 1
    else:
        hyoonJson['hyoonStats'][hyoonStringCleaned] += 1

    with open('hyoon.json', 'w') as jsonFile:
        json.dump(hyoonJson, jsonFile)

    path = "./images/" + hyoonString

    file = discord.File(path)
    e = discord.Embed(title="Give us this day our daily hyoon", description=descriptionMessage)
    e.set_image(url="attachment://" + hyoonString)
    await ctx.send(file = file, embed = e)

@bot.command(name='stats', help='view hyoon stats')
async def hyoonstats(ctx):

    regularHyoon = 0
    forbiddenHyoon = 0
    mostCommonHyoon = ''
    mostCommonHyoonCount = 0
    with open('hyoon.json', 'r') as json_file:
        data = json.load(json_file)
        for hyoon in data['hyoonStats']:
            if hyoon == 'forbiddenhyoon':
                forbiddenHyoon += data['hyoonStats'][hyoon]
            else:
                regularHyoon += data['hyoonStats'][hyoon]
                if data['hyoonStats'][hyoon] > mostCommonHyoonCount:
                    mostCommonHyoon = hyoon + '.jpg'
                    mostCommonHyoonCount = data['hyoonStats'][hyoon]

    path = "./images/" + mostCommonHyoon
    file = discord.File(path)
    forbiddenHyoonPercentage = (forbiddenHyoon/(regularHyoon + forbiddenHyoon)) * 100
    statsText = "Regular Hyoons: " + str(regularHyoon) + "\n" + "Forbidden Hyoons: " + str(forbiddenHyoon) + "\n" + "Forbidden Hyoon Percentage: " + f'{forbiddenHyoonPercentage:.2f}' + "%\nMost Common Hyoon Count: " + str(mostCommonHyoonCount)
    e = discord.Embed(title="Hyoon Stats", description=statsText)
    e.set_image(url="attachment://" + mostCommonHyoon)
    await ctx.send(file=file, embed = e)

@bot.command(name='lb', help='view hyoon leaderboard')
async def hyoonlb(ctx):

    with open('hyoon.json', 'r') as json_file:
        data = json.load(json_file)

    totalForbiddenHyoonsDescription = ''
    forbiddenHyoonPercentageDescription = ''
    sortedDataTotal = dict(data)
    sortedDataTotal['hyoonLeaderboard'] = sorted(data['hyoonLeaderboard'], key=lambda x : x['forbiddenHyoons'], reverse=True)
    sortedDataPercentage = dict(data)
    sortedDataPercentage['hyoonLeaderboard'] = sorted(data['hyoonLeaderboard'], key=lambda x : x['forbiddenHyoonPercentage'], reverse=True)
    for rank, user in enumerate(sortedDataTotal['hyoonLeaderboard']):
        if rank > 4:
            break
        username = await bot.fetch_user(user['id'])
        totalForbiddenHyoonsDescription = totalForbiddenHyoonsDescription + str(rank + 1) + ". " + str(username) + ": " + str(user['forbiddenHyoons']) + " forbidden hyoons\n"

    for rank, user in enumerate(sortedDataPercentage['hyoonLeaderboard']):
        if rank > 4:
            break
        percent = user['forbiddenHyoonPercentage']*100
        username = await bot.fetch_user(user['id'])
        forbiddenHyoonPercentageDescription = forbiddenHyoonPercentageDescription + str(rank + 1) + ". " + str(username) + ": " + f'{percent:.2f}%' + " forbidden hyoons\n"

    file = discord.File("./images/forbiddenhyoon.jpg")
    e = discord.Embed(title="Hyoon Leaderboard")
    e.add_field(name="Total Forbidden Hyoons", value=totalForbiddenHyoonsDescription, inline = False)
    e.add_field(name="Forbidden Hyoon Percentage", value =forbiddenHyoonPercentageDescription, inline = False)
    e.set_image(url="attachment://forbiddenhyoon.jpg")
    await ctx.send(file=file, embed = e)

@bot.command(name='dateme', help='ask hyoon on a date')
async def hyoondateme(ctx):
    
    path = "./images/hyoon54.jpg"

    file = discord.File(path)
    e = discord.Embed(title="Confess to Hyoon!", description="\"Sorry, I'm dating Alex right now!\"")
    e.set_image(url="attachment://hyoon54.jpg")
    await ctx.send(file = file, embed = e)

bot.run(TOKEN)