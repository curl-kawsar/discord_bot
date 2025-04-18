import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging
import random
from keep_alive import keep_alive
import time
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)

# Bot uptime tracking
start_time = time.time()

# Load environment variables
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
if not TOKEN:
    # For Replit, check for token in environment
    TOKEN = os.environ.get('DISCORD_TOKEN')
    if not TOKEN:
        raise ValueError("No token found! Make sure you have set DISCORD_TOKEN in your environment variables")

# Bot setup with all intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# Server structure configuration with permissions
CATEGORIES_AND_CHANNELS = {
    "⚙️ SYSTEM": [
        ("『🤖』bot-commands", discord.ChannelType.text, {"staff_only": True}),
        ("『📱』bot-logs", discord.ChannelType.text, {"management_only": True})
    ],
    "🌐 NEXUS HUB": [
        ("『👋』welcome-portal", discord.ChannelType.text, {"public": True}),
        ("『📢』announcements", discord.ChannelType.text, {"staff_only": True}),
        ("『📜』guidelines", discord.ChannelType.text, {"public": True}),
        ("『💫』company-vision", discord.ChannelType.text, {"public": True})
    ],
    "⚡ OPERATIONS CENTER": [
        ("『💻』mission-control", discord.ChannelType.text, {"staff_only": True}),
        ("『🚀』active-projects", discord.ChannelType.text, {"staff_only": True}),
        ("『⏱』timeline-sync", discord.ChannelType.text, {"staff_only": True}),
        ("『📚』knowledge-base", discord.ChannelType.text, {"staff_only": True}),
        ("『📊』status-updates", discord.ChannelType.text, {"management_only": True})
    ],
    "🔮 INNOVATION LABS": [
        ("『🎨』design-nexus", discord.ChannelType.text, {"role_specific": "✨ Design Weaver"}),
        ("『⚙️』dev-sanctuary", discord.ChannelType.text, {"role_specific": "⚙️ Code Architect"}),
        ("『📣』marketing-hub", discord.ChannelType.text, {"role_specific": "📣 Marketing Sage"}),
        ("『💎』sales-matrix", discord.ChannelType.text, {"role_specific": "💎 Sales Virtuoso"})
    ],
    "🛸 PROJECT DIMENSION": [
        ("『📋』project-blueprint", discord.ChannelType.text, {"management_only": True}),
        ("『✨』task-forge", discord.ChannelType.text, {"staff_only": True}),
        ("『🛡』quality-nexus", discord.ChannelType.text, {"staff_only": True})
    ],
    "🎯 SYNC CHAMBERS": [
        ("『🌟』Team Sync", discord.ChannelType.voice, {"staff_only": True}),
        ("『💫』Client Portal", discord.ChannelType.voice, {"staff_only": True}),
        ("『🧠』Ideation Chamber", discord.ChannelType.voice, {"staff_only": True}),
        ("『💭』Neural Network", discord.ChannelType.voice, {"staff_only": True})
    ]
}

# Role hierarchy and permissions with futuristic names
ROLES = [
    {
        "name": "⚡ System Admin",
        "permissions": discord.Permissions(administrator=True),
        "color": discord.Color.from_rgb(255, 0, 89)  # Cyberpunk Pink
    },
    {
        "name": "🔮 Project Oracle",
        "permissions": discord.Permissions(
            manage_channels=True,
            manage_messages=True,
            mention_everyone=True,
            view_channel=True,
            send_messages=True,
            manage_roles=True
        ),
        "color": discord.Color.from_rgb(0, 255, 255)  # Cyan
    },
    {
        "name": "⚙️ Code Architect",
        "permissions": discord.Permissions(
            view_channel=True,
            send_messages=True,
            read_message_history=True,
            attach_files=True
        ),
        "color": discord.Color.from_rgb(0, 255, 136)  # Matrix Green
    },
    {
        "name": "✨ Design Weaver",
        "permissions": discord.Permissions(
            view_channel=True,
            send_messages=True,
            read_message_history=True,
            attach_files=True
        ),
        "color": discord.Color.from_rgb(147, 0, 255)  # Neon Purple
    },
    {
        "name": "📣 Marketing Sage",
        "permissions": discord.Permissions(
            view_channel=True,
            send_messages=True,
            read_message_history=True,
            attach_files=True
        ),
        "color": discord.Color.from_rgb(255, 128, 0)  # Neon Orange
    },
    {
        "name": "💎 Sales Virtuoso",
        "permissions": discord.Permissions(
            view_channel=True,
            send_messages=True,
            read_message_history=True,
            attach_files=True
        ),
        "color": discord.Color.from_rgb(255, 223, 0)  # Neon Gold
    },
    {
        "name": "🌟 Client Entity",
        "permissions": discord.Permissions(
            view_channel=True,
            send_messages=True,
            read_message_history=True
        ),
        "color": discord.Color.from_rgb(170, 170, 170)  # Silver
    }
]

