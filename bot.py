import discord, drive, random, database
from discord.ext import commands

PREFIX = '!'
TOKEN = 'NDU1NTQ1NTAyNjEyNzE3NTg4.Df9jZw.wDK4S-bWQX4uREGh3zx2EJUiO9o'
bot = commands.Bot(command_prefix=PREFIX, description='A bot that plays the d or no d game.')
NUM = {'d': 0, 'no_d':1}

unique_id = 78465897
active_players = []

class Player:
    def __init__(self, _name, score = 0):
        global unique_id
        self.name = _name
        self.score = 0

        self.id = str(unique_id)
        unique_id -= 15465742

        self.group = None
        self.playing = False

    def __eq__(self, other): 
        return(self.name == other.name)

    def __repr__(self): return "Player:<user_id:{}>".format(self.id)

    def repr(self):
        return("Player object<name:{}, score:{}, playing:{}>".format(self.name, self.score, self.playing))

    def update(self, change=0):
        database.update_score(self.name, self.score, change)
        self.score += 1
        self.playing = False

    def guess(self, arg):
        arg = NUM[arg]

        if arg == self.group:
            self.update(1)
            return True
        else: return False

    def get_image(self):
        global images
        self.playing = True
        self.group = random.randint(0,1)
        return random.choice(images[self.group])['id']

def load_players():
    data = database.load_all()
    active_players = [generate_player(player_data) for player_data in data]
    return(active_players)

def generate_player(dict):
    player = {'user_id':dict['user_id'], 'object':Player( dict['user_id'], dict['score'])}
    return (player)

def query_player(name):
    global active_players
    name = name.replace('#','')
    for player in active_players:
        if player['user_id'] == name:
            return(player)
    else: 
        return False

@bot.event
async def on_ready():
    global images, active_players
    print('Logged in as: {}, with the client ID: {}...'.format(bot.user.name,bot.user.id))
    try:
        images = drive.load_images()
        print('Successfully loaded images...')
    except Exception as e:
        print("Loading images failed with error:<{}>! Terminating program.".format(e))
        exit()
    try:
        active_players = load_players()
        print("Successfully loaded player data...:")
    except Exception as e:
        print("Loading player data failed with error:<{}>! Terminating program.".format(e))
        exit()
    print('Press CTRL + C to stop execution of the bot.\n')
    return

@bot.command()
async def info(ctx):
    embed = discord.Embed(title="Trap Bot", description="Bot designed to play the D or no D game.", color=0xeee657)

    # give info about you here
    embed.add_field(name="Author", value="Blitzher")

    # Shows the number of servers the bot is member of.
    embed.add_field(name="Server count", value=f"{len(bot.guilds)}")

    # give users a link to invite thsi bot to their server
    embed.add_field(name="Invite", value="Invitation Link: https://goo.gl/LyYLr1")

    await ctx.send(embed=embed)

@bot.command(pass_context=True)
async def start(ctx):
    global active_players
    author = str(ctx.message.author)

    if not database.query(author):
        database.add_user(author)

        active_players = load_players()
        print("Welcome to the new player, {}!".format(author))

    player = query_player(author)['object']

    URL = drive.get_url(player.get_image())
    print("Sent image<Player:{}, image_group:{}>".format(player.name, player.group))
    await ctx.send("Can you tell if this individual has a d or not?")
    embed = discord.Embed()
    embed.set_image(url = URL)
    await ctx.send(embed=embed)

@bot.command()
async def guess(ctx, arg):
    author = str(ctx.message.author)

    try:
        player = query_player(author)['object']
    except:
        print("\nError finding player: {}.\n".format(author))
        return

    if player.guess(arg):
        await ctx.send("Nice, you got it!")
    else:
        await ctx.send("Congratulations, you're gay now.")

@bot.command()
async def stats(ctx):
    for line in database.load_all():
        await ctx.send(str(line))

def main():
    bot.run(TOKEN)

if __name__ == '__main__':
    main()
