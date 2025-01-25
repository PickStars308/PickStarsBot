import json
import os

from nonebot import get_plugin_config, on_command
from nonebot.adapters.onebot.v11 import Bot, Event, GroupMessageEvent
from nonebot.plugin import PluginMetadata
from nonebot.rule import to_me

from Utils.ControlTool import ControlTool
from Utils.FileTool import FileTool
from .config import Administrator, Config

__plugin_meta__ = PluginMetadata(
    name="Administer",
    description="插件 Administer 是一个用于管理机器人的插件，提供了如添加或移除管理员、启用或禁用机器人等功能。",
    usage="使用命令进行管理操作，"
          "例如：添加管理员、移除管理员、启用机器人、禁用机器人"
          "指令均需@机器人"
          "例如：@[Bot] /添加管理员 @[User]"
          "示例："
          "1. 授权管理员：@[Bot] /授权管理员 @[User]"
          "2. 移除管理员：@[Bot] /移除管理员 @[User]"
          "3. 启用机器人：@[Bot] /启用机器人"
          "4. 禁用机器人：@[Bot] /禁用机器人",
    config=Config,
)

ADMIN_FILE_PATH = "Config/Authorized/Admins.json"
GROUP_FILE_PATH = "Config/Authorized/Group.json"

def load_data(type: int):
    if type == 1:
        if FileTool.read_json_file(ADMIN_FILE_PATH):
            return FileTool.read_json_file(ADMIN_FILE_PATH)
        else:
            return []
    elif type == 2:
        if FileTool.read_json_file(GROUP_FILE_PATH):
            return FileTool.read_json_file(GROUP_FILE_PATH)
        else:
            return []
    else:
        return []

def save_data(type: int, data: int):
    if type == 1:
        FileTool.write_json_file(ADMIN_FILE_PATH, data)
    elif type == 2:
        FileTool.write_json_file(GROUP_FILE_PATH, data)
    else:
        return

def delete_data(file: str, data_list, item_to_delete):
    data_list.remove(item_to_delete)
    print(f"已删除 {data_list}。")
    try:
        os.makedirs(os.path.dirname(file), exist_ok=True)
        with open(file, 'w', encoding='utf-8') as file:
            json.dump(data_list, file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"错误：保存文件时发生未知错误 {file}。错误信息：{str(e)}")

# 定义授权管理员指令
authorize_admin = on_command("授权管理员", rule=to_me(), priority=1, block=True)

@authorize_admin.handle()
async def _(bot: Bot, event: Event, QQ = None):

    if ControlTool.extract_type(str(event.get_session_id())) == "group":
        message = event.message
        for segment in message:
            if segment.type == "at":
                QQ = segment.data.get("qq")
                break
        if QQ:
            if Administrator is None:
                await authorize_admin.finish("请先在.env文件中配置：ADMINISTRATOR=Bot管理员", reply_message=True)
            else:
                if int(event.get_user_id()) == Administrator or ControlTool.is_authorized(int(event.get_user_id())):
                    # 读取现有管理员列表
                    AuthorizedAdmins = load_data(1)
                    if int(QQ) in AuthorizedAdmins:
                        # 如果管理员已授权
                        await authorize_admin.finish(f"管理员 {QQ} 已经被授权！", reply_message=True)
                    else:
                        save_data(1, int(QQ))
                        await authorize_admin.finish(f"成功授权管理员 {QQ}！", reply_message=True)
                else:
                    await authorize_admin.finish("只有管理员才能使用此指令！", reply_message=True)
        else:
            await authorize_admin.finish(
                "指令格式错误！\n\n正确格式：\n@[Bot] /授权管理员 @[User]\n\n示例：\n@[Bot] /授权管理员 @[User]"
                , reply_message=True)
    else:
        await authorize_admin.finish("该指令未适配私聊\n"
                                     "请在群聊中使用此指令！", reply_message=True)

# 定义移除管理员指令
remove_admin = on_command("移除管理员", rule=to_me(), priority=1, block=True)

@remove_admin.handle()
async def _(bot: Bot, event: Event, QQ = None):
    if ControlTool.extract_type(str(event.get_session_id())) == "group":
        message = event.message
        for segment in message:
            if segment.type == "at":
                QQ = segment.data.get("qq")
                break

        if QQ:
            if Administrator is None:
                await remove_admin.finish("请先在.env文件中配置：ADMINISTRATOR=Bot管理员", reply_message=True)
            else:
                if int(event.get_user_id()) == Administrator or ControlTool.is_authorized(int(event.get_user_id())):
                    # 读取现有管理员列表
                    AuthorizedAdmins = load_data(1)
                    if int(QQ) in AuthorizedAdmins:
                        delete_data(ADMIN_FILE_PATH, AuthorizedAdmins, int(QQ))
                        await remove_admin.finish(f"成功移除管理员 {QQ}！", reply_message=True)
                    else:
                        # 如果管理员不在列表中
                        await remove_admin.finish(f"管理员 {QQ} 不在授权列表中！", reply_message=True)
                else:
                    await remove_admin.finish("只有管理员才能使用此指令！", reply_message=True)
        else:
            await remove_admin.finish(
                "指令格式错误！\n\n正确格式：\n@[Bot] /移除管理员 @[User]\n\n示例：\n@[Bot] /移除管理员 @[User]"
                , reply_message=True)
    else:
        await authorize_admin.finish("该指令未适配私聊\n"
                                     "请在群聊中使用此指令！", reply_message=True)



# 定义启用Robot指令
enable_robot = on_command("启用机器人", aliases={"启用Robot", "启用robot"}, rule=to_me(), priority=1, block=True)
@enable_robot.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    if ControlTool.extract_type(str(event.get_session_id())) == "group":
        if Administrator is None:
            await enable_robot.finish("请先在.env文件中配置：ADMINISTRATOR=Bot管理员", reply_message=True)
        else:
            if int(event.get_user_id()) == Administrator or ControlTool.is_authorized(int(event.get_user_id())):
                if event.group_id in load_data(2):
                        await enable_robot.finish("Robot已经在该群聊中启用！", reply_message=True)
                else:
                    # 添加群聊到列表并写入文件
                    save_data(2,event.group_id)
                    await enable_robot.finish("成功启用Robot！", reply_message=True)
            else:
                await enable_robot.finish("只有管理员才能使用此指令！", reply_message=True)
    else:
        await authorize_admin.finish("该指令未适配私聊\n"
                                     "请在群聊中使用此指令！", reply_message=True)


# 定义禁用Robot指令
disable_robot = on_command("禁用机器人", aliases={"禁用Robot", "禁用robot"}, rule=to_me(), priority=1, block=True)
@disable_robot.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    if ControlTool.extract_type(str(event.get_session_id())) == "group":
        if Administrator is None:
            await disable_robot.finish("请先在.env文件中配置：ADMINISTRATOR=Bot管理员", reply_message=True)
        else:
            if int(event.get_user_id()) == Administrator or ControlTool.is_authorized(int(event.get_user_id())):
                Robot = load_data(2)
                if int(event.group_id) in Robot:
                    delete_data(GROUP_FILE_PATH, Robot, int(event.group_id))
                    await remove_admin.finish(f"成功禁用Robot", reply_message=True)
                else:
                    # 如果管理员不在列表中
                    await remove_admin.finish(f"Robot已经在该群聊中禁用！", reply_message=True)
            else:
                await disable_robot.finish("只有管理员才能使用此指令！", reply_message=True)
    else:
        await authorize_admin.finish("该指令未适配私聊\n"
                                     "请在群聊中使用此指令！", reply_message=True)