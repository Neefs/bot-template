import os
import sys

from discord import Embed
import traceback as tb
import discord
from discord.ext import commands
from utils.bot import PlaceHolder
from utils.errors import NotDeveloper


class Development(commands.Cog):
    """A Cog that has developer utils"""

    def __init__(self, bot: PlaceHolder):
        self.bot = bot

    def cog_check(self, ctx):
        if not ctx.author.id in self.bot.devs:
            raise NotDeveloper()
        return True

    @commands.Cog.listener()
    async def on_ready(self):
        """Shows that the cog is ready."""
        print("✅ Development cog is ready.")

    @commands.command()
    async def shutdown(self, ctx):
        """Shuts the bot down."""
        await ctx.send(embed=Embed(title="Shutting down", color=0xFF0000))
        await self.bot.closing_logic()

    @commands.command(name="clearconsole", aliases=["cc"])
    async def clear_console(self, ctx):
        """Clears the output console"""
        await ctx.send(embed=Embed(title="Console Cleared", color=self.bot.color))
        os.system("clear")

    @commands.command(name="loadcog", aliases=["lc", "reloadcog", "rc", "load", "reload"])
    async def load_cog(self, ctx: commands.Context, *, cog: str = None):
        """Loads and reloads cogs."""
        folders = ["events", "commands"]
        cogs = ""
        if not cog or cog.lower().strip() in ["~", "all"]:
            for folder in folders:
                try:
                    for filename in os.listdir(folder):
                        if filename.endswith(".py") and not filename.startswith("_"):
                            cogstr = f"{folder}.{filename[:-3]}"
                            try:
                                await self.bot.load_extension(cogstr)
                                cogs += f"\n\n📥 `{cogstr}`"
                            except (commands.ExtensionAlreadyLoaded,):
                                await self.bot.unload_extension(cogstr)
                                await self.bot.load_extension(cogstr)
                                cogs += f"\n\n🔁 `{cogstr}`"
                            except Exception as e:
                                print(
                                    "Ignoring exception while loading cog {}:".format(
                                        cogstr
                                    )
                                )
                                traceback = "".join(
                                    tb.format_exception(type(e), e, e.__traceback__)
                                )
                                cogs += f"\n\n⚠️ `{cogstr}`\n```py\n{traceback}\n```"
                except FileNotFoundError:
                    print(str(folder) + " Could not be found")
            await ctx.send(cogs)
            print(cogs)
            return
        listedcogs = cog.lower().split(' ')
        for cog in listedcogs:
            if cog == 'jishaku':
                try:
                    await self.bot.load_extension(cog)
                    cogs += f"\n\n📥 `{cog}`"
                except (commands.ExtensionAlreadyLoaded,):
                    await self.bot.unload_extension(cog)
                    await self.bot.load_extension(cog)
                    cogs += f"\n\n🔁 `{cog}`"
                except Exception as e:
                    print(
                        "Ignoring exception while loading cog {}:".format(
                            cogstr
                        )
                    )
                    traceback = "".join(
                        tb.format_exception(type(e), e, e.__traceback__)
                    )
                    cogs += f"\n\n📥 ⚠️ `{cogstr}`\n```py\n{traceback}\n```"
                continue

            for folder in folders:
                try:
                    files = os.listdir(folder)
                    cogstr = f'{folder}.{cog}'
                    if (cog + '.py') in files:
                        await self.bot.load_extension(cogstr)
                        cogs += f"\n\n📥 `{cogstr}`"
                    else:
                        continue
                except (commands.ExtensionAlreadyLoaded,):
                    await self.bot.unload_extension(cogstr)
                    await self.bot.load_extension(cogstr)
                    cogs += f"\n\n🔁 `{cogstr}`"
                except Exception as e:
                    print(
                        "Ignoring exception while loading cog {}:".format(
                            cogstr
                        )
                    )
                    traceback = "".join(
                        tb.format_exception(type(e), e, e.__traceback__)
                    )
                    cogs += f"\n\n📥 ⚠️ `{cogstr}`\n```py\n{traceback}\n```"
        await ctx.send(cogs)

    @commands.command(name='unloadcog', aliases=['uc', 'unload'])
    async def unload_cog(self, ctx, *, cog:str = None):
        """Unloads cogs."""
        folders = ["events", "commands"]
        cogs = ""
        if not cog or cog.lower().strip() in ["~", "all"]:
            for folder in folders:
                try:
                    for filename in os.listdir(folder):
                        if filename.endswith(".py") and not filename.startswith("_"):
                            cogstr = f"{folder}.{filename[:-3]}"
                            try:
                                await self.bot.unload_extension(cogstr)
                                cogs += f"\n\n📤 `{cogstr}`"
                            except Exception as e:
                                print(
                                    "Ignoring exception while loading cog {}:".format(
                                        cogstr
                                    )
                                )
                                traceback = "".join(
                                    tb.format_exception(type(e), e, e.__traceback__)
                                )
                                cogs += f"\n\n📤 ⚠️ `{cogstr}`\n```py\n{traceback}\n```"
                except FileNotFoundError:
                    print(str(folder) + " Could not be found")
            await ctx.send(cogs)
            print(cogs)
            return

        listedcogs = cog.lower().split(' ')
        for cog in listedcogs:
            if cog == 'jishaku':
                try:
                    await self.bot.unload_extension(cog)
                    cogs += f"\n\n📤 `{cog}`"
                except Exception as e:
                    print(
                        "Ignoring exception while loading cog {}:".format(
                            cogstr
                        )
                    )
                    traceback = "".join(
                        tb.format_exception(type(e), e, e.__traceback__)
                    )
                    cogs += f"\n\n📤 ⚠️ `{cogstr}`\n```py\n{traceback}\n```"
                continue

            for folder in folders:
                try:
                    files = os.listdir(folder)
                    cogstr = f'{folder}.{cog}'
                    if (cog + '.py') in files:
                        await self.bot.unload_extension(cogstr)
                        cogs += f"\n\n📤 `{cogstr}`"
                    else:
                        continue
                
                except Exception as e:
                    print(
                        "Ignoring exception while loading cog {}:".format(
                            cogstr
                        )
                    )
                    traceback = "".join(
                        tb.format_exception(type(e), e, e.__traceback__)
                    )
                    cogs += f"\n\n📤 ⚠️ `{cogstr}`\n```py\n{traceback}\n```"
        await ctx.send(cogs)

    @commands.command()
    async def restart(self, ctx):
        """Restarts the bot"""
        try:
            await ctx.message.delete()
        except:
            pass
        await ctx.send(embed=Embed(title="Restarting... Allow up to 20 seconds", color=self.bot.color))

        self.restart_bot()

    

    @commands.command(name="synccommands", aliases=['synccommand', 'sync', 'sc'])
    async def sync_commands(self, ctx, guild:int=None):
        """Syncs all application commands"""
        try:
            await ctx.message.delete()
        except:
            pass

        if guild:
            await self.bot.tree.sync(guild=discord.Object(guild))
            await ctx.send(embed=Embed(title="Commands Synced", color=self.bot.color, description=f"Application commands have been synced to {guild}."))
            return

        class ConfirmSyncView(discord.ui.View):
            def __init__(self, bot, msg=None):
                self.bot = bot
                self.msg = msg
                super().__init__(timeout=180)

            async def on_timeout(self) -> None:
                try:
                    await self.msg.delete()
                except:
                    pass

            
            async def interaction_check(self, interaction: discord.Interaction) -> bool:
                return interaction.user == ctx.author

            @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
            async def confirm_button(self, interaction:discord.Interaction, button:discord.ui.Button):
                await self.bot.tree.sync()
                await interaction.response.send_message(embed=Embed(title="Commands Synced", color=self.bot.color, description="Application commands have been synced **globally**."), ephemeral=True)

            @discord.ui.button(label="Cancel", style=discord.ButtonStyle.red)
            async def cancel_button(self, interaction:discord.Interaction, button:discord.ui.Button):
                await interaction.response.send_message(embed=Embed(title="Cancelled", color=0xff0000, description="Cancelled application commands sync."), ephemeral=True)





        view = ConfirmSyncView(self.bot)
        view.msg = await ctx.send("Are you sure", view=view)


        
        
    


    def restart_bot(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)
        


                    

        


async def setup(bot):
    await bot.add_cog(Development(bot))
