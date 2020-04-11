#!/usr/bin/env python
# coding: utf-8

import discord
import os
import re

from dataclasses import dataclass
from dotenv import load_dotenv
from typing import List, Dict

__author__ = "Adrien Lescourt"
__email__ = "adrien.lescourt@hesge.ch"
__copyright__ = "2020, HES-SO"
__status__ = "Dev"
__version__ = "0.2"


"""
Discord bot to creates polls

The question must comes as first argument after the /poll
All arguments must comes between double quotes
You can optionally add choices.

/poll "Question"
or
/poll "Question" "Choice A" "Choice B" "Choice C"
"""


REGEX = re.compile(r'"(.*?)"')


class PollException(Exception):
    pass


@dataclass
class Poll:
    question: str
    choices: List[str]

    @classmethod
    def from_str(cls, poll_str: str) -> "Poll":
        """Return a Poll object from a string that match this template:

        '/poll "Question comes first" "then first choice" "second choice" "third choice"'     end so on if needed

        or simpler question that need binary answer:
        '/poll "Only the question"

        Raises PollException if the double quotes count is odd
        """
        quotes_count = poll_str.count('"')
        if quotes_count == 0 or quotes_count % 2 != 0:
            raise PollException("Poll must have an even number of double quotes")

        fields = re.findall(REGEX, poll_str)
        return cls(fields[0], fields[1:] if len(fields) > 0 else [])

    def to_embed(self) -> discord.Embed:
        """Construct the nice and good looking discord Embed object that represent the poll"""
        description = "\n".join(
            self.get_regional_indicator_symbol(idx) + " " + choice
            for idx, choice in enumerate(self.choices)
        )
        title = "📊" + self.question
        embed = discord.Embed(
            title=title, description=description, color=discord.Color.dark_red()
        )
        return embed

    def reactions(self) -> List[str]:
        """Add as many reaction as the Poll choices needs"""
        if self.choices:
            return [
                self.get_regional_indicator_symbol(i) for i in range(len(self.choices))
            ]
        else:
            return ["👍", "👎"]

    @staticmethod
    def get_regional_indicator_symbol(idx: int) -> str:
        """idx=0 -> A, idx=1 -> B, ... idx=25 -> Z"""
        if 0 <= idx < 26:
            return chr(ord("\U0001F1E6") + idx)
        return ""


class EasyPoll(discord.Client):
    """Simple discord bot that creates poll

    Each time a poll is send, we store it in a dict. When the bot read one of its own message, it checks
    in the dict it the poll exists. If it does, it addthe reactions emoji to it
    """

    def __init__(self, **options):
        super().__init__(**options)
        self.polls: Dict[str, Poll] = {}

    @staticmethod
    def help() -> discord.Embed:
        description = """/poll "Question"
        Or
        /poll "Question" "Choice A" "Choice B" "Choice C"
        """
        embed = discord.Embed(
            title="Usage:", description=description, color=discord.Color.dark_red()
        )
        embed.set_footer(text="HEPIA powered")
        return embed

    @staticmethod
    def get_poll_key(channel_id: int, question: str) -> str:
        return str(channel_id) + question

    async def on_ready(self) -> None:
        print(f"{self.user} has connected to Discord!")
        activity = discord.Game("/poll")
        await self.change_presence(activity=activity)

    async def send_reactions(self, message: discord.message) -> None:
        """Add the reactions to the just sent poll embed message"""
        if not message.embeds:
            return
        key = self.get_poll_key(message.channel.id, message.embeds[0].title)
        poll = self.polls.get(key)
        if poll:
            for reaction in poll.reactions():
                await message.add_reaction(reaction)
            self.polls.pop(key)

    async def send_poll(self, message: discord.message) -> None:
        """Send the embed poll to the channel"""
        poll = Poll.from_str(message.content)
        # TODO: find a better key... can we hide data in the embed object?
        key = self.get_poll_key(message.channel.id, "📊" + poll.question)
        self.polls[key] = poll
        await message.channel.send(embed=poll.to_embed())

    async def on_message(self, message: discord.message) -> None:
        """Every time a message is send on the server, it arrives here"""

        if message.author == self.user:
            await self.send_reactions(message)
            return

        if message.content.startswith("/poll"):
            try:
                await self.send_poll(message)
            except PollException:
                await message.channel.send(embed=self.help())


if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("DISCORD_TOKEN")
    client = EasyPoll()
    client.run(token)
