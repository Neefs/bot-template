from discord.ext import commands
import mystbin
import aiohttp
import os
import jishaku


class PlaceHolder(commands.Bot):
    def __init__(self, **options):
        self.config = options.pop("config")
        self.name = self.config["bot"]["name"]
        self.prefix = self.config["bot"]["prefix"]
        self.devs = self.config["bot"]["developers"]
        self.color = 0xFF0AF0
        super().__init__(commands.when_mentioned_or(self.prefix), **options)

    @property
    def me(self):
        """Alias for bot.user"""
        return self.user

    @property
    def id(self):
        """Alias for bot.user.id"""
        return self.user.id

    def load_cogs(self, folders: str | list):
        if isinstance(folders, str):
            folders = [folders]
        for folder in folders:
            try:
                for filename in os.listdir(folder):
                    if filename.endswith(".py") and not filename.startswith("_"):
                        self.load_extension(f"{folder}.{filename[:-3]}")
            except FileNotFoundError:
                print(str(folder) + " Could not be found")

    async def post_code(self, code, lang=None) -> str:
        if not lang:
            lang = "python"
        client = mystbin.Client()
        returned = await client.post(code, lang)
        await client.close()
        return returned

    async def starting_logic(self):
        self.load_cogs(["commands", "events"])
        self.load_extension("jishaku")

    async def closing_logic(self):
        await self.close()