# Welcome messages list
WELCOME_MESSAGES = [
    "🌟 Welcome to the future of digital innovation, {member}!",
    "💫 A new entity has joined our digital realm! Welcome, {member}!",
    "⚡ Greetings, {member}! Your digital journey begins now!",
    "🚀 Welcome aboard the innovation spaceship, {member}!",
    "🔮 A new creative force has emerged! Welcome, {member}!"
]

# Welcome embed colors
WELCOME_COLORS = [
    0xFF0059,  # Cyberpunk Pink
    0x00FFFF,  # Cyan
    0x00FF88,  # Matrix Green
    0x9300FF,  # Neon Purple
    0xFF8000   # Neon Orange
]

# Add this after WELCOME_COLORS definition
welcome_system_enabled = False
welcome_channel_readonly = False

@bot.event
async def on_ready():
    """Initialize bot and register all commands"""
    print(f'{bot.user} has connected to Discord!')
    print(f'Bot is in {len(bot.guilds)} servers')
    for guild in bot.guilds:
        print(f'- {guild.name} (id: {guild.id})')
    
    # Set custom status
    await bot.change_presence(
        activity=discord.Activity(
            type=discord.ActivityType.WATCHING,
            name="the digital realm 🌐"
        ),
        status=discord.Status.online
    )
    
    # Register all commands
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    print(f'Message received: {message.content} from {message.author} in {message.channel}')
    await bot.process_commands(message)

@bot.event
async def on_member_join(member):
    """Handles new member joins"""
    # Only process if welcome system is enabled
    if not welcome_system_enabled:
        return
        
    try:
        # Find the welcome channel
        welcome_channel = discord.utils.get(member.guild.channels, name="『👋』welcome-portal")
        if welcome_channel:
            # Create welcome embed
            welcome_embed = discord.Embed(
                title="🌐 NEW ENTITY DETECTED 🌐",
                description=random.choice(WELCOME_MESSAGES).format(member=member.mention),
                color=random.choice(WELCOME_COLORS)
            )
            
            # Add member info to embed
            welcome_embed.add_field(
                name="📊 Entity ID",
                value=f"#{len(member.guild.members)}",
                inline=True
            )
            welcome_embed.add_field(
                name="🕒 Access Granted",
                value=member.created_at.strftime("%Y-%m-%d"),
                inline=True
            )
            
            # Add server info
            welcome_embed.add_field(
                name="📚 Next Steps",
                value="• Check 『📜』guidelines for server rules\n"
                      "• Visit 『💫』company-vision to learn about us\n"
                      "• Await role assignment from management",
                inline=False
            )
            
            # Set thumbnail and footer
            welcome_embed.set_thumbnail(url=member.avatar.url if member.avatar else member.default_avatar.url)
            welcome_embed.set_footer(text=f"Welcome to {member.guild.name} | Powered by Orvix")
            
            # Send welcome message
            await welcome_channel.send(embed=welcome_embed)
            
            # Try to DM the user
            try:
                dm_embed = discord.Embed(
                    title="🌟 Welcome to the Digital Frontier! 🌟",
                    description=(
                        f"Greetings, {member.mention}! Welcome to **{member.guild.name}**!\n\n"
                        "🔹 Please read our guidelines carefully\n"
                        "🔹 Management will assign your role soon\n"
                        "🔹 Feel free to introduce yourself in the welcome channel\n\n"
                        "If you have any questions, feel free to ask in the appropriate channels!"
                    ),
                    color=0x00FFFF
                )
                await member.send(embed=dm_embed)
            except discord.Forbidden:
                print(f"Couldn't DM user {member.name}")
                
    except Exception as e:
        print(f"Error in welcome message: {str(e)}")

