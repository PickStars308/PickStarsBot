import json
import os
import shutil


class FileTool:
    def __init__(self):
        pass

    def write_json_file(file_path: str, new_data: any):
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)

            # 读取现有文件内容（如果文件存在且内容为数组）
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
            except FileNotFoundError:
                data = []  # 文件不存在时，初始化为空数组

            # 确保数据是一个数组
            if not isinstance(data, list):
                print(f"错误：数据 {file_path} 不是预期的格式 (数组)")
                return

            # 将新的数据追加到数组中
            data.append(new_data)

            # 保存更新后的数据到文件
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            print(f"已成功将数据保存到 {file_path}.")

        except json.JSONDecodeError:
            print(f"错误：无法解码 JSON {file_path}.")
        except Exception as e:
            print(f"错误：保存文件时发生未知错误 {file_path}。错误信息：{str(e)}")


    def read_json_file(file_path: str):
        try:
            # 打开文件并读取内容
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)  # 解析JSON内容
            return data
        except FileNotFoundError:
            print(f"错误：文件{file_path} 未找到")
            return None
        except json.JSONDecodeError:
            print(f"错误：无法解码 JSON {file_path}.")
            return None

    # 创建文件夹
    def create_folder(self, folder_path):
        try:
            os.makedirs(folder_path, exist_ok=True)  # exist_ok=True 表示如果文件夹已存在，不会抛出异常
            print(f"文件夹 '{folder_path}' 创建成功。")
        except Exception as e:
            print(f"创建文件夹失败：{e}")

    # 删除文件夹及其内容
    def delete_folder(self, folder_path):
        try:
            shutil.rmtree(folder_path)  # 删除文件夹及其内部所有文件和子文件夹
            print(f"文件夹 '{folder_path}' 删除成功。")
        except Exception as e:
            print(f"删除文件夹失败：{e}")

    # 创建文件
    def create_file(self, file_path, content=""):
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"文件 '{file_path}' 创建成功。")
        except Exception as e:
            print(f"创建文件失败：{e}")

    # 删除文件
    def delete_file(self, file_path):
        try:
            os.remove(file_path)  # 删除文件
            print(f"文件 '{file_path}' 删除成功。")
        except Exception as e:
            print(f"删除文件失败：{e}")

    # 移动文件或文件夹
    def move(self, source, destination):
        try:
            shutil.move(source, destination)
            print(f"'{source}' 移动到 '{destination}' 成功。")
        except Exception as e:
            print(f"移动失败：{e}")

    # 复制文件或文件夹
    def copy(self, source, destination):
        try:
            if os.path.isdir(source):  # 如果是文件夹
                shutil.copytree(source, destination)
            else:  # 如果是文件
                shutil.copy(source, destination)
            print(f"'{source}' 复制到 '{destination}' 成功。")
        except Exception as e:
            print(f"复制失败：{e}")

    # 列出文件夹中的文件和子文件夹
    def list_files(self, folder_path):
        try:
            if os.path.exists(folder_path):
                files = os.listdir(folder_path)
                print(f"文件夹 '{folder_path}' 中的文件/文件夹：")
                for file in files:
                    print(file)
            else:
                print(f"文件夹 '{folder_path}' 不存在。")
        except Exception as e:
            print(f"列出文件夹内容失败：{e}")

    # 判断文件是否存在
    def file_exists(file_path: str) -> bool:
        if os.path.exists(file_path):
            return True
        else:
            return False

    # 获取文件的大小
    def get_file_size(self, file_path):
        try:
            if os.path.isfile(file_path):
                file_size = os.path.getsize(file_path)
                print(f"文件 '{file_path}' 的大小为 {file_size} 字节。")
            else:
                print(f"'{file_path}' 不是一个有效的文件。")
        except Exception as e:
            print(f"获取文件大小失败：{e}")
