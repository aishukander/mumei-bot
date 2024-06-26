#各種使用的模組
"""======================================================================================="""
import discord
from discord.ext import commands
import os
import random
import modules.json
from modules.json import setting_json_path, token_json_path
"""======================================================================================="""

intents = discord.Intents.all()

#加載setting.json的內容
jdata = modules.json.open_json(setting_json_path)

#加載TOKEN
TOKEN = modules.json.open_json(token_json_path)

#呼喚bot的前綴
bot = commands.Bot(command_prefix="~",intents=intents)

#刪除help指令
bot.remove_command("help")

@bot.event
async def on_ready():
    #載入所有位於cogs的cog
    async def load_cogs():
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                bot.load_extension(f'cogs.{filename[:-3]}')
    
    await load_cogs()

    #啟動時會在終端機印出的訊息
    print(f"=========================================")
    print(f"=   mumei Bot Logged in as {bot.user}   =")
    print(f"=             >>Bot start<<             =")
    print(f"=========================================")

    #bot的狀態顯示
    await bot.change_presence(activity=discord.Game(name="~help 來獲取指令列表"))

#用於加載、卸載、重讀不同cosg檔
"""======================================================================================="""
@bot.command()
async def load(ctx, extension):
    #檢測使用者的伺服器管理員權限
    if ctx.author.guild_permissions.administrator:
        try:
            bot.load_extension(f"cogs.{extension}")
            await ctx.send(f"{extension}模塊加載完成")
        except Exception as e:
            await ctx.send(f"加載模塊時發生錯誤: {e}")
    #告知使用者沒有管理員權限
    else:
        await ctx.send("你沒有管理者權限用來執行這個指令")

@bot.command()
async def unload(ctx, extension):
    if ctx.author.guild_permissions.administrator:
        try:
            bot.unload_extension(f"cogs.{extension}")
            await ctx.send(f"{extension}模塊卸載完成")
        except Exception as e:
            await ctx.send(f"卸載模塊時發生錯誤: {e}")
    else:
        await ctx.send("你沒有管理者權限用來執行這個指令")

@bot.command()
async def reload(ctx, extension):
    if ctx.author.guild_permissions.administrator:
        try:
            bot.reload_extension(f"cogs.{extension}")
            await ctx.send(f"{extension}模塊重載完成")
        except Exception as e:
            await ctx.send(f"重載模塊時發生錯誤: {e}")
    else:
        await ctx.send("你沒有管理者權限用來執行這個指令")

@bot.command()
async def list(ctx):
    if ctx.author.guild_permissions.administrator:
        loaded_cogs = [cog for cog in bot.cogs]
        message = "已載入的 cog 如下：\n"
        for cog in loaded_cogs:
            message += f"* {cog}\n"
        await ctx.send(message)
    else:
        await ctx.send("你沒有管理者權限用來執行這個指令")
"""======================================================================================="""

#用來取得bot的邀請連結
@bot.command()
async def invitation(ctx):
    color = random.randint(0, 16777215)
    embed=discord.Embed(title="------連結------", url=jdata["invitation"], description="狠狠的點下去吧", color=color)
    await ctx.send(embed=embed)

#測試bot的ping值
@bot.command()
async def ping(ctx):
    await ctx.send(f"{round(bot.latency*1000)}(ms)")

tag_on = 0
#管理tag回覆功能指令
@bot.command()
async def tag(ctx, action: str):
    if ctx.author.guild_permissions.administrator:
        global tag_on
        if action.lower() == "on":
            tag_on = 1
            await ctx.send("已啟用tag功能")
        
        elif action.lower() == "off":
            tag_on = 0
            await ctx.send("已暫時關閉tag功能")
        
        else:
            await ctx.send("無效的動作參數, 請使用 `on` 或 `off`")
    else:
        await ctx.send("你沒有管理者權限用來執行這個指令")

#tag回覆功能本體
@bot.event
async def on_message(msg):
    if tag_on and "405704403937525782" in msg.content and msg.author != bot.user:
        await msg.channel.send("十秒だけ持ちこたえてくれ!")
    await bot.process_commands(msg)

if __name__ == "__main__":
    bot.run(TOKEN["BOT_TOKEN"])
