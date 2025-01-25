import json

from nonebot import get_plugin_config, on_command
from nonebot.adapters.onebot.v11 import MessageSegment, Bot, Event
from nonebot.adapters.onebot.v12 import GroupMessageEvent
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
import requests
from nonebot.typing import T_State

from Utils.ControlTool import ControlTool
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="60sNews",
    description="60sNews 是 一个获取 60s 早报 的插件",
    usage="@[Bot] /60s",
    config=Config,
)

config = get_plugin_config(Config)


News = on_command("60s", rule=to_me(), aliases={"60s早报", "早报"}, priority=1, block=True)

@News.handle()
async def _(bot: Bot, event: Event, state: T_State):
    control_tool = ControlTool()
    GroupID = control_tool.extract_group_id(event.get_session_id())

    if control_tool.is_authorized(GroupID):
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
            pass
    else:
        await News.finish(f"本群({GroupID})\n"
                          f"未授权使用本插件，请联系管理员", reply_message=True)
