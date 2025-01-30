from datetime import datetime

import requests
from nonebot import get_plugin_config, on_command
from nonebot.adapters.onebot.v11 import Event, Bot, MessageSegment
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="BingWallpapers",
    description="获取每日 Bing 壁纸",
    usage=(
        "命令：\n"
        "  - @[Bot] /Bing每日壁纸\n"
        "示例：\n"
        "  - @[Bot] /Bing\n"
        "  - @[Bot] /bing\n"
        "功能：\n"
        "  - 获取每日 Bing 壁纸\n"
    ),
    config=Config,
)

config = get_plugin_config(Config)


BingWallpapers = on_command("Bing每日壁纸", rule=to_me(), aliases={"Bing", "bing"}, priority=1, block=True)


@BingWallpapers.handle()
async def bing(bot: Bot, event: Event):
    url = "https://api.dwo.cc/api/bing?info=true"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()

        time = data["time"]

        date_obj = datetime.strptime(time, "%Y%m%d")

        formatted_date = date_obj.strftime("%Y-%m-%d")

        await BingWallpapers.finish(MessageSegment.image(data["url"]) + "\n" + data["title"] + "\n日期：" + formatted_date)
    else:
        await BingWallpapers.finish(f"检索数据失败，状态代码： {response.status_code}")


