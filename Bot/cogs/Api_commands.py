import asyncio
import base64
from io import BytesIO
from operator import ge
import random
import aiohttp
from click import prompt
import discord
import os
from discord.ext import commands
from discord import InteractionResponse, app_commands
import requests
from translate import Translator
from craiyon import Craiyon, craiyon_utils


waifuBaseURL = "https://api.waifu.pics/"
RANDOMGIRLBASEURL = "https://randomuser.me/api/?gender=female"

class Api_commands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
    
    @app_commands.command(name="text-to-image",description="Text to Image Generator; ")
    async def text_to_image(self,interaction:discord.Interaction, prompt: str):
        AiImgEmbed = discord.Embed(title="Prompt: "+prompt, colour=discord.Colour.random())
        inter = interaction.response
        await inter.defer(thinking=True)
        generator = Craiyon()
        generated_images = await generator.async_generate(prompt)
        print(generated_images.images)
        img = generated_images.images[0]
        AiImgEmbed.set_image(url=img)
        await interaction.followup.send(embed=AiImgEmbed)
        # print(url)

    @app_commands.command(name="hot-or-not",description="Rate this girl hot or not")
    async def hotornot(self, interaction: discord.Interaction):
        hotornotEmbed = discord.Embed(title="Rate this girl by using :thumbsup: or :thumbsdown:",colour=discord.Colour.random())

        response = requests.get(RANDOMGIRLBASEURL)
        if response.status_code == 200:
    # Parse the JSON data
            data = response.json()
            large_picture_url = data['results'][0]['picture']['large']
            hotornotEmbed.set_image(url=large_picture_url)
        await interaction.response.send_message(embed=hotornotEmbed)
        
    
    @app_commands.command(name="slash-girls",description='Slash Girls? More like smashgirls; Generates random waifu image of your choice.')
    
    @app_commands.choices(girltype =[
        app_commands.Choice(name="Waifu", value="waifu"),
        app_commands.Choice(name="Neko", value="neko"),
        app_commands.Choice(name="Shinobu", value="shinobu"),
        app_commands.Choice(name="Megumin", value="megumin")
    ])
    @app_commands.choices(category =[
    app_commands.Choice(name="NSFW", value="nsfw")
    ])
    async def slashgirls(self,interaction: discord.Interaction, girltype: str, category: str = "sfw"):
        channel = interaction.channel
        
        if (girltype== 'neko'):
            imageCategory = "sfw" if category == "sfw" else "nsfw"
            if imageCategory == "nsfw":
                if await is_nsfw(channel=channel):
                    await fetch_img(imageCat=imageCategory, girltype=girltype, interaction=interaction)
                else:
                    await interaction.response.send_message("Try in a NSFW channel!")
            elif imageCategory == "sfw":
                await fetch_img(imageCat=imageCategory, girltype=girltype, interaction=interaction)
            
        elif (girltype == 'waifu'):
            imageCategory = "sfw" if category == "sfw" else "nsfw"
            if imageCategory == "nsfw":
                if await is_nsfw(channel=channel):
                    await fetch_img(imageCat=imageCategory, girltype=girltype, interaction=interaction)
                else:
                    await interaction.response.send_message("Try in a NSFW channel!")
            elif imageCategory == "sfw":
                await fetch_img(imageCat=imageCategory, girltype=girltype, interaction=interaction)

        elif (girltype=='megumin'):
                imageCategory = "sfw" if category == "sfw" else "nsfw"
                if imageCategory == "nsfw":
                    if await is_nsfw(channel=channel):
                        await interaction.response.send_message("Realy? No megumin nsfw!")
                    else:
                        await interaction.response.send_message("Try in a NSFW channel!")
                elif imageCategory == "sfw":
                    await fetch_img(imageCat=imageCategory, girltype=girltype, interaction=interaction)

        elif (girltype == 'shinobu'):
                imageCategory = "sfw" if category == "sfw" else "nsfw"
                if imageCategory == "nsfw":
                    if await is_nsfw(channel=channel):
                        await interaction.response.send_message("Really? No shinobu nsfw!")
                    else:
                        await interaction.response.send_message("Try in a NSFW channel!")
                elif imageCategory == "sfw":
                    await fetch_img(imageCat=imageCategory, girltype=girltype, interaction=interaction)






async def fetch_json(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            return data
        
        
async def fetch_img(imageCat: str, girltype:str, interaction: discord.Interaction):
    slashgirlsEmbeds = discord.Embed(title="Enjoy your slash girl 🤤",colour=discord.Colour.random())
    updatedURL = waifuBaseURL+imageCat+"/"+girltype
    data = await fetch_json(updatedURL)
    imgurl = data['url']
    slashgirlsEmbeds.set_image(url=imgurl)
    await interaction.response.send_message(embed=slashgirlsEmbeds)
        
async def is_nsfw(channel: discord.Interaction.channel):
    if isinstance(channel,discord.TextChannel):
        if channel.nsfw:
            return True
        else:
            return False
    else:
        return "bruh"
        
async def setup(bot: commands.Bot):
    # print("Api_commands is loaded")
    await bot.add_cog(Api_commands(bot))
