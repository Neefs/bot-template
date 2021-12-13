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
                                self.bot.load_extension(cogstr)
                                cogs += f"\n\n📥 `{cogstr}`"
                            except (discord.ExtensionAlreadyLoaded,):
                                self.bot.unload_extension(cogstr)
                                self.bot.load_extension(cogstr)
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
                    self.bot.load_extension(cog)
                    cogs += f"\n\n📥 `{cog}`"
                except (discord.ExtensionAlreadyLoaded,):
                    self.bot.unload_extension(cog)
                    self.bot.load_extension(cog)
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
                        self.bot.load_extension(cogstr)
                        cogs += f"\n\n📥 `{cogstr}`"
                    else:
                        continue
                except (discord.ExtensionAlreadyLoaded,):
                    self.bot.unload_extension(cogstr)
                    self.bot.load_extension(cogstr)
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
                                self.bot.unload_extension(cogstr)
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
                    self.bot.unload_extension(cog)
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
                        self.bot.unload_extension(cogstr)
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
        message = await ctx.send(embed=Embed(title="Restarting... Allow up to 20 seconds", color=self.bot.color))

        self.restart_bot()

    def restart_bot(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)
        


                    

        


def setup(bot):
    bot.add_cog(Development(bot))
