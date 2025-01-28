import discord
from discord import app_commands
from discord.ext import tasks
import json
import time
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
TOKEN = os.getenv('TOKEN')
GUILD_ID = int(os.getenv('GUILD_ID'))
PREMIUM_ROLE_ID = int(os.getenv('PREMIUM_ROLE_ID'))
LOG_CHANNEL_ID = int(os.getenv('LOG_CHANNEL_ID'))
TOS_CHANNEL_ID = int(os.getenv('TOS_CHANNEL_ID'))

# Initialize bot
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.reactions = True
bot = discord.Client(intents=intents)
tree = app_commands.CommandTree(bot)

# Data storage structure
DATA = {
    "users": {},
    "posts": {}
}

# File operations
def save_data():
    with open('data.json', 'w') as f:
        json.dump(DATA, f, indent=2)

def load_data():
    global DATA
    try:
        with open('data.json', 'r') as f:
            DATA = json.load(f)
    except FileNotFoundError:
        save_data()

def get_user_rep(user_id):
    user = DATA['users'].setdefault(str(user_id), {'ratings': [], 'rep': 0.0})
    if user['ratings']:
        user['rep'] = sum(user['ratings']) / len(user['ratings'])
    return user['rep']

def update_rep(user_id, rating):
    user = DATA['users'].setdefault(str(user_id), {'ratings': [], 'rep': 0.0})
    user['ratings'].append(rating)
    user['rep'] = sum(user['ratings']) / len(user['ratings'])
    save_data()

