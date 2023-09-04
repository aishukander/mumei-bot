import discord
from discord.ext import commands
from core.classes import Cog_Extension
import re
import asyncio

class cmd(Cog_Extension):

 #刪除所傳的訊息並讓機器人覆誦
  @commands.command()
  async def say(self,ctx,msg):
      if ctx.author.guild_permissions.administrator:
          await ctx.message.delete()
          await ctx.send(msg)
      else:
          await ctx.send("你沒有管理者權限用來執行這個指令")

 #刪除所選數量的訊息
  @commands.command()
  async def delete(self,ctx,num:int):
      if ctx.author.guild_permissions.administrator:
          #刪除訊息(因為指令也算一條訊息 所以num+1)
          await ctx.channel.purge(limit=num+1)
      else:
          await ctx.send("你沒有管理者權限用來執行這個指令")

  @commands.command()
  async def ban(self, ctx, member: discord.Member):
      if ctx.author.guild_permissions.administrator:
          await member.ban()
          await ctx.send(f'{member} 已踢出伺服器')
      else:
          await ctx.send("你沒有管理者權限用來執行這個指令")

  @commands.command()
  async def reword(self,ctx,msg):
      text = msg
      await ctx.send("請輸入要替換的單字：")
      #定義檢查函數來確保只接受用戶自己在同一頻道的訊息
      def check(msg):
          return msg.author == ctx.author and msg.channel == ctx.channel
      try:
          #等待用戶輸入並將訊息存入old參數裡，並且超過6秒沒有回覆就引發異常
          old = await self.bot.wait_for('message', check=check, timeout=6)
          await ctx.send("請輸入要替換成的單字：")
          #等待用戶輸入並將訊息存入new參數裡，並且超過6秒沒有回覆就引發異常
          new = await self.bot.wait_for('message', check=check, timeout=6)
          #將old與new參數傳遞給re.sub函數並完成文本修改
          new_text = re.sub(old.content, new.content, text)
          await ctx.send(new_text)
      except asyncio.TimeoutError:
          #如果發生超時異常，則取消指令並通知用戶
          await ctx.send("您沒有及時回覆，指令已取消。")

async def setup(bot):
    await bot.add_cog(cmd(bot))