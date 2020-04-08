#!/usr/bin/env python
# coding: utf-8

import os
from typing import List

import discord
from dotenv import load_dotenv

__author__ = "Adrien Lescourt"
__email__ = "adrien.lescourt@hesge.ch"
__copyright__ = "2020, HES-SO"
__status__ = "Dev"

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD = os.getenv("DISCORD_GUILD")


def get_regional_indicator_symbol(idx: int) -> str:
    """
    idx=0 -> A, idx=1 -> B, etc...
    :param idx:
    :return:
    """
    if 0 <= idx < 26:
        return chr(ord("\U0001F1E6") + idx)
    return ""


def quotes_to_list(str_with_quotes: str) -> List[str]:
    """
    Returns a string list from a string with multiple quotes

    The list is empty if the quotes count is odd

    eg.
    '/poll "this is a test" "and it is" "working"
    returns
    ["this is a test", "and it is", "working"]
    """
    quotes_count = str_with_quotes.count('"')
    if quotes_count == 0 or quotes_count % 2 != 0:
        return []

    return [stripped for s in str_with_quotes.split('"')[1:] if (stripped := s.strip())]


class EasyClient(discord.Client):
    """Simple discord bot that creates poll

    To track the polls sent by the bot and avoid racing between poll sent and poll reaction,
    we store the (channel_id, question) in a dict
    Also used to retreive the choices and add as many regional emoji as needed
    """

    def __init__(self, **options):
        super().__init__(**options)
        self.polls = {}

    @staticmethod
    def help():
        s = "Usage:\n"
        s += '/poll "Question"\n'
        s += "Or\n"
        s += '/poll "Question" "Choice A", "Choice B", "Choice C"...\n'
        return s

    async def on_ready(self):
        print(f"{self.user} has connected to Discord!")

    async def on_message(self, message):
        # message comes from the bot, we need to add the reactions to it
        if message.author == client.user:
            await self._send_reactions(message)
            return

        # message comes from an user
        if message.content.startswith("/easypoll"):
            res = await self._send_choices(message)
            if not res:
                await message.channel.send(self.help())

    async def _send_choices(self, message):
        """Send the message with the question. Reactions will be added afterwards"""
        quotes = quotes_to_list(message.content)
        if quotes:
            question, *choices = quotes
            self.polls[(message.channel.id, question)] = choices
            response = question + " \n "
            response += " \n ".join(
                get_regional_indicator_symbol(idx) + choice
                for idx, choice in enumerate(choices)
            )
            await message.channel.send(response)
            return True
        return False

    async def _send_reactions(self, message):
        """Send emoji reactions after it has send a message with the choices"""
        poll_question, *_ = message.content.split("\n")
        key = message.channel.id, poll_question.strip()
        if key in self.polls:
            if self.polls[key]:
                for idx, _ in enumerate(self.polls[key]):
                    await message.add_reaction(get_regional_indicator_symbol(idx))
                self.polls.pop(key)
            else:
                await message.add_reaction("👍")
                await message.add_reaction("👎")


if __name__ == "__main__":
    client = EasyClient()
    client.run(TOKEN)
