from nonebot import get_plugin_config, on_command
from nonebot.adapters.onebot.v11 import Message
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="TestPlugin",
    description="该插件是一个测试功能插件，功能测试完毕后，将转移到正式插件",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

weather = on_command("天气", rule=to_me(), aliases={"weather", "查天气"}, priority=10, block=True)

@weather.handle()
async def handle_function():
    # await weather.send("天气是...")
    await weather.finish("天气是...")