@bot.command(name='welcome_toggle')
@commands.has_permissions(administrator=True)
async def toggle_welcome(ctx):
    """Toggle the welcome message system on/off"""
    global welcome_system_enabled
    welcome_system_enabled = not welcome_system_enabled
    status = "enabled" if welcome_system_enabled else "disabled"
    
    embed = discord.Embed(
        title="🤖 Welcome System Status",
        description=f"Welcome system has been **{status}**!",
        color=0x00FF88 if welcome_system_enabled else 0xFF0059
    )
    embed.add_field(
        name="Current Status",
        value="✅ Active" if welcome_system_enabled else "❌ Inactive",
        inline=True
    )
    embed.add_field(
        name="Command Usage",
        value="Use `!welcome_test` to test the welcome message",
        inline=True
    )
    
    await ctx.send(embed=embed)

@bot.command(name='welcome_status')
@commands.has_permissions(administrator=True)
async def welcome_status(ctx):
    """Check the current status of the welcome system"""
    embed = discord.Embed(
        title="🤖 Welcome System Status",
        description="Current configuration of the welcome message system",
        color=0x00FF88 if welcome_system_enabled else 0xFF0059
    )
    
    embed.add_field(
        name="System Status",
        value="✅ Active" if welcome_system_enabled else "❌ Inactive",
        inline=True
    )
    
    embed.add_field(
        name="Welcome Channel",
        value="『👋』welcome-portal",
        inline=True
    )
    
    embed.add_field(
        name="Available Commands",
        value=(
            "`!welcome_toggle` - Enable/disable system\n"
            "`!welcome_test` - Test welcome message\n"
            "`!welcome_status` - View system status"
        ),
        inline=False
    )
    
    await ctx.send(embed=embed)

@bot.command(name='welcome_test')
@commands.has_permissions(administrator=True)
async def test_welcome(ctx, member: discord.Member = None):
    """Test the welcome message for a member"""
    if not welcome_system_enabled:
        await ctx.send("❌ Welcome system is currently disabled. Use `!welcome_toggle` to enable it first!")
        return
        
    member = member or ctx.author
    await on_member_join(member)
    await ctx.send("✅ Tested welcome message!")

@bot.command(name='welcome_mode')
@commands.has_permissions(administrator=True)
async def toggle_welcome_mode(ctx):
    """Toggle the welcome channel between read-only and write mode"""
    global welcome_channel_readonly
    welcome_channel_readonly = not welcome_channel_readonly
    
    try:
        # Find the welcome channel
        welcome_channel = discord.utils.get(ctx.guild.channels, name="『👋』welcome-portal")
        if welcome_channel:
            # Get the default role (@everyone)
            default_role = ctx.guild.default_role
            
            if welcome_channel_readonly:
                # Set to view-only mode
                await welcome_channel.set_permissions(default_role, 
                    view_channel=True,
                    send_messages=False,
                    add_reactions=False
                )
                status = "read-only"
                color = 0xFF0059  # Cyberpunk Pink
            else:
                # Set to normal mode
                await welcome_channel.set_permissions(default_role,
                    view_channel=True,
                    send_messages=True,
                    add_reactions=True
                )
                status = "write enabled"
                color = 0x00FF88  # Matrix Green
            
            # Create status embed
            embed = discord.Embed(
                title="🔒 Welcome Channel Mode",
                description=f"Welcome channel has been set to **{status}** mode!",
                color=color
            )
            
            embed.add_field(
                name="Current Status",
                value="🔒 View Only" if welcome_channel_readonly else "✏️ Write Enabled",
                inline=True
            )
            
            embed.add_field(
                name="Channel",
                value="『👋』welcome-portal",
                inline=True
            )
            
            embed.add_field(
                name="Permissions",
                value="• Can View: ✅\n• Can Send Messages: ❌" if welcome_channel_readonly 
                      else "• Can View: ✅\n• Can Send Messages: ✅",
                inline=False
            )
            
            await ctx.send(embed=embed)
        else:
            await ctx.send("❌ Welcome channel not found! Make sure the server is set up properly.")
            
    except Exception as e:
        print(f"Error toggling welcome mode: {str(e)}")
        await ctx.send(f"❌ An error occurred while changing welcome channel mode: {str(e)}")

