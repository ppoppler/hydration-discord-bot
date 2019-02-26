import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import time
import sqlite3
import random
import functools

""" Thirsty Member Class

Child class of discord.Member That contains one extra attribute: Thirst
thirst = A counter that tracks the user's thirstiness. 
Everything else is manually copied into the

"""
class ThirstyMember(discord.Member):
    def __init__(self,member):
        #super().__init__(**kwargs.get('user'))
        self.id = member.id
        self.discriminator = member.discriminator
        self.avatar = member.avatar
        self.name = member.name
        self.bot = member.bot
        self.permissions_in = member.permissions_in
        self.mentioned_in = member.mentioned_in
        self.voice = member.voice
        self.joined_at = member.joined_at
        self.roles = member.roles
        self.status = member.status
        self.game = member.game
        self.server = member.server
        self.nick = member.nick
        self.thirst = 0

def createDatabase():
    # Connecting to Facts database 
    connection = sqlite3.connect("Facts.db")

    # cursor
    crsr = connection.cursor()

    # SQL command to create a table in the Facts database
    print('Creating database...')
    sql_command = """DROP TABLE Facts;"""
    #sql_command = """CREATE TABLE Facts (
    #    info VARCHAR(400),
    #    number INT PRIMARY KEY);"""

    # Execute the command statement
    crsr.execute(sql_command)
    connection.commit()
    print('Database cretaed')

def createPhrasesDatabase():
    connection = sqlite3.connect("Responses.db")
    crsr = connection.cursor()
    print('Creating thirst response database')
    sql_command = """CREATE TABLE ThirstResponses (
            Response VARCHAR(400) PRIMARY KEY,
            ThirstLevel INT)"""
    crsr.execute(sql_command)
    connection.commit()
    print('Responses Database Created')
    
#createPhrasesDatabase()

def modifyDatabase(): 
    print("[ Beginning modification of Facts.db ]")
    connection = sqlite3.connect("Facts.db")
    crsr = connection.cursor()
    with open(r'C:\Users\Philip\Desktop\Hydration Bot\facts.txt') as f:
        content = f.readlines()
        content = [line.strip() for line in content]
    for i in range (0,len(content)):
        number = i+1
        print('Fact ' + str(number) + ': ' + content[i])
        sql_command = """INSERT INTO Facts VALUES ('{}',{});""".format(content[i],number)
        crsr.execute(sql_command)
        print("[ Fact " + str(number) + " added]")
        
    print("[ Saving database information... ]")
    connection.commit()
    print("[ Closing database connection... ]")
    connection.close()

#modifyDatabase()
def getFacts(): 
    print("[ Loading facts from Facts.db...] ")
    connection = sqlite3.connect("C:\\Users\Philip\Desktop\Hydration Bot\Facts.db")
    crsr = connection.cursor()
    crsr.execute('SELECT * FROM Facts;')
    facts = crsr.fetchall()
    print("[ "+ str(len(facts)) + " facts retrieved from Facts.db ]")
    return facts

def getResponses():
    print("[ Loading Thirst Responses from Responses.db...] ")
    connection = sqlite3.connect("C:\\Users\Philip\Desktop\Hydration Bot\Responses.db")
    crsr = connection.cursor()
    crsr.execute('SELECT Response FROM ThirstResponses WHERE ThirstLevel = 1;' )
    lt = crsr.fetchall()
    crsr.execute('SELECT Response FROM ThirstResponses WHERE ThirstLevel = 2;' )
    mt = crsr.fetchall()
    crsr.execute('SELECT Response FROM ThirstResponses WHERE ThirstLevel = 3;' )
    ht = crsr.fetchall()
    low_thirst = []
    med_thirst = []
    hi_thirst = []
    
    for n in range(0, len(lt)):
        low_thirst.append(lt[n][0])
    for n in range(0,len(mt)):
        med_thirst.append(mt[n][0])
    for n in range(0,len(ht)):
        hi_thirst.append(ht[n][0])
    message = low_thirst[0].format("Phil,",str(30))
    print("[ MESSAGE TEST: "  + message + " ]")
    print(low_thirst)
    print(med_thirst)
    print(hi_thirst)
    ThirstMessages = (low_thirst,med_thirst,hi_thirst)
    return ThirstMessages
   
def randomizeThirstMessage(thirst):
    if(thirst>=3):
        thirst = 3
    thirst= thirst - 1 
    message = random.choice(ThirstMessages[thirst])
    return message

ThirstMessages = getResponses()
facts = getFacts()
Client = discord.Client()
bot = commands.Bot(command_prefix='+')

#    On Ready:
# Produces debuggin code on start up
@bot.event
async def on_ready():
    print("Testing, testing")
    print("I am " + bot.user.name)

