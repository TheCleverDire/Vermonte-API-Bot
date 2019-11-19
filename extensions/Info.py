import discord
from discord.ext import commands
from discord import CategoryChannel, Client, Colour, Embed, Guild, Member, Role, TextChannel, User, VoiceChannel, utils
from discord.ext.commands import Bot, BucketType, Cog, Context, command, group
import typing
import colorsys


class Info(commands.Cog):
    """Info"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="guildinfo", aliases=['gi', 'serverinfo'])
    async def guildinfo(self, ctx: Context) -> None:
        """Returns info about a guild"""
        created = ctx.guild.created_at
        features = ", ".join(ctx.guild.features)
        region = ctx.guild.region
        id = ctx.guild.id
        owner = ctx.guild.owner
        
        boostlvl = ctx.guild.premium_tier
        boostlen = ctx.guild.premium_subscription_count
       
        #lists of server elements
        rolelist = ctx.guild.roles
        cats = ctx.guild.categories
        chans = ctx.guild.text_channels
        
        # How many of each type of channel?
        roles = len(ctx.guild.roles)
        channels = ctx.guild.channels
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
        member_count = ctx.guild.member_count
        members = ctx.guild.members
        online = 0
        dnd = 0
        idle = 0
        offline = 0
        mobile = 0
        web = 0
        desktop = 0
        mobileidle = 0
        webidle = 0
        desktopidle = 0
        mobilednd = 0
        webdnd = 0
        desktopdnd = 0
        
        for member in members:
            if str(member.status) == "online":
                online += 1
            elif str(member.status) == "offline":
                offline += 1
            elif str(member.status) == "idle":
                idle += 1
            elif str(member.status) == "dnd":
                dnd += 1
        
        for member in members:
            if str(member.mobile_status) == "online":
                mobile += 1
            if str(member.web_status) == "online":
                web += 1
            if str(member.desktop_status) == "online":
                desktop += 1
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

        embed = Embed(
            colour=Colour.blurple(),
            description=f"""
                **Server (Guild) information**
                ID: {id}
                Created: {created}
                Owner: {owner}
                Voice region: {region}
                Features: {features}
                Nitro Tier: {boostlvl}
                Nitro Boosters: {boostlen}
                **Server Stats**
                Categorys: {cats}
                Channels: {chans}
                Roles: {rolelist}
                **Counts**
                Members: {member_count:,}
                Roles: {roles}
                Text: {text_channels}
                Voice: {voice_channels}
                Channel categories: {category_channels}
                **Members**
                online: {online}
                idle: {idle}
                dnd: {dnd}
                offline: {offline}
                **Client Type**
                Desktop: {desktop} online, {desktopidle} idle, {desktopdnd} busy
                Web: {web} online, {webidle} idle, {webdnd} busy
                Mobile: {mobile} online, {mobileidle} idle, {mobilednd} busy
            """
        )

        embed.set_thumbnail(url=ctx.guild.icon_url)

        await ctx.send(embed=embed)
    
    
    @commands.command(name="channelinfo", aliases=['ci'])
    async def channel_info(self, ctx: Context, channel: TextChannel) -> None:
        """Returns info about a channel."""   
    
        name = ctx.bot.fetch_channel(channel).name
        created = ctx.bot.fetch_channel(channel).created_at
        id = ctx.bot.fetch_channel(channel).id
        catid = ctx.bot.fetch_channel(channel).category_id
        cat = ctx.bot.fetch_channel(channel).category
        topic = ctx.bot.fetch_channel(channel).topic
        pos = ctx.bot.fetch_channel(channel).position
        type = ctx.bot.fetch_channel(channel).type
        nsfw = ctx.bot.fetch_channel(channel).is_nsfw()
        croles = ctx.bot.fetch_channel(channel).changed_roles
    
        embed = Embed(
            colour=Colour.blurple(),
            description=f"""
                **Channel information**
                Created: {created}
                Name: {name}
                ID: {id}
                Category ID: {catid}
                Category: {cat}
                Topic: {topic}
                Position: {position}
                Type: {type}
                NSFW?: {nsfw}
                Changed Roles: {croles}
            """
        )
        
        await ctx.send(embed=embed)
        
    
    @commands.command(name="userinfo", aliases=['ui', 'clientinfo'])
    async def user_info(self, ctx: Context, user: User) -> None:
        """Returns info about a user."""
        
        created = user.created_at
        name = user.name
        avatar = user.avatar_url
        id = user.id
        discrim = user.discriminator
        bot = user.bot
        
        embed = Embed(
            colour=Colour.blurple(),
            description=f"""
                **User information**
                Created: {created}
                Name: {name}
                Discriminator: {discrim}
                ID: {id}
                Tag: {str(name)}
                is a Bot?: {bot}
            """
        )

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
        
        embed = Embed(
            colour=Colour.blurple(),
            description=f"""
                **Bot information**
                Created: {created}
                Name: {name}
                Discriminator: {discrim}
                ID: {id}
                Guilds: {guildcount}
            """
        )

        embed.set_thumbnail(url=ctx.me.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(name="memberinfo", aliases=['mi'])
    async def member_info(self, ctx: Context, user: Member) -> None:
        """Returns info about a member."""
        
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
        mobile = user.is_on_mobile()
        top = user.top_role
        
        #List of users roles
        for i in range(len(user.roles)):
            roles += str(user.roles[i]) + ", "
        
        #Activitie list for user
        for i in range(len(user.activities)):
            activities += str(user.activities[i]) + " "
        
        embed = Embed(
            colour=Colour.blurple(),
            description=f"""
                **Member information**
                Joined: {joined}
                Name: {name}
                Nick: {nick}
                Boosted since: {boostsince}
                Bot?: {bot}
                Activities: {str(activities)}
                Mobile?: {mobile}
                Status: {gstatus}
                Desktop App: {dstatus}
                Web App (Could be on mobile web): {wstatus}
                Mobile App (Android/iOS): {mstatus}
                Roles: {str(roles)}
                Top Role: {top}               
            """
        )

        embed.set_thumbnail(url=user.avatar_url)

        await ctx.send(embed=embed)
        
        
    @commands.command(name="perms")
    async def perm_info(self, ctx: Context, user: Member) -> None:
        """Returns info about a members permissions"""
        
        admin = user.guild_permissions.administrator
        audit = user.guild_permissions.view_audit_log
        server = user.guild_permissions.manage_guild
        role = user.guild_permissions.manage_roles
        chan = user.guild_permissions.manage_channels
        kick = user.guild_permissions.kick_members
        ban = user.guild_permissions.ban_members
        inv = user.guild_permissions.create_instant_invite
        chnick = user.guild_permissions.change_nickname
        mnick = user.guild_permissions.manage_nicknames
        emoji = user.guild_permissions.manage_emojis
        webh = user.guild_permissions.manage_webhooks
        read = user.guild_permissions.read_messages
        send = user.guild_permissions.send_messages
        sendtts = user.guild_permissions.send_tts_messages
        mmsg = user.guild_permissions.manage_messages
        embedl = user.guild_permissions.embed_links
        files = user.guild_permissions.attach_files
        hist = user.guild_permissions.read_message_history
        eone = user.guild_permissions.mention_everyone
        exemojis = user.guild_permissions.external_emojis
        react = user.guild_permissions.add_reactions
        
        embed = Embed(
            colour=Colour.blurple(),
            description=f"""
                **Permission information**
                Administrator?: {admin}*
                
                **General Permissions**
                View Audit Log?: {audit}
                Manage Server?: {server}
                Manage Roles?: {role}
                Manage Channels?: {chan}
                Kick Members?: {kick}
                Ban Members?: {ban}
                Create Invite?: {inv}
                Change Nickname?: {chnick}
                Manage Nicknames?: {mnick}
                Manage Emojis?: {emoji}
                Manage Webhooks?: {webh}
                Read Text/Voice Channels?: {read}
                **Text Permissions**
                Send Msgs?: {send}
                Send TTS?: {sendtts}
                Manage Msgs?: {mmsg}
                Embed Links?: {embedl}
                Attach Files?: {files}
                Read Msg History?: {hist}
                @everyone?: {eone}
                Use External Emojis?: {exemojis}
                Add Reactions?: {react}
                
                _**Notes:**_
                * This perm overrides all below it making everything else automatically true
            """
        )

        embed.set_thumbnail(url=user.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(name="roleperms")
    async def role_perm_info(self, ctx: Context, role: Role) -> None:
        """Returns info about a roles permissions"""
        
        admin = role.permissions.administrator
        audit = role.permissions.view_audit_log
        server = role.permissions.manage_guild
        role = role.permissions.manage_roles
        chan = role.permissions.manage_channels
        kick = role.permissions.kick_members
        ban = role.permissions.ban_members
        inv = role.permissions.create_instant_invite
        chnick = role.permissions.change_nickname
        mnick = role.permissions.manage_nicknames
        emoji = role.permissions.manage_emojis
        webh = role.permissions.manage_webhooks
        read = role.permissions.read_messages
        send = role.permissions.send_messages
        sendtts = role.permissions.send_tts_messages
        mmsg = role.permissions.manage_messages
        embedl = role.permissions.embed_links
        files = role.permissions.attach_files
        hist = role.permissions.read_message_history
        eone = role.permissions.mention_everyone
        exemojis = role.permissions.external_emojis
        react = role.permissions.add_reactions
        
        embed = Embed(
            colour=Colour.blurple(),
            description=f"""
                **Permission information**
                Administrator?: {admin}*
                
                **General Permissions**
                View Audit Log?: {audit}
                Manage Server?: {server}
                Manage Roles?: {role}
                Manage Channels?: {chan}
                Kick Members?: {kick}
                Ban Members?: {ban}
                Create Invite?: {inv}
                Change Nickname?: {chnick}
                Manage Nicknames?: {mnick}
                Manage Emojis?: {emoji}
                Manage Webhooks?: {webh}
                Read Text/Voice Channels?: {read}
                **Text Permissions**
                Send Msgs?: {send}
                Send TTS?: {sendtts}
                Manage Msgs?: {mmsg}
                Embed Links?: {embedl}
                Attach Files?: {files}
                Read Msg History?: {hist}
                @everyone?: {eone}
                Use External Emojis?: {exemojis}
                Add Reactions?: {react}
                
                _**Notes:**_
                * This perm overrides all below it making everything else automatically true
            """
        )

        embed.set_thumbnail(url=user.avatar_url)

        await ctx.send(embed=embed)
    
    @commands.command(name="roles")
    async def roles_info(self, ctx: Context) -> None:
        """Returns a list of all roles and their corresponding IDs."""
        # Sort the roles alphabetically and remove the @everyone role
        roles = sorted(ctx.guild.roles, key=lambda role: role.name)
        roles = [role for role in roles if role.name != "@everyone"]

        # Build a string
        role_string = ""
        for role in roles:
            role_string += f"`{role.id}` - {role.mention}\n"

        # Build an embed
        embed = Embed(
            title="Role information",
            colour=Colour.blurple(),
            description=role_string
        )

        embed.set_footer(text=f"Total roles: {len(roles)}")

        await ctx.send(embed=embed)


    @commands.command(name="role")
    async def role_info(self, ctx: Context, *roles: typing.Union[Role, str]) -> None:
        """
        Return information on a role or list of roles.
        To specify multiple roles just add to the arguments, delimit roles with spaces in them using quotation marks.
        """
        parsed_roles = []

        for role_name in roles:
            if isinstance(role_name, Role):
                # Role conversion has already succeeded
                parsed_roles.append(role_name)
                continue

            role = utils.find(lambda r: r.name.lower() == role_name.lower(), ctx.guild.roles)

            if not role:
                await ctx.send(f":x: Could not convert `{role_name}` to a role")
                continue

            parsed_roles.append(role)

        for role in parsed_roles:
            embed = Embed(
                title=f"{role.name} info",
                colour=role.colour,
            )

            embed.add_field(name="ID", value=role.id, inline=True)

            embed.add_field(name="Colour (RGB)", value=f"#{role.colour.value:0>6x}", inline=True)

            h, s, v = colorsys.rgb_to_hsv(*role.colour.to_rgb())

            embed.add_field(name="Colour (HSV)", value=f"{h:.2f} {s:.2f} {v}", inline=True)

            embed.add_field(name="Member count", value=len(role.members), inline=True)

            embed.add_field(name="Position", value=role.position)

            embed.add_field(name="Permission code", value=role.permissions.value, inline=True)

            await ctx.send(embed=embed)
            

def setup(bot):
    bot.add_cog(Info(bot))