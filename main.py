#各種使用的模組
"""======================================================================================="""
import discord
from discord.ext import commands
import os
import random
import asyncio
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
    #同步斜線指令
    slash = await bot.tree.sync()

    #載入所有位於cogs的cog
    cog_path = "cogs"
    extensions = []

    for filepath in os.listdir(cog_path):
        if filepath.endswith(".py") and not filepath.startswith("_"):
            cog = f"{cog_path}.{filepath[:-3]}"
            extensions.append(cog)
    await asyncio.gather(*[bot.load_extension(ext) for ext in extensions])

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
            await bot.load_extension(f"cogs.{extension}")
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
            await bot.unload_extension(f"cogs.{extension}")
            await ctx.send(f"{extension}模塊卸載完成")
        except Exception as e:
            await ctx.send(f"卸載模塊時發生錯誤: {e}")
    else:
        await ctx.send("你沒有管理者權限用來執行這個指令")

@bot.command()
async def reload(ctx, extension):
    if ctx.author.guild_permissions.administrator:
        try:
            await bot.reload_extension(f"cogs.{extension}")
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
@bot.tree.command(name = "invitation", description = "獲取Bot的邀請連結")
async def invitation(interaction: discord.Interaction):
    color = random.randint(0, 16777215)
    embed=discord.Embed(title="------連結------", url=jdata["invitation"], description="狠狠的點下去吧", color=color)
    await interaction.response.send_message(embed=embed)

#測試bot的ping值
@bot.tree.command(name = "ping", description = "PingBot")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"{round(bot.latency*1000)}(ms)")

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
