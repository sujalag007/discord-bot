import discord
from discord.ext import commands
import datetime
import pytz

TOKEN = "MTM4MzQyMzk1NzgwMTIzODU3OQ.GS98ap.JaxnV5N1QOSf4O4uo53BmWFv4u8x7FGhzgHEXU"

TRACK_FILE = "submissions.txt"
PROGRESS_CHANNEL_ID = 1350373020757262408
tz = pytz.timezone('Asia/Kolkata')

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents) 


@bot.event
async def on_ready():
    print(f'✅ Bot is online as {bot.user}')
    await bot.change_presence(activity=discord.Game(name='Tracking progress')) 


@bot.event
async def on_message(message):
    """Save messages from a specific channel as submission, ignoring bot messages."""
    if message.author.bot:
        return
    
    if message.channel.id == PROGRESS_CHANNEL_ID:
        author_name = str(message.author)
        now_ist = datetime.datetime.now(tz)
        with open(TRACK_FILE, "a") as f:
            f.write(f"{author_name},{now_ist.isoformat()}\n")
        await message.channel.send(f"✅ {message.author.mention} submission recorded.")
    
    await bot.process_commands(message)


@bot.command()
async def report1day(ctx):
    """Who submitted in the last 24 hours."""
    now_ist = datetime.datetime.now(tz)
    cutoff = now_ist - datetime.timedelta(days=1)

    members_submitted = set()
    try:
        with open(TRACK_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(',', 1)
                if len(parts) < 2:
                    continue
                user, datetime_str = parts
                submission_dt = datetime.datetime.fromisoformat(datetime_str)
                submission_dt = submission_dt.astimezone(tz)

                if submission_dt >= cutoff:
                    members_submitted.add(user)
    except FileNotFoundError:
        members_submitted = set()

    if members_submitted:
        report = "🎉 **Members who submitted in the last 24 hours:**\n" + '\n'.join(members_submitted)
    else:
        report = "❕ No submissions in the last 24 hours."

    await ctx.send(report)


@bot.command()
async def inactive3days(ctx):
    """Who haven't submitted in the last 3 days."""
    now_ist = datetime.datetime.now(tz)
    cutoff = now_ist - datetime.timedelta(days=3)

    members_submitted = set()
    try:
        with open(TRACK_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(',', 1)
                if len(parts) < 2:
                    continue
                user, datetime_str = parts
                submission_dt = datetime.datetime.fromisoformat(datetime_str)
                submission_dt = submission_dt.astimezone(tz)

                if submission_dt >= cutoff:
                    members_submitted.add(user)
    except FileNotFoundError:
        members_submitted = set()

    all_members = set()
    for member in ctx.guild.members:
        if not member.bot:
            all_members.add(str(member))

    inactive_members = all_members - members_submitted

    if inactive_members:
        inactive_report = "❕ **Members inactive in the last 3 days:**\n" + '\n'.join(inactive_members)
    else:
        inactive_report = "🎉 Everyone has been active in the last 3 days!"

    await ctx.send(inactive_report)


bot.run(TOKEN)

