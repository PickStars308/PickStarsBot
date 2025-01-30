import requests
from nonebot import get_plugin_config
from nonebot.adapters.onebot.v11 import Event, Message
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata
from nonebot.plugin import on_command
from nonebot.rule import to_me

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="Weather",  # 插件名称
    description="查询指定地区天气的 NoneBot2 插件",  # 插件描述
    usage=(
        "命令：\n"
        "  - @[Bot] /天气 <地区名称>\n"
        "示例：\n"
        "  - @[Bot] /天气 北京\n"
        "  - @[Bot] /天气 上海\n"
        "功能：\n"
        "  - 查询指定地区的天气信息\n"
    ),
    config=Config,
)

config = get_plugin_config(Config)


# 定义命令触发器
weather = on_command("天气", rule=to_me(), priority=1)

@weather.handle()
async def _(event: Event, args: Message = CommandArg()):
    msg = args.extract_plain_text()

    if not msg:
        await weather.finish("请输入地区名称，例如：@[Bot] /天气 北京")
    # 调用 API 获取天气数据
    api_url = "https://xiaoapi.cn/API/zs_tq.php"
    params = {
        "type": "zgtq",
        "msg": msg,
        "n": "1"
    }
    try:
        response = requests.get(api_url, params=params)
        data = response.json()
        if data["code"] == 200:
            # 提取天气信息
            weather_info = data['data'].split('\n')
            weather_str = "\n".join(weather_info)
            # 提取生活指数
            life_index = data['shzs'].split('\n')
            life_str = "\n".join(life_index)
            # 提取其他信息
            city = data['keyWord']
            region = data['name']
            tips = data['tips']
            # 组合成最终字符串
            output = (
                f"=== 城市信息 ===\n"
                f"城市: {city}\n"
                f"地区: {region}\n\n"
                f"=== 天气信息 ===\n"
                f"{weather_str}\n\n"
                f"=== 生活指数 ===\n"
                f"{life_str}"
            )
            # 输出结果
            await weather.finish(f"{output}")
        else:
            await weather.finish(f"API 返回错误：{data.get('msg')}")
    except requests.exceptions.RequestException as e:
        await weather.finish(f"请求失败：{str(e)}")
