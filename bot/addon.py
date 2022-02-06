import asyncio
import os
from datetime import datetime
from pathlib import Path
import contextlib
import aiosqlite
import disnake
from disnake.ext import commands
from disnake.utils import maybe_coroutine


class ListCall(list):

    def append(self, rhs):
        return super().append(rhs)

    def call(self, *args, **kwargs):
        return asyncio.gather(
            *(maybe_coroutine(func, *args, **kwargs) for func in self)
        )


to_call = ListCall()


class Vexron(commands.Bot):
    def __init__(self, **kwargs):
        super().__init__(self.get_prefix, **kwargs)
        self.cwd = str(Path(__file__).parents[0])
        self.token = kwargs.pop("token", None)
        self.help_command = None

    async def after_db(self):
        """Runs after the db is connected"""
        await to_call.call(self)

    @to_call.append
    async def loading(self):
        # Startup and file loads.
        print("**Starting...**")
        for filename in os.listdir(f'{self.cwd}/cogs'):
            try:
                self.load_extension(f"cogs.{filename[: -3]}")
                print(f"Util ext loaded ({filename})")
            except Exception as e:
                print(f"Failed to load {filename}\n\n[ERROR] {e}")
                pass
        print("Connected!")

    @to_call.append
    async def tables(self):
        await self.db.execute(''' CREATE TABLE IF NOT EXISTS reported(user INT NOT NULL)''')
    

    async def get_prefix(self, message):
        return "v!"

    def starter(self):
        try:
            db = self.loop.run_until_complete(
                aiosqlite.connect(f"{self.cwd}/data/main.sqlite")
            )
        except Exception as e:
            print("Could not connect to database:", e)
        else:
            self.launch_time = datetime.utcnow()
            self.db = db
            self.loop.run_until_complete(self.after_db())
            self.run(self.token)