#    On Voice State Update
# Whenever a user changes voice
@bot.event
async def on_voice_state_update(old,new):
    #print(old.voice.voice_channel == None)
    #print(new.voice.voice_channel == None)
    # Collect user ID who joined
    old = ThirstyMember(old)
    new = ThirstyMember(new)
    userID = new.id
    startHydration = False
    textChannel = None
    # When a user joins a voice channel (and wasn't already in a voice channel)
    if(old.voice.voice_channel is None and new.voice.voice_channel is not None):
        # Collect channel name
        channel = new.voice.voice_channel.name
        for txtchannel in new.server.channels:
            # Find main text channel
            if txtchannel.name == 'general':
                # Remember text Channel name
                textChannel = txtchannel
                print("Hydration Bot sending a hydration message")
                # Send a message to the text Channel
                await bot.send_message(txtchannel,new.name + " joined " + channel)
                # Start the Hyrdation Loop
                startHydration = True
                break
    if(old.voice.voice_channel is not None and new.voice.voice_channel is None):
        new.thirst = 0
        print(new.name + " 's thirst has gone down back to zero.")

    # While the Hydration Loop is active, and the user leaves from all voice channels
    while(startHydration and new.voice.voice_channel is not None and userID is old.id):
        # 1800 = 30 Minutes
        # 1200 = 20 Minutes
        # 60 = 1 Minute
        interval = 60
        
        # Sleep for that amount, to delay the message
        await asyncio.sleep(interval)
        # Calculate the number of minutes
        minutes = int(interval/60)
        # If the user left voice
        if(new.voice.voice_channel is None and userID is old.id):
            # Don't display the message and break the thread
            print("Ending Hydration loop for User: " + userID)
            break
        # Otherwise display the message 
        if(drink.has_been_called is False and new.thirst == 1):
            message = randomizeThirstMessage(new.thirst)
            await bot.send_message(textChannel, message.format(new.name,str(minutes)))
        # If the thirst is at two and they haven't drinked
        elif(drink.has_been_called is False and new.thirst == 2):
            message = randomizeThirstMessage(new.thirst)
            await bot.send_message(textChannel,message.format(new.name,str(minutes)))
        # If the thirst is greater than or equal to three and they haven't drinked 
        elif(drink.has_been_called is False and new.thirst >= 3):
            message = randomizeThirstMessage(new.thirst)
            await bot.send_message(textChannel, message.format(new.name,str(minutes)))
        
       # Increment Thirst Meter
        new.thirst+=1 
        
        # If the user did drink 
        #if(drink.has_been_called is True):
        #    print(str(drink.id==new.id) + " " +  str(drink.has_been_called))
        # If the user did drink and the user is the started Hydration (their ID can be identified)
        if drink.has_been_called is True and drink.id == new.id:
            print('[ User ' + new.name + ' drank in server: ' + new.server.name + ', in channel: ' + new.voice.voice_channel.name + ' ]')
            print('[ User' + new.name + "'s thirst level decreased by 1 ] ")
            if(new.thirst >=1):
                new.thirst-= drink.number_of_drinks
                if(new.thirst<0):
                    new.thirst = 0
            await bot.send_message(textChannel, "Great job hydrating " + new.name + "!")
        print('[ User ' + new.name + "'s current thirst level: " + str(new.thirst) + " ]")
        
        drink.has_been_called = False

# Basic Hello command       
@bot.command(pass_context=True)
async def hello(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.message.author
    await bot.say("Hello " + user.name + "! :potable_water: Remember to drink water!")
    print ("User " + user.name + " initiated #hello command" )
    print(user.joined_at)

# Fact Reader that reads from 80 differetn facts in a database. 
# Database contains a number identifier as a primary key and a fact string that can store up to 500 characters 
@bot.command(pass_context=True)
async def fact(ctx, user: discord.Member = None):
    if user is None:
        user = ctx.message.author
    server = ctx.message.server
    channel = ctx.message.channel
    fact = random.choice(facts)
    #Debug
    print('[ Fact '+ str(fact[1]) + " selected for " + user.name + " in server: " + server.name + ", in channel: " + channel.name + " ] ")
    message = "Fact " + str(fact[1]) + ": " + fact[0] 
    await bot.send_message(channel, message)

#Wrapper that sends the ID and 
def calltracker(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.has_been_called = True
        wrapper.id = 0
        wrapper.number_of_drinks = 0
        return func(*args, **kwargs)
    wrapper.has_been_called = False
    wrapper.number_of_drinks = 0
    return wrapper

#NEEDS COMMENTS
@calltracker
@bot.command(pass_context=True)
async def drink(ctx, user:ThirstyMember = None):
    if user is None:
        user = ThirstyMember(ctx.message.author)
    await bot.send_message(ctx.message.channel, user.name + " drank some water. Great job hydrating!")
    drink.id = user.id
    drink.number_of_drinks = drink.number_of_drinks + 1
    drink.has_been_called = True
    print("[ User " + user.name + " hydrated " + str(drink.number_of_drinks) + " times during the time interval ]")
     
# Displays chatlog in console 
@bot.event
async def on_message(message):   
    await bot.process_commands(message)
    author = message.author
    content = message.content
    print('{}: {}'.format(author,content))
    

bot.run("NDU5NjEwNzI4MDU2MzU2ODY0.Dg4tdA.ypAGqVWDHBXpikEFrtS-ly2kFCY")
