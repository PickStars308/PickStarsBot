import requests
from nonebot import get_plugin_config, on_command
from nonebot.adapters.onebot.v11 import Event
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me

from Utils.ControlTool import ControlTool
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="Hitokoto",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)


Hitokoto = on_command("一言", rule=to_me(), aliases={"hitokoto", "Hitokoto"}, priority=1, block=True)

@Hitokoto.handle()
async def _(event: Event):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7'
    }
    params = {
        'type': 'json'
    }

    control_tool = ControlTool()
    GroupID = control_tool.extract_group_id(event.get_session_id())

    if control_tool.is_authorized(GroupID):
        try:
            response = requests.get('https://yyapi.xpdbk.com/api/ian', headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
            text = data["text"]
            author = data["author"]
            await Hitokoto.finish(f'{text}\n\n             —————— {author}')
        except requests.exceptions.RequestException as e:
            print(f"错误获取数据：{e}")
            await Hitokoto.finish('错误获取数据：' + str(e))

    else:
        await Hitokoto.finish(f"本群({GroupID})\n"
                          f"未授权使用本插件，请联系管理员\n"
                          f"发送以下激活命令：\n"
                          f"@[Bot] /启用Robot", reply_message=True)

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