from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="TestPlugin",
    description="该插件是一个测试功能插件，功能测试完毕后，将转移到正式插件",
    usage="无",
    config=Config,
)

config = get_plugin_config(Config)
#
# weather = on_command("天气", rule=to_me(), aliases={"Weather", "查天气"}, priority=10, block=True)
#
# @weather.handle()
# async def handle_function():
#     # await Weather.send("天气是...")
#     await weather.finish("天气是...")

# control_tool = ControlTool()
# GroupID = control_tool.extract_group_id(event.get_session_id())
#
# if control_tool.is_authorized(GroupID):
#     pass
# else:
#     await News.finish(f"本群({GroupID})\n"
#                       f"未授权使用本插件，请联系管理员\n"
#                       f"发送以下激活命令：\n"
#                       f"@[Bot] /启用Robot", reply_message=True)