import json
import os

class ControlTool:
    def __init__(self):
        self.group_auth_file_path = "Config/Authorized/Group.json"
        self.admin_auth_file_path = "Config/Authorized/Admins.json"

    def is_admin_authorized(self, admin_id: int) -> bool:
        """
        判断管理员是否授权，返回布尔值
        授权文件在 Config/Authorized/Admin.json 中
        判断 admin_id 是否在授权列表中
        """
        # 检查文件是否存在
        if not os.path.exists(self.admin_auth_file_path):
            print(f"管理员授权文件 '{self.admin_auth_file_path}' 不存在！")
            return False

        try:
            # 打开并加载 JSON 文件
            with open(self.admin_auth_file_path, "r", encoding="utf-8") as file:
                authorized_admins  = json.load(file)

            # 判断 admin_id 是否在授权列表中
            return admin_id in authorized_admins

        except Exception as e:
            print(f"读取管理员授权文件失败：{e}")
            return False

    def is_authorized(self, group_id: int) -> bool:
        """
        判断群是否授权，返回布尔值
        授权文件在 Config/Authorized/Group.json 中
        判断 group_id 是否在授权列表中
        """
        # 检查文件是否存在
        if not os.path.exists(self.group_auth_file_path):
            print(f"授权文件 '{self.group_auth_file_path}' 不存在！")
            return False

        try:
            # 打开并加载 JSON 文件
            with open(self.group_auth_file_path, "r", encoding="utf-8") as file:
                authorized_groups = json.load(file)

            # 判断 group_id 是否在授权列表中
            return group_id in authorized_groups

        except Exception as e:
            print(f"读取授权文件失败：{e}")
            return False

    @staticmethod
    def extract_group_id(group_str: str) -> int:
        """
        从字符串中提取群ID
        """
        try:
            parts = group_str.split('_')
            if len(parts) == 3:
                return int(parts[1])
            else:
                return None
        except ValueError:
            return None

    @staticmethod
    def extract_type(admin_str: str) -> str:
        """
        从字符串中提取类型
        """
        parts = admin_str.split('_')
        if len(parts) == 3:
            return str(parts[0])
        else:
            return None

