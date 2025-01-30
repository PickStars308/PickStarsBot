import json

import requests
from nonebot import get_plugin_config, on_command
from nonebot.adapters.onebot.v11 import MessageSegment, Bot, Event
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from nonebot.typing import T_State

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="60sNews",
    description="获取 每日 60s 早报",
    usage=(
        "命令：\n"
        "  - @[Bot] /60s\n"
        "示例：\n"
        "  - @[Bot] /60s\n"
        "功能：\n"
        "  - 获取 每日 60s 早报\n"
    ),
    config=Config,
)

config = get_plugin_config(Config)


News = on_command("60s", rule=to_me(), aliases={"60s早报", "早报"}, priority=1, block=True)

@News.handle()
async def _(bot: Bot, event: Event, state: T_State):
    url = "http://api.suxun.site/api/sixs?type=json"
    payload = {}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0',
        'Accept': '*/*',
        'Host': 'api.suxun.site',
        'Connection': 'keep-alive'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    response_data = json.loads(response.text)
    # 解析数据
    code = response_data["code"]
    msg = response_data["msg"]
    if code == "200" and msg == "获取成功":
        date = response_data["date"]
        head_image = response_data["head_image"]
        image = response_data["image"]
        news = response_data["news"]
        weiyu = response_data["weiyu"]
        news_str = "\n\n".join(news)
        message_content = f"\n{weiyu}\n\n{news_str}"
        await News.finish(MessageSegment.image(head_image) + MessageSegment.text(message_content))