@bot.command(name='welcome_help')
@commands.has_permissions(administrator=True)
async def welcome_help(ctx):
    """Show all welcome system commands"""
    embed = discord.Embed(
        title="🤖 Welcome System Commands",
        description="All available commands for the welcome system",
        color=0x00FFFF
    )
    
    embed.add_field(
        name="System Commands",
        value=(
            "`!welcome_toggle` - Enable/disable welcome messages\n"
            "`!welcome_test` - Test welcome message\n"
            "`!welcome_status` - View system status\n"
            "`!welcome_mode` - Toggle view-only mode\n"
            "`!welcome_help` - Show this help message"
        ),
        inline=False
    )
    
    embed.add_field(
        name="Current Settings",
        value=(
            f"Welcome System: {'✅ Active' if welcome_system_enabled else '❌ Inactive'}\n"
            f"Welcome Channel Mode: {'🔒 View Only' if welcome_channel_readonly else '✏️ Write Enabled'}"
        ),
        inline=False
    )
    
    await ctx.send(embed=embed)

async def setup_channel_permissions(channel, guild, permission_type, role_name=None):
    """Setup permissions for a channel based on its type"""
    # Default permissions - hide from everyone
    everyone_perms = discord.PermissionOverwrite(view_channel=False)
    await channel.set_permissions(guild.default_role, overwrite=everyone_perms)
    
    # Get role objects
    admin_role = discord.utils.get(guild.roles, name="⚡ System Admin")
    manager_role = discord.utils.get(guild.roles, name="🔮 Project Oracle")
    
    # Always give access to Admin
    if admin_role:
        await channel.set_permissions(admin_role, overwrite=discord.PermissionOverwrite(view_channel=True, send_messages=True))
    
    if permission_type.get("public"):
        # Public channels are visible to everyone
        await channel.set_permissions(guild.default_role, overwrite=discord.PermissionOverwrite(view_channel=True, send_messages=True))
    
    elif permission_type.get("staff_only"):
        # Staff channels are visible to all staff roles
        for role_info in ROLES[:-1]:  # Exclude Client role
            role = discord.utils.get(guild.roles, name=role_info["name"])
            if role:
                await channel.set_permissions(role, overwrite=discord.PermissionOverwrite(view_channel=True, send_messages=True))
    
    elif permission_type.get("management_only"):
        # Management channels are only visible to Admin and Manager roles
        if manager_role:
            await channel.set_permissions(manager_role, overwrite=discord.PermissionOverwrite(view_channel=True, send_messages=True))
    
    elif permission_type.get("role_specific"):
        # Role-specific channels are only visible to that role and management
        specific_role = discord.utils.get(guild.roles, name=role_name)
        if specific_role:
            await channel.set_permissions(specific_role, overwrite=discord.PermissionOverwrite(view_channel=True, send_messages=True))
        if manager_role:
            await channel.set_permissions(manager_role, overwrite=discord.PermissionOverwrite(view_channel=True, send_messages=True))

