import discord
from discord.ext import commands
from core.classes import Cog_Extension
import json
import random

with open('setting.json', 'r', encoding='utf8') as jfile:
   jdata = json.load(jfile)

class cmd(Cog_Extension):
  
  @commands.command() 
  async def say(self,ctx,msg):
      await ctx.message.delete() #刪除所傳的訊息 
      await ctx.send(msg)        #讓機器人覆誦

  @commands.command()
  async def delete(self,ctx,num:int):       #delete 數字，決定刪除多少條訊息 
      await ctx.channel.purge(limit=num+1)  #刪除訊息(因為指令也算一條訊息 所以num+1)    

async def setup(bot):
    await bot.add_cog(cmd(bot))