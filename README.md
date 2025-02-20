# [mumei-bot](https://discord.com/api/oauth2/authorize?client_id=999157840063242330&permissions=8&scope=applications.commands+bot)
要下載一般最新版本請點Release,選最上面的版本然後下載mumei-bot.zip <br>
[要下載最新測試版請點這裡](https://github.com/aishukander/mumei-bot/archive/refs/heads/main.zip) <br>

## 初始化
(音樂功能依賴FFmpeg) <br>
等容器創建完畢再自行添加Token.json至/opt/mumei-bot/json內 <br>
或是直接複製一份完整的json資料夾進/opt/mumei-bot/ <br>

Token.json
```json
{
    "Bot_Token":"",
    "Google_AI_Key":""
}
```

## 啟動
Docker compose <br>
```yml
services:
  mumei-bot:
    container_name: mumei-bot
    image: aishukander/mumei-bot
    restart: unless-stopped
    volumes:
      - /opt/mumei-bot/json:/bot/json
      - /opt/mumei-bot/CallPicture:/bot/CallPicture
```

Docker cli <br>
```bash
docker run -d \
--name=mumei-bot \
--restart=unless-stopped \
-v /opt/mumei-bot/json:/bot/json \
-v /opt/mumei-bot/CallPicture:/bot/CallPicture \
aishukander/mumei-bot
```
