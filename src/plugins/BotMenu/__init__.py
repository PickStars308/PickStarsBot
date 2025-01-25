import json
import os

from arclet.alconna import Alconna, Args
from nonebot import get_plugin_config
from nonebot.internal.matcher import Matcher
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me
from nonebot_plugin_alconna import on_alconna

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="BotMenu",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

# 定义菜单路径
MENU_CONFIG_PATH = 'Config/Menu/Function.json'


# 加载菜单配置数据
def load_menu_config():
    if not os.path.exists(MENU_CONFIG_PATH):
        raise FileNotFoundError(f"配置文件 {MENU_CONFIG_PATH} 未找到")

    with open(MENU_CONFIG_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    menus = data.get("Menu", [])

    return menus

def load_menu_data(page: int):
    if not os.path.exists(MENU_CONFIG_PATH):
        raise FileNotFoundError(f"配置文件 {MENU_CONFIG_PATH} 未找到")

    with open(MENU_CONFIG_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 获取 Menu 数据
    menus = data.get("Menu", [])

    # Check if the page number is within the valid range
    if page < 1 or page > len(menus):
        return f"页码 {page} 超出范围，配置中只有 {len(menus)} 页"

    # 获取指定页的 Function 列表
    menu_items = menus[page - 1].get("Function", [])

    # 格式化输出
    return "\n".join(menu_items)


# 注册菜单命令
menu = on_alconna(Alconna("/菜单", Args["page", int, 1]), block=True, priority=1, rule=to_me())

# 定义快捷方式，支持“菜单”和“菜单 1”都作为第一页
menu.shortcut(r"^/菜单$", {"args": [1], "fuzzy": False})  # 默认菜单为第一页
menu.shortcut(r"^/菜单 (\d+)$", {"args": ["{page}"], "fuzzy": False})  # 支持菜单页码


# 处理菜单的函数
@menu.handle()
async def _(matcher: Matcher, page: int):
    # 加载菜单数据
    menu_config = load_menu_config()

    menu_items = load_menu_data(page)

    if "超出范围" in menu_items:
        await matcher.finish(f"                     ⭐错误⭐                 "
                             f"\n\n{menu_items}\n\n"
                             f"                 当前页：{page} / {len(menu_config)}"
                             f"\n\n请发送“菜单 [页码]”查看其他页面")

    await matcher.finish(f"                 ⭐星辰菜单⭐                 "
                         f"\n\n{menu_items}\n\n"
                         f"                 当前页：{page} / {len(menu_config)}"
                         f"\n\n请发送“菜单 [页码]”查看其他页面")