import string

import requests
from nonebot import get_plugin_config, on_message, on_notice
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment, PokeNotifyEvent, NoticeEvent
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="AtEvent",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)


at = on_message(rule=to_me())

@at.handle()
async def _(bot: Bot, event: MessageEvent):
    user_id = event.user_id
    get_msg = str(event.get_message())
    if not get_msg:
        infos = await bot.get_stranger_info(user_id=user_id)
        template = string.Template("$Hitokoto\n\n"
                                   "你好, $Name! \n"
                                   "我是 星辰Bot\n"
                                   "你有什么需要吗？")
        # 网络请求：http://api.suxun.site/api/qinghua 代码
        response = requests.get('http://api.suxun.site/api/yiyan')
        data = response.json()
        # 提取需要的数据
        qinghua = data['Hitokoto']
        # 将数据存入字典
        data = {
            'Hitokoto': f'Hitokoto：{qinghua}',
            'Name': f'{infos.get("nickname")}',
            'Place': 'Wonderland'
        }
        # 使用模板替换变量
        result = template.substitute(data)
        await at.send(MessageSegment.text(result) + MessageSegment.face(319),reply_message=True)


# 使用 on_notice 装饰器来注册群戳一戳提醒事件监听器
group_poke = on_notice()

# 以下为戳一戳回复事件
@group_poke.handle()
async def _(bot: Bot, event: NoticeEvent):
    if isinstance(event, PokeNotifyEvent):
        if event.target_id == event.self_id:  # 判断戳的是不是机器人？不然就监听所有的戳一戳事件了。
            group_id = event.group_id
            user_id = event.user_id
            try:
                # 获取数据
                infos = await bot.get_stranger_info(user_id=user_id)
                # ------开发环境调试
                # # 保存为 JSON 文件
                # with open('stranger_info.json', 'w', encoding='utf-8') as file:
                #    json.dump(infos, file, ensure_ascii=False, indent=4)
                # ------开发环境调试
                nickname = infos.get('nickname')
            except Exception as e:
                nickname = ""

            data = MessageSegment.image(
                "https://tianquan.gtimg.cn/nudgeaction/item/8/expression.jpg") + MessageSegment.text(
                "竟然有人会尝试戳我\n") + "所以旅行者(" + MessageSegment.text(
                f"{nickname})\n我是星辰Bot，有什么需要帮助的吗？")
            await group_poke.finish(data)

            # ------开发环境调试
            # print("戳一戳提醒事件" + str(infos))
            # print("戳一戳提醒事件" + nickname)
            # print("戳一戳提醒事件" + str(event).replace("[notice.notify.poke]: ",""))
            # print("戳一戳提醒事件：" + str(event.target_id) + "被戳了戳")
            # ------开发环境调试