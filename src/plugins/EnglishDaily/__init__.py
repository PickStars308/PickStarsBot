import requests
from nonebot import get_plugin_config, on_command
from nonebot.adapters.onebot.v11 import Bot, Event, Message
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from nonebot.typing import T_State

from Utils.Tools import Tools
from .config import TOUTIAOAPI, Config

__plugin_meta__ = PluginMetadata(
    name="EnglishDaily",  # 插件名称
    description="接口返回随机一句英剧句子，包含英语原句、释义、来源等",  # 插件描述
    usage=(
        "命令：\n"
        "  - @[Bot] /每日英语\n"
        "示例：\n"
        "  - @[Bot] /ED\n"
        "功能：\n"
        "  - 接口返回随机一句英剧句子，包含英语原句、释义、来源等\n"
    ),
    config=Config,
)

config = get_plugin_config(Config)


# 定义命令触发器
toutiao = on_command("每日英语", aliases={"ED"}, rule=to_me(), priority=1, block=True)

@toutiao.handle()
async def handle_toutiao(bot: Bot, event: Event, state: T_State):

    api_url = "https://whyta.cn/api/tx/everyday"
    params = {
        "key": TOUTIAOAPI
    }

    if not TOUTIAOAPI:
        await toutiao.finish("未配置 Toutiao API Token，请先配置后再使用。")

    try:
        # 使用 requests 发送 GET 请求
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()

        # 访问各个字段
        code = data['code']
        msg = data['msg']
        result = data['result']
        result_id = result['id']
        content = result['content']
        note = result['note']
        source = result['source']
        date = result['date']

        if code == 200:

            if source == "":
                await toutiao.send(f"日期：{date}\n\n{content}\n\n{note}")

                tts = Tools.text_to_speech(content)
                #发送语音
                await toutiao.finish(Message(f'[CQ:record,file={tts}]'))

            else:
                await toutiao.finish(f"日期：{date}\n\n{content}\n\n{note}\n\n{source}")

        else:
            await toutiao.finish(f"API 返回错误：{data.get('msg')}")
    except requests.exceptions.RequestException as e:
        await toutiao.finish(f"请求失败：{str(e)}")