# Utility functions
def create_stars(score):
    full = int(score // 2)
    half = int(score % 2)
    return '★' * full + '½' * half + '☆' * (5 - full - half)

async def is_staff(interaction):
    return interaction.user.guild_permissions.manage_messages

# Bot events
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    check_expiries.start()

@bot.event
async def on_thread_create(thread):
    load_data()
    await thread.join()
    
    author = thread.owner
    premium = any(r.id == PREMIUM_ROLE_ID for r in author.roles)
    expiry_days = 30 if premium else 7
    expiry = int(time.time()) + expiry_days * 86400
    
    rep = get_user_rep(author.id)
    stars = create_stars(rep)
    
    embed = discord.Embed(
        title="Agree to Terms of Service",
        description=f"⭐ **Reputation**: {rep:.1f}/10 ({stars})\n"
                    f"✅ React to accept TOS and activate post\n"
                    f"❌ React to cancel (post will be deleted in 1 minute)",
        color=0x00ff00
    )
    
    tos_msg = await thread.send(embed=embed)
    await tos_msg.add_reaction('✅')
    await tos_msg.add_reaction('❌')
    
    DATA['posts'][str(thread.id)] = {
        'author': author.id,
        'expiry': expiry,
        'status': 'pending',
        'locked': False,
        'tos_msg': tos_msg.id
    }
    save_data()

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    
    load_data()
    post_id = reaction.message.channel.id
    post = DATA['posts'].get(str(post_id))
    
    if post and reaction.message.id == post['tos_msg']:
        if str(reaction.emoji) == '✅':
            # Check reputation
            rep = get_user_rep(post['author'])
            if rep < 3.0:
                await reaction.message.channel.edit(locked=True, reason="Low reputation")
                post['locked'] = True
                await log_action(f"🔒 Post locked - Low reputation (<3)\nPost: {reaction.message.channel.mention}")
            
            # Update post status
            post['status'] = 'active'
            save_data()
            
            # Schedule expiry warning
            warning_time = post['expiry'] - 86400
            await log_action(f"📝 New post activated\n{reaction.message.channel.mention} expires <t:{post['expiry']}:R>")
        
        elif str(reaction.emoji) == '❌':
            await reaction.message.channel.delete(reason="User cancelled TOS")
            del DATA['posts'][str(post_id)]
            save_data()

# Commands
@tree.command(name="report", description="Report a post", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(reason="Reason for reporting")
async def report_post(interaction, reason: str):
    if not isinstance(interaction.channel, discord.Thread):
        await interaction.response.send_message("❌ This command can only be used in forum posts!", ephemeral=True)
        return
    
    await log_action(
        f"🚩 Post reported\n"
        f"Post: {interaction.channel.mention}\n"
        f"Reason: {reason}\n"
        f"Reporter: {interaction.user.mention}"
    )
    await interaction.response.send_message("✅ Report submitted to moderators!", ephemeral=True)

@tree.command(name="remove", description="Delete your own post", guild=discord.Object(id=GUILD_ID))
async def remove_post(interaction):
    post = DATA['posts'].get(str(interaction.channel.id))
    if not post:
        await interaction.response.send_message("❌ No active post in this channel!", ephemeral=True)
        return
    
    if post['author'] != interaction.user.id:
        await interaction.response.send_message("❌ You can't delete someone else's post!", ephemeral=True)
        return
    
    await interaction.channel.delete(reason="User requested deletion")
    del DATA['posts'][str(interaction.channel.id)]
    save_data()

@tree.command(name="force_close", description="Mod: Close a post", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(reason="Reason for closing")
async def force_close(interaction, reason: str):
    if not await is_staff(interaction):
        await interaction.response.send_message("❌ Insufficient permissions!", ephemeral=True)
        return
    
    post = DATA['posts'].get(str(interaction.channel.id))
    if not post:
        await interaction.response.send_message("❌ No active post in this channel!", ephemeral=True)
        return
    
    await interaction.channel.edit(locked=True, archived=True, reason=reason)
    post['status'] = 'closed'
    save_data()
    await log_action(f"🔒 Post force-closed\n{interaction.channel.mention}\nReason: {reason}")
    await interaction.response.send_message("✅ Post closed successfully!", ephemeral=True)

@tree.command(name="rep", description="Check a user's reputation", guild=discord.Object(id=GUILD_ID))
async def check_rep(interaction, user: discord.User):
    rep = get_user_rep(user.id)
    stars = create_stars(rep)
    embed = discord.Embed(
        title=f"{user.display_name}'s Reputation",
        description=f"⭐ {rep:.1f}/10\n{stars}",
        color=0xffd700
    )
    await interaction.response.send_message(embed=embed)

@tree.command(name="rate", description="Rate a user", guild=discord.Object(id=GUILD_ID))
@app_commands.describe(user="User to rate", score="Rating (1-5)", reason="Reason for rating")
async def rate_user(interaction, user: discord.User, score: app_commands.Range[int, 1, 5], reason: str):
    post = DATA['posts'].get(str(interaction.channel.id))
    if not post or post['status'] != 'closed':
        await interaction.response.send_message("❌ You can only rate in closed posts!", ephemeral=True)
        return
    
    if user.id == interaction.user.id:
        await interaction.response.send_message("❌ You can't rate yourself!", ephemeral=True)
        return
    
    # Convert to 10-point scale
    converted_score = score * 2
    update_rep(user.id, converted_score)
    
    await log_action(
        f"⭐ New rating\n"
        f"User: {user.mention}\n"
        f"Score: {score}/5 ({converted_score}/10)\n"
        f"Reason: {reason}"
    )
    await interaction.response.send_message(f"✅ Successfully rated {user.display_name}!", ephemeral=True)

# Tasks
@tasks.loop(minutes=5)
async def check_expiries():
    load_data()
    now = time.time()
    
    for post_id, post in list(DATA['posts'].items()):
        if post['status'] == 'active' and post['expiry'] < now:
            channel = bot.get_channel(int(post_id))
            if channel:
                await channel.edit(locked=True, archived=True, reason="Post expired")
                post['status'] = 'closed'
                await log_action(f"⏰ Post expired\n{channel.mention}")
    
    save_data()

async def log_action(message):
    channel = bot.get_channel(LOG_CHANNEL_ID)
    if channel:
        await channel.send(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {message}")

# Run bot
if __name__ == '__main__':
    load_data()
    bot.run(TOKEN)