@bot.command(name='setup')
@commands.has_permissions(administrator=True)
async def setup_server(ctx):
    """Sets up the entire server structure"""
    try:
        print(f"Setup command received from {ctx.author} in {ctx.guild.name}")
        guild = ctx.guild
        
        # Send initial message
        await ctx.send("Starting server setup... 🚀")
        
        # Create roles
        print("Creating roles...")
        existing_roles = [role.name for role in guild.roles]
        for role_info in ROLES:
            if role_info["name"] not in existing_roles:
                await guild.create_role(
                    name=role_info["name"],
                    permissions=role_info["permissions"],
                    color=role_info["color"]
                )
                print(f"Created role: {role_info['name']}")
                await ctx.send(f"✅ Created role: {role_info['name']}")

        # Create categories and channels
        print("Creating categories and channels...")
        for category_name, channels in CATEGORIES_AND_CHANNELS.items():
            # Create category
            category = await guild.create_category_channel(name=category_name)
            print(f"Created category: {category_name}")
            await ctx.send(f"📁 Created category: {category_name}")
            
            # Create channels in category
            for channel_info in channels:
                channel_name, channel_type, permissions = channel_info
                if channel_type == discord.ChannelType.text:
                    channel = await category.create_text_channel(name=channel_name)
                else:
                    channel = await category.create_voice_channel(name=channel_name)
                
                # Setup permissions for the channel
                await setup_channel_permissions(
                    channel, 
                    guild, 
                    permissions,
                    role_name=permissions.get("role_specific")
                )
                
                print(f"Created channel: {channel_name}")
                await ctx.send(f"➕ Created channel: {channel_name}")

        await ctx.send("✨ Server setup completed successfully! 🎉")
        
    except Exception as e:
        print(f"Error during setup: {str(e)}")
        await ctx.send(f"❌ An error occurred during setup: {str(e)}")

@bot.command(name='clean')
@commands.has_permissions(administrator=True)
async def clean_server(ctx):
    """Removes all channels and categories (use with caution!)"""
    try:
        guild = ctx.guild
        await ctx.send("🚨 Starting server cleanup...")
        
        for channel in guild.channels:
            await channel.delete()
            print(f"Deleted channel: {channel.name}")
            
        await ctx.send("🧹 Server cleaned! You can now run !setup to create the structure again.")
    except Exception as e:
        print(f"Error during cleanup: {str(e)}")
        await ctx.send(f"❌ An error occurred during cleanup: {str(e)}")

@setup_server.error
@clean_server.error
async def command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("❌ You need administrator permissions to use this command!")
    else:
        print(f"Command error: {str(error)}")
        await ctx.send(f"❌ An error occurred: {str(error)}")

@bot.command(name='status')
@commands.has_permissions(administrator=True)
async def check_status(ctx):
    """Check bot status and performance"""
    # Calculate uptime
    uptime = time.time() - start_time
    days = int(uptime // (24 * 3600))
    hours = int((uptime % (24 * 3600)) // 3600)
    minutes = int((uptime % 3600) // 60)
    
    embed = discord.Embed(
        title="🤖 Bot Status",
        description="Current system status and performance metrics",
        color=0x00FF88
    )
    
    # Add uptime
    embed.add_field(
        name="⏰ Uptime",
        value=f"{days}d {hours}h {minutes}m",
        inline=True
    )
    
    # Add server count
    embed.add_field(
        name="🌐 Servers",
        value=f"Active in {len(bot.guilds)} servers",
        inline=True
    )
    
    # Add latency
    embed.add_field(
        name="📡 Latency",
        value=f"{round(bot.latency * 1000)}ms",
        inline=True
    )
    
    # Add system info
    embed.add_field(
        name="💻 System",
        value="Hosted on Replit",
        inline=True
    )
    
    # Add last restart
    embed.add_field(
        name="🔄 Last Restart",
        value=datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S UTC'),
        inline=True
    )
    
    await ctx.send(embed=embed)

# Add this before bot.run(TOKEN)
keep_alive()  # Start the web server
try:
    bot.run(TOKEN)
except discord.errors.HTTPException as e:
    print(f"Rate limit error: {e}")
    os.system('kill 1')  # Restart the bot if rate limited 