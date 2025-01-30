import requests
from nonebot import get_plugin_config, on_command
from nonebot.adapters.onebot.v11 import Event
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="Hitokoto",
    description="返回随机一条名人名言。",
    usage=(
        "命令：\n"
        "  - @[Bot] /一言\n"
        "示例：\n"
        "  - @[Bot] /名人名言\n"
        "  - @[Bot] /Word\n"
        "功能：\n"
        "  - 返回随机一条名人名言\n"
    ),
    config=Config,
)

config = get_plugin_config(Config)


Hitokoto = on_command("一言", rule=to_me(), aliases={"名人名言", "Word"}, priority=1, block=True)

@Hitokoto.handle()
async def _(event: Event):
    try:
        response = requests.get('https://xiaoapi.cn/API/yiyan.php')
        response = response.text
        await Hitokoto.finish(f'{response}')
    except requests.exceptions.RequestException as e:
        print(f"错误获取数据：{e}")
        await Hitokoto.finish('错误获取数据：' + str(e))

    # url = 'https://v1.hitokoto.cn'
    #
    # try:
    #     response = requests.get(url)
    #     response.raise_for_status()  # Raise an exception for HTTP errors
    #     data = response.json()  # Parse the JSON response
    #
    #     # Extract hitokoto and uuid
    #     hitokoto_text = data.get('hitokoto', 'No quote available')
    #     uuid = data.get('uuid', '')
    #
    #     # Construct the URL and output the result
    #     hitokoto_url = f'https://hitokoto.cn/?uuid={uuid}'
    #
    #     print(f'Hitokoto: {hitokoto_text}')
    #
    #     FinalLink = "https://s0.wp.com/mshots/v1/" + hitokoto_url + "?w=600&h=400"
    #
    #     redirected_url = Tools.get_redirected_url(FinalLink)
    #     if redirected_url:
    #         print(f"Final redirected URL: {redirected_url}")
    #         await Hitokoto.finish(MessageSegment.image(redirected_url))
    #     else:
    #         await Hitokoto.finish(f'Hitokoto: {hitokoto_text}')
    #
    #     # await Hitokoto.finish(f'Hitokoto: {hitokoto_text}\n {MessageSegment.image("https://urlscan.io/liveshot/?url=" + hitokoto_url)}')
    #
    # except requests.exceptions.RequestException as e:
    #     print(f"Error fetching data: {e}")
    #     await Hitokoto.finish('Error fetching data' + str(e))