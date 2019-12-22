import discord
import dateutil
from discord.ext import commands
from discord import CategoryChannel, Client, Colour, Embed, Guild, Member, Role, TextChannel, User, VoiceChannel, utils
from discord.ext.commands import Bot, BucketType, Cog, Context, command, group
import typing
import colorsys
from paginator import PaginatorSession

class Info(commands.Cog):
    """Info"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="guildinfo", aliases=['gi', 'serverinfo'])
    async def guildinfo(self, ctx: Context, *, guild_id: int = None) -> None:
        """Returns info about a guild"""
        if guild_id is not None and await self.bot.is_owner(ctx.author):
            guild = self.bot.get_guild(guild_id)
            if guild is None:
                return await ctx.send(f'Invalid Guild ID given.')
        else:
            guild = ctx.guild
        
        created = guild.created_at
        features = ", ".join(guild.features)
        
        id = guild.id
        owner = guild.owner
        ownerdn = guild.owner.display_name
        
        boostlvl = guild.premium_tier
        boostlen = guild.premium_subscription_count
       
        #lists of server elements
        rolelist = guild.roles
        cats = guild.categories
        chans = guild.text_channels
        
        #Dictionary of flags
        regionFlag = {
            'amsterdam': ":flag_nl: - Amsterdam",
            'brazil': ":flag_br: -  Brazil",
            'eu_central': ":flag_eu: - Central Europe",
            'eu-central': "",
            'eu_west': ":flag_eu: - West Europe",
            'eu-west': "",
            'europe': ":flag_eu: - Europe",
            'frankfurt': ":flag_de: - Frankfurt",
            'hongkong': ":flag_ch: - Hong Kong",
            'india': ":flag_in: - India",
            'japan': ":flag_jap: - Japan",
            'london': ":flag_uk: - London",
            'russia': ":flag_ru: - Russia",
            'singapore': ":flag_au: - Singapore",
            'southafrica': ":flag_za: - South Africa",
            'sydney': ":flag_au: - Sydney",
            'us_central': ":flag_us: - US Central",
            'us-central': "",
            'us_east': ":flag_us: - US East",
            'us-east': "",
            'us_south': ":flag_us: - US South",
            'us-south': "",
            'us_west': ":flag_us: - US West",
            'us-west': ""
        }

        region = guild.region
        
        
        # How many of each type of channel?
        roles = len(guild.roles)
        channels = guild.channels
        text_channels = 0
        category_channels = 0
        voice_channels = 0
        for channel in channels:
            if type(channel) == TextChannel:
                text_channels += 1
            elif type(channel) == CategoryChannel:
                category_channels += 1
            elif type(channel) == VoiceChannel:
                voice_channels += 1
       
        # How many of each client type status?
        member_count = guild.member_count
        members = guild.members
        available = 0
        online = 0
        dnd = 0
        idle = 0
        offline = 0
        mobile = 0
        web = 0
        desktop = 0
        mobileonline = 0
        webonline = 0
        desktoponline = 0
        mobileidle = 0
        webidle = 0
        desktopidle = 0
        mobilednd = 0
        webdnd = 0
        desktopdnd = 0
        
        for member in members:
            if str(member.status) == "online" or str(member.status) == "idle" or str(member.status) == "dnd":
                available += 1
            if str(member.status) == "online":
                online += 1
            elif str(member.status) == "offline":
                offline += 1
            elif str(member.status) == "idle":
                idle += 1
            elif str(member.status) == "dnd":
                dnd += 1
        
        for member in members:
            if str(member.mobile_status) == "online" or str(member.mobile_status) == "dnd" or str(member.mobile_status) == "idle":
               mobile += 1
            if str(member.web_status) == "online" or str(member.web_status) == "dnd" or str(member.web_status) == "idle":
               web += 1
            if str(member.desktop_status) == "online" or str(member.desktop_status) == "dnd" or str(member.desktop_status) == "idle":
               desktop += 1
            if str(member.mobile_status) == "online":
                mobileonline += 1
            if str(member.web_status) == "online":
                webonline += 1
            if str(member.desktop_status) == "online":
                desktoponline += 1
            if str(member.mobile_status) == "dnd":
                mobilednd += 1
            if str(member.web_status) == "dnd":
                webdnd += 1
            if str(member.desktop_status) == "dnd":
                desktopdnd += 1
            if str(member.mobile_status) == "idle":
                mobileidle += 1
            if str(member.web_status) == "idle":
                webidle += 1
            if str(member.desktop_status) == "idle":
                desktopidle += 1

        embed = discord.Embed(title=str(guild.name) + "'s information", colour=Colour.blurple())
        embed.add_field(name=":id:", value=id)
        embed.add_field(name=":date: Guild Created On", value=created.strftime("%A %d %B %Y %H:%M"))
        embed.add_field(name=":bust_in_silhouette: Owner", value=str(owner) + " aka " + str(ownerdn))
        embed.add_field(name=":telephone_receiver:  Voice Region", value=" ".join([regionFlag[n] for n in region]))
        #embed.add_field(name=":telephone_receiver:  Voice Region", value=region)
        embed.add_field(name="Nitro Level", value=str(boostlvl) + "/" + str(3))
        embed.add_field(name="# of current boosts", value=str(boostlen) + "/" + str(30))
        if boostlen > 2:
            embed.add_field(name=".. needed for lvl 1", value="Already unlocked")
        else:
            embed.add_field(name=".. needed for lvl 1", value=str(2 - boostlen))
        if boostlen > 15:
            embed.add_field(name=".. needed for lvl 2", value="Already unlocked")
        else:    
            embed.add_field(name=".. needed for lvl 2", value=str(15 - boostlen))
        if boostlen > 30:
            embed.add_field(name=".. needed for lvl 3", value="Already unlocked")
        else:
            embed.add_field(name=".. needed for lvl 3", value=str(30 - boostlen))
        embed.add_field(name=":busts_in_silhouette: # of Members", value=member_count)
        embed.add_field(name="... of which human", value=len([member for member in guild.members if not member.bot]))
        embed.add_field(name="... of which bots", value=len([member for member in guild.members if member.bot]))
        embed.add_field(name="... of Roles", value=roles)
        embed.add_field(name="... of Text Channels", value=text_channels)
        embed.add_field(name="... of Voice Channels", value=voice_channels)
        embed.add_field(name="... of Categories", value=category_channels)
        embed.add_field(name="Members available (Total)", value=available)
        embed.add_field(name=":green_circle: Members Online", value=online)
        embed.add_field(name=":orange_circle: Members Idle", value=idle)
        embed.add_field(name=":red_circle: Members Busy", value=dnd)
        embed.add_field(name=":black_circle: Members Offline/Invisible", value=offline)
        embed.add_field(name=":computer: Members using the Desktop App", value=str(desktop) + " total\n" + str(desktoponline) + " online\n" + str(desktopidle) + " idle\n" + str(desktopdnd) + " busy")
        embed.add_field(name="Members using the Browser App", value=str(web) + " total\n" + str(webonline) + " online\n" + str(webidle) + " idle\n" + str(webdnd) + " busy")
        embed.add_field(name=":iphone: Members using the Mobile App", value=str(mobile) + " total\n" + str(mobileonline) + " online\n" + str(mobileidle) + " idle\n" + str(mobilednd) + " busy")
        embed.set_thumbnail(url=guild.icon_url)
        
        if boostlen > 30:
            embed.set_footer(text="Max Level reached", icon_url="")
        else:
            embed.set_footer(text=str(30 - boostlen) + " boosts to go for max boost level", icon_url="")
                   
        await ctx.send(embed=embed)
        
    @commands.command(name="textchannelinfo", aliases=['tci'])
    async def text_channel_info(self, ctx: Context, channel_id: int = None) -> None:
        """Returns info about a channel."""   
        if channel_id is not None and await self.bot.is_owner(ctx.author):
            channel = self.bot.get_channel(channel_id)
            if channel is None:
                return await ctx.send(f'Invalid Channel ID given.')
        else:
            channel = ctx.channel
         
        name = channel.name
        created = channel.created_at
        id = channel.id
        catid = channel.category_id
        cat = channel.category
        topic = channel.topic
        pos = channel.position
        type = channel.type
        nsfw = channel.is_nsfw()
        croles = channel.changed_roles
    
        embed = discord.Embed(title=channel.name + "'s Information" ,colour=Colour.blurple())
        embed.add_field(name="Created", value=created)
        embed.add_field(name="Name", value=name)
        embed.add_field(name="ID", value=id)
        embed.add_field(name="Category ID", value=catid)
        embed.add_field(name="Category", value=cat)
        embed.add_field(name="Topic", value=topic)
        embed.add_field(name="Position", value=pos)
        embed.add_field(name="Channel Type", value=type)
        embed.add_field(name="is NSFW?", value=nsfw)
        embed.add_field(name="Changed Roles", value=croles) 
                
        await ctx.send(embed=embed)
        
    @commands.command(name="voicechannelinfo", aliases=['vci'])
    async def voice_channel_info(self, ctx: Context, channel_id: int = None) -> None:
        """Returns info about a channel."""   
        if channel_id is not None:
            channel = self.bot.get_channel(channel_id)
            if channel is None:
                return await ctx.send(f'Invalid Channel ID given.')
        else:
            channel = ctx.channel
        
        name = channel.name
        created = channel.created_at
        id = channel.id
        catid = channel.category_id
        cat = channel.category
        pos = channel.position
        type = channel.type
        croles = channel.changed_roles
        ulimit = channel.user_limit
        bitrate = channel.bitrate
    
        embed = discord.Embed(title=channel.name + "'s Information" ,colour=Colour.blurple())
        embed.add_field(name="Created", value=created)
        embed.add_field(name="Name", value=name)
        embed.add_field(name="ID", value=id)
        embed.add_field(name="Category ID", value=catid)
        embed.add_field(name="Category", value=cat)
        embed.add_field(name="Position", value=pos)
        embed.add_field(name="User Limit", value=ulimit)
        embed.add_field(name="Bitrate", value=bitrate)
        embed.add_field(name="Channel Type", value=type)
        embed.add_field(name="Changed Roles", value=croles) 
        
        await ctx.send(embed=embed)
    
    @commands.command(name="userinfo", aliases=['ui', 'clientinfo'])
    async def user_info(self, ctx: Context, *, user_id: int = None) -> None:
        """Returns info about a user."""
        if user_id is not None and await self.bot.is_owner(ctx.author):
            user = self.bot.get_user(user_id)
            if user is None:
                return await ctx.send(f'Invalid User ID given.')
        else:
            user = user
        
        created = user.created_at
        name = user.name
        avatar = user.avatar_url
        id = user.id
        discrim = user.discriminator
        bot = user.bot
        
        embed = discord.Embed(title=str(user.name) + "'s information", colour=Colour.blurple())
        embed.add_field(name="Account made on", value=created.strftime("%A %d %B %Y %H:%M"))
        embed.add_field(name="Username", value=name)
        embed.add_field(name="Users Discriminator", value=discrim)
        embed.add_field(name="Users ID", value=id)
        embed.add_field(name="Tag", value=str(name) + "#" + str(discrim))
        embed.add_field(name="Bot?", value=bot)
        embed.set_thumbnail(url=user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(name="botinfo", aliases=['bi', 'info'])
    async def botinfo(self, ctx: Context) -> None:
        """Returns info about the bot."""
        
        created = ctx.me.created_at
        name = ctx.me.name
        avatar = ctx.me.avatar_url
        id = ctx.me.id
        discrim = ctx.me.discriminator
        guildcount = len(self.bot.guilds)
        latency = self.bot.latency
        
        embed = discord.Embed(title="Bots Information", colour=Colour.blurple())
        embed.add_field(name="Bots Name", value=name)        
        embed.add_field(name="Bots Discriminator", value=discrim)
        embed.add_field(name="Bots ID", value=id)
        embed.add_field(name="Number of guilds bot is in", value=guildcount)
        embed.add_field(name="Bot created on", value=created.strftime("%A %d %B %Y %H:%M"))
        embed.add_field(name="Latency", value=latency)
        
        embed.set_thumbnail(url=ctx.me.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(name="memberinfo", aliases=['mi'])
    async def member_info(self, ctx: Context, guild_id: int = None, *, user_id: int = None) -> None:
        """Returns info about a member."""
        if user_id is not None and await self.bot.is_owner(ctx.author):
            user = self.bot.get_guild(guild_id).get_member(user_id)
            if user is None:
                return await ctx.send(f'Invalid User ID given.')
        else:
            user = user
                   
        roles = ""
        activities = ""
        joined = user.joined_at
        name = user.name
        gstatus = user.status
        wstatus = user.web_status
        dstatus = user.desktop_status
        mstatus = user.mobile_status
        bot = user.bot
        nick = user.nick
        boostsince = user.premium_since
        pc = user.is_on_pc()
        web = user.is_on_web()
        mobile = user.is_on_mobile()
        top = user.top_role
        
        #List of users roles
        for i in range(len(user.roles)):
            roles += str(user.roles[i].mention) + ", "
                
        embed = discord.Embed(title=str(user.display_name) + "'s Information", colour=Colour.blurple())
        embed.add_field(name="Member joined on", value=joined.strftime("%A %d %B %Y %H:%M"))
        embed.add_field(name="Members Nickname", value=nick)
        if boostsince == None:
            embed.add_field(name="Boosted server since", value="Never boosted")
        else:
            embed.add_field(name="Boosted server since", value=boostsince.strftime("%A %d %B %Y %H:%M"))
        embed.add_field(name=":robot: Bot?", value=bot)
        embed.add_field(name="On PC?", value=pc)
        embed.add_field(name="On Web?", value=web)
        embed.add_field(name=":iphone: On Mobile?", value=mobile)
        embed.add_field(name=":computer: Desktop App", value=dstatus)
        embed.add_field(name="Web/Browser App", value=wstatus)
        embed.add_field(name=":iphone: Android/iOS App", value=mstatus)
        embed.add_field(name="Roles Member is in", value=roles)
        embed.add_field(name="Highest role of Member", value=top)
        embed.set_thumbnail(url=user.avatar_url)

        await ctx.send(embed=embed)
        
    @commands.command(name="avatar")
    async def avatar(self, ctx: Context, *, user: discord.Member) -> None:
        if user is not None and await self.bot.is_owner(ctx.author):
            user = self.bot.get_user(user)
            if user is None:
                return await ctx.send(f'Invalid User ID given.')
        else:
            user = user
        
        """Returns a users avatar"""
        
        avatar = user.avatar_url
        
        await ctx.send(avatar)
        
    @commands.command(name="roleperms")
    async def role_perm_info(self, ctx: Context, *, role: discord.Role) -> None:
        """Returns info about a members permissions"""
        
        admin = role.permissions.administrator
        
        embed = Embed(
            colour=Colour.blurple(),
            description=f"""
                **Permission information for {role.name}**
                Administrator?: {admin}*
                
                _**Notes:**_
                * This perm overrides all below it making everything else automatically true
            """
        )
        
        await ctx.send(embed=embed)

    @commands.command(name="perms")
    async def perm_info(self, ctx: Context, *, user: Member) -> None:
        """Returns info about a members permissions"""
        
        perms = ""
        if user.guild_permissions.administrator:
            perms += "Administrator, "
        if user.guild_permissions.create_instant_invite:
            perms += "Create Instant Invite, "
        if user.guild_permissions.kick_members:
            perms += "Kick Members, "
        if user.guild_permissions.ban_members:
            perms += "Ban Members, "
        if user.guild_permissions.manage_channels:
            perms += "Manage Channels, "
        if user.guild_permissions.manage_guild:
            perms += "Manage Guild, "
        if user.guild_permissions.add_reactions:
            perms += "Add Reactions, "
        if user.guild_permissions.view_audit_log:
            perms += "View Audit Log, "
        if user.guild_permissions.read_messages:
            perms += "Read Messages, "
        if user.guild_permissions.send_messages:
            perms += "Send Messages, "
        if user.guild_permissions.send_tts_messages:
            perms += "Send TTS Messages, "
        if user.guild_permissions.manage_messages:
            perms += "Manage Messages, "
        if user.guild_permissions.embed_links:
            perms += "Embed Links, "
        if user.guild_permissions.attach_files:
            perms += "Attach Files, "
        if user.guild_permissions.read_message_history:
            perms += "Read Message History, "
        if user.guild_permissions.mention_everyone:
            perms += "Mention Everyone, "
        if user.guild_permissions.external_emojis:
            perms += "Use External Emojis, "
        if user.guild_permissions.connect:
            perms += "Connect to Voice, "
        if user.guild_permissions.speak:
            perms += "Speak, "
        if user.guild_permissions.mute_members:
            perms += "Mute Members, "
        if user.guild_permissions.deafen_members:
            perms += "Deafen Members, "
        if user.guild_permissions.move_members:
            perms += "Move Members, "
        if user.guild_permissions.use_voice_activation:
            perms += "Use Voice Activation, "
        if user.guild_permissions.change_nickname:
            perms += "Change Nickname, "
        if user.guild_permissions.manage_nicknames:
            perms += "Manage Nicknames, "
        if user.guild_permissions.manage_roles:
            perms += "Manage Roles, "
        if user.guild_permissions.manage_webhooks:
            perms += "Manage Webhooks, "
        if user.guild_permissions.manage_emojis:
            perms += "Manage Emojis, "

        if perms is None:
            perms = "None"
        else:
            perms = perms.strip(", ")
        
        embed = discord.Embed(title="Permissions for "+user.nick)
        embed.add_field(name="Permissions", value=perms)

        embed.set_thumbnail(url=user.avatar_url)

        await ctx.send(embed=embed)
    
    @commands.command(name="roles")
    async def roles_info(self, ctx: Context, *, guild_id: int = None) -> None:
        """Returns a list of all roles and their corresponding IDs."""
        if guild_id is not None and await self.bot.is_owner(ctx.author):
            guild = self.bot.get_guild(guild_id)
            if guild is None:
                return await ctx.send(f'Invalid Guild ID given.')
        else:
            guild = ctx.guild
            
        # Sort the roles by the order as shown in the client's Roles UI
        roles = sorted(guild.roles, key=lambda role: role.position, reverse=True)
        #roles = [role for role in roles if role.name != "@everyone"]        

        # Build a string
        role_string = ""
        for role in roles:
            role_string += f"{role.position} - {role.mention}\n"
       
        embed = discord.Embed(title="Roles", colour=Colour.blurple(), description=f"""{role_string}""")
        
       
        await ctx.send(embed=embed)        

    @commands.command(name="joinlist")
    async def join_list(self, ctx, *, guild_id: int = None) -> None:
        """Retrieve List of Member by join date"""
        if guild_id is not None and await self.bot.is_owner(ctx.author):
            guild = self.bot.get_guild(guild_id)
            if guild is None:
                return await ctx.send(f'Invalid Guild ID given.')
        else:
            guild = ctx.guild
        
        users = sorted(guild.members, key=lambda member: member.joined_at, reverse=False)
                
        user_string = ""
        for user in users:
            joined = user.joined_at
            user_string += f"""{user.display_name} - {user.top_role} - {joined.strftime("%A %d %B %Y %H:%M")}\n"""
        
        f = open("export/joins.txt", "w")
        f.write(user_string)
        f.close()     
        
        file = discord.File("export/joins.txt")
        
        await ctx.send(str("Dumped data to file"), files=[file])
      
    @commands.command(name="botjoinlist")
    async def botjoin_list(self, ctx, *, guild_id: int = None) -> None:
        """Retrieve List of Bots by join date"""
        if guild_id is not None and await self.bot.is_owner(ctx.author):
            guild = self.bot.get_guild(guild_id)
            if guild is None:
                return await ctx.send(f'Invalid Guild ID given.')
        else:
            guild = ctx.guild
        
        users = sorted(guild.members, key=lambda member: member.joined_at, reverse=False)
        users = [user for user in users if user.bot]       
        
        user_string = ""
        for user in users:
            joined = user.joined_at
            user_string += f"""{user.display_name} - {user.top_role} - {joined.strftime("%A %d %B %Y %H:%M")}\n"""
        
        f = open("export/botjoins.txt", "w")
        f.write(user_string)
        f.close()     
        
        file = discord.File("export/botjoins.txt")
        
        await ctx.send(str("Dumped data to file"), files=[file])
       
    @commands.command(name="nopclist")
    async def nd_status_list(self, ctx, *, guild_id: int = None) -> None:
        """Retrieve list of Members not on the Desktop App"""
        if guild_id is not None and await self.bot.is_owner(ctx.author):
            guild = self.bot.get_guild(guild_id)
            if guild is None:
                return await ctx.send(f'Invalid Guild ID given.')
        else:
            guild = ctx.guild
        
        users = sorted(guild.members, key=lambda member: member.joined_at, reverse=False)
        users = [user for user in users if not user.is_on_pc()]

        user_string = ""
        for user in users:
            user_string += f"""{user.name} - {user.display_name}\n"""

        f = open("export/nopclist.txt", "w")
        f.write("Users not on PC\n\n"+user_string)
        f.close()

        file = discord.File("export/nopclist.txt")

        await ctx.send(str("Dumped Data to file"), files=[file])
        
    @commands.command(name="pclist")
    async def d_status_list(self, ctx, *, guild_id: int = None) -> None:
        """Retrieve list of Members on the Desktop App"""
        if guild_id is not None and await self.bot.is_owner(ctx.author):
            guild = self.bot.get_guild(guild_id)
            if guild is None:
                return await ctx.send(f'Invalid Guild ID given.')
        else:
            guild = ctx.guild
        
        users = sorted(guild.members, key=lambda member: member.joined_at, reverse=False)
        users = [user for user in users if user.is_on_pc()]

        user_string = ""
        for user in users:
            user_string += f"""{user.name} - {user.display_name}\n"""

        f = open("export/pclist.txt", "w")
        f.write("Users on PC\n\n"+user_string)
        f.close()

        file = discord.File("export/pclist.txt")

        await ctx.send(str("Dumped Data to file"), files=[file])
    
    @commands.command(name="nonmobilelist") 
    async def nm_status_list(self, ctx, *, guild_id: int = None) -> None:
        """Retrieve list of Members not on the iOS/Android App"""
        if guild_id is not None and await self.bot.is_owner(ctx.author):
            guild = self.bot.get_guild(guild_id)
            if guild is None:
                return await ctx.send(f'Invalid Guild ID given.')
        else:
            guild = ctx.guild
        
        users = sorted(guild.members, key=lambda member: member.joined_at, reverse=False)
        users = [user for user in users if not user.is_on_mobile()]

        user_string = ""
        for user in users:
            user_string += f"""{user.name} - {user.display_name}\n"""

        f = open("export/nomobilelist.txt", "w")
        f.write("Users not on iOS/Android\n\n"+user_string)
        f.close()

        file = discord.File("export/nomobilelist.txt")

        await ctx.send(str("Dumped Data to file"), files=[file])   
    
    @commands.command(name="mobilelist") 
    async def m_status_list(self, ctx, *, guild_id: int = None) -> None:
        """Retrieve list of Members on the iOS/Android App"""
        if guild_id is not None and await self.bot.is_owner(ctx.author):
            guild = self.bot.get_guild(guild_id)
            if guild is None:
                return await ctx.send(f'Invalid Guild ID given.')
        else:
            guild = ctx.guild
        
        users = sorted(guild.members, key=lambda member: member.joined_at, reverse=False)
        users = [user for user in users if user.is_on_mobile()]

        user_string = ""
        for user in users:
            user_string += f"""{user.name} - {user.display_name}\n"""

        f = open("export/mobilelist.txt", "w")
        f.write("Users on iOS/Android\n\n"+user_string)
        f.close()

        file = discord.File("export/mobilelist.txt")

        await ctx.send(str("Dumped Data to file"), files=[file])

    @commands.command(name="nonweblist")
    async def nw_status_list(self, ctx, *, guild_id: int = None) -> None:
        """Retrieve list of Members not on Discord Browser App or isn't a bot"""
        if guild_id is not None and await self.bot.is_owner(ctx.author):
            guild = self.bot.get_guild(guild_id)
            if guild is None:
                return await ctx.send(f'Invalid Guild ID given.')
        else:
            guild = ctx.guild
        
        users = sorted(guild.members, key=lambda member: member.joined_at, reverse=False)
        users = [user for user in users if not user.is_on_web()]

        user_string = ""
        for user in users:
            user_string += f"""{user.name} - {user.display_name}\n"""

        f = open("export/noweblist.txt", "w")
        f.write("Users not on web-browser/not bots\n\n"+user_string)
        f.close()

        file = discord.File("export/noweblist.txt")

        await ctx.send(str("Dumped Data to file"), files=[file])

    @commands.command(name="weblist")
    async def w_status_list(self, ctx, *, guild_id: int = None) -> None:
        """Retrieve list of Members on Discord Browser App or is a bot"""
        if guild_id is not None and await self.bot.is_owner(ctx.author):
            guild = self.bot.get_guild(guild_id)
            if guild is None:
                return await ctx.send(f'Invalid Guild ID given.')
        else:
            guild = ctx.guild
        
        users = sorted(guild.members, key=lambda member: member.joined_at, reverse=False)
        users = [user for user in users if user.is_on_web()]

        user_string = ""
        for user in users:
            user_string += f"""{user.name} - {user.display_name}\n"""

        f = open("export/weblist.txt", "w")
        f.write("Users on web-browser/bots\n\n"+user_string)
        f.close()

        file = discord.File("export/weblist.txt")

        await ctx.send(str("Dumped Data to file"), files=[file])

    @commands.command(name="userjoinlist")
    async def humanjoin_list(self, ctx, *, guild_id: int = None) -> None:
        """Retrieve List of Users by join date"""
        if guild_id is not None and await self.bot.is_owner(ctx.author):
            guild = self.bot.get_guild(guild_id)
            if guild is None:
                return await ctx.send(f'Invalid Guild ID given.')
        else:
            guild = ctx.guild
        
        users = sorted(guild.members, key=lambda member: member.joined_at, reverse=False)
        users = [user for user in users if not user.bot]       
                
        user_string = ""
        for user in users:
            joined = user.joined_at
            user_string += f"""{user.display_name} - {user.top_role} - {joined.strftime("%A %d %B %Y %H:%M")}\n"""
        
        f = open("export/userjoins.txt", "w")
        f.write(user_string)
        f.close()     
        
        file = discord.File("export/userjoins.txt")
        
        await ctx.send(str("Dumped data to file"), files=[file])
          
        
    @commands.command(name="channellist")
    async def channel_list(self, ctx: Context, *, guild_id: int = None) -> None:
        """Retrieve List of channels"""
        if guild_id is not None and await self.bot.is_owner(ctx.author):
            guild = self.bot.get_guild(guild_id)
            if guild is None:
                return await ctx.send(f'Invalid Guild ID given.')
        else:
            guild = ctx.guild
        
        channels = sorted(guild.channels, key=lambda channel: channel.position, reverse=False)     
                                
        channel_string = ""
        for channel in channels:
            position = channel.position
            channel_string += f"""{channel.name} - {position}\n"""
        
        f = open("export/chanlist.txt", "w")
        f.write(channel_string)
        f.close()     
        
        file = discord.File("export/chanlist.txt")
        
        await ctx.send(str("Dumped data to file"), files=[file])
          
        
    @commands.command(name="memberroles")
    async def user_roles_info(self, ctx: Context, *, user_id: int = None) -> None:
        """Returns a list of a members roles and their corresponding IDs."""
        if user_id is not None and await self.bot.is_owner(ctx.author):
            user = self.bot.get_user(user_id)
            if user is None:
                return await ctx.send(f'Invalid User ID given.')
        else:
            user = user
       
        # Sort the roles by the order as shown in the client's Roles UI
        roles = sorted(user.roles, key=lambda role: role.position, reverse=True)
        #roles = [role for role in roles if role.name != "@everyone"]        

        # Build a string
        role_string = ""
        for role in roles:
            role_string += f"{role.position} - {role.mention}\n"
       
        embed = discord.Embed(title="Roles for " + user.display_name, colour=Colour.blurple(), description=f"""{role_string}""")
        
       
        await ctx.send(embed=embed)     

    @commands.command(name="roleinfo", aliases=['ri'])
    async def roleinfo(self, ctx, *, rolename, guild_id: int = None):
        '''Get information about a role. Case Sensitive!'''
        if guild_id is not None and await self.bot.is_owner(ctx.author):
            guild = self.bot.get_guild(guild_id)
            if guild is None:
                return await ctx.send(f'Invalid Guild ID given.')
        else:
            guild = ctx.guild
        
        try:
            role = discord.utils.get(guild.roles, name=rolename)
        except:
            return await ctx.send(f"Role could not be found. The system IS case sensitive!")

        em = discord.Embed(description=f'Role ID: {str(role.id)}', color=role.color or discord.Color.green())
        em.title = role.name
        perms = ""
        if role.permissions.administrator:
            perms += "Administrator, "
        if role.permissions.create_instant_invite:
            perms += "Create Instant Invite, "
        if role.permissions.kick_members:
            perms += "Kick Members, "
        if role.permissions.ban_members:
            perms += "Ban Members, "
        if role.permissions.manage_channels:
            perms += "Manage Channels, "
        if role.permissions.manage_guild:
            perms += "Manage Guild, "
        if role.permissions.add_reactions:
            perms += "Add Reactions, "
        if role.permissions.view_audit_log:
            perms += "View Audit Log, "
        if role.permissions.read_messages:
            perms += "Read Messages, "
        if role.permissions.send_messages:
            perms += "Send Messages, "
        if role.permissions.send_tts_messages:
            perms += "Send TTS Messages, "
        if role.permissions.manage_messages:
            perms += "Manage Messages, "
        if role.permissions.embed_links:
            perms += "Embed Links, "
        if role.permissions.attach_files:
            perms += "Attach Files, "
        if role.permissions.read_message_history:
            perms += "Read Message History, "
        if role.permissions.mention_everyone:
            perms += "Mention Everyone, "
        if role.permissions.external_emojis:
            perms += "Use External Emojis, "
        if role.permissions.connect:
            perms += "Connect to Voice, "
        if role.permissions.speak:
            perms += "Speak, "
        if role.permissions.mute_members:
            perms += "Mute Members, "
        if role.permissions.deafen_members:
            perms += "Deafen Members, "
        if role.permissions.move_members:
            perms += "Move Members, "
        if role.permissions.use_voice_activation:
            perms += "Use Voice Activation, "
        if role.permissions.change_nickname:
            perms += "Change Nickname, "
        if role.permissions.manage_nicknames:
            perms += "Manage Nicknames, "
        if role.permissions.manage_roles:
            perms += "Manage Roles, "
        if role.permissions.manage_webhooks:
            perms += "Manage Webhooks, "
        if role.permissions.manage_emojis:
            perms += "Manage Emojis, "

        if perms is None:
            perms = "None"
        else:
            perms = perms.strip(", ")

        em.add_field(name='Hoisted', value=str(role.hoist))
        em.add_field(name='Position from bottom', value=str(role.position))
        em.add_field(name='Managed by Integration', value=str(role.managed))
        em.add_field(name='Mentionable', value=str(role.mentionable))
        em.add_field(name='People in this role', value=str(len(role.members)))

        pages = []
        pages.append(em)

        em2 = discord.Embed(description=f'Role ID: {str(role.id)}', color=role.color or discord.Color.green())
        em2.title = role.name
        em2.add_field(name='Permissions', value=perms)

        pages.append(em2)

        thing = str(role.created_at.__format__('%A, %B %d, %Y'))

        p_session = PaginatorSession(ctx, footer=f'Created At: {thing}', pages=pages)
        await p_session.run()


def setup(bot):
    bot.add_cog(Info(